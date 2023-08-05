import os
import glob
import tempfile
import shutil

import pytest

from swh.core.utils import numfile_sortkey as sortkey
from swh.objstorage import get_objstorage
from swh.scheduler.tests.conftest import *  # noqa
from swh.archiver.storage import get_archiver_storage
from swh.archiver import (ArchiverWithRetentionPolicyDirector,
                          ArchiverWithRetentionPolicyWorker)
from swh.archiver.tests import SQL_DIR


DUMP_FILES = os.path.join(SQL_DIR, '*.sql')


@pytest.fixture(scope='session')
def celery_includes():
    return [
        'swh.archiver.tasks',
    ]


@pytest.fixture
def swh_archiver_db(postgresql):
    all_dump_files = sorted(glob.glob(DUMP_FILES), key=sortkey)

    cursor = postgresql.cursor()
    for fname in all_dump_files:
        with open(fname) as fobj:
            cursor.execute(fobj.read())
    postgresql.commit()
    return postgresql


@pytest.fixture
def swh_archiver(swh_archiver_db):

    # Create source storage
    src_root = tempfile.mkdtemp()
    src_config = {
        'cls': 'pathslicing',
        'args': {
            'root': src_root,
            'slicing': '0:2/2:4/4:6'
        }
    }
    src_storage = get_objstorage(**src_config)

    dest_root = tempfile.mkdtemp()
    dest_config = {
        'cls': 'pathslicing',
        'args': {
            'root': dest_root,
            'slicing': '0:2/2:4/4:6',
        }
    }
    dest_storage = get_objstorage(**dest_config)

    # Keep mapped the id to the storages
    storages = {
        'src': src_storage,  # uffizi
        'dest': dest_storage  # banco
    }
    cursor = swh_archiver_db.cursor()
    for storage in storages:
        cursor.execute("INSERT INTO archive(name) VALUES(%s)", (storage,))
    swh_archiver_db.commit()

    # Override configurations
    src_archiver_conf = {'host': 'src'}
    dest_archiver_conf = {'host': 'dest'}
    src_archiver_conf.update(src_config)
    dest_archiver_conf.update(dest_config)
    archiver_storages = [src_archiver_conf, dest_archiver_conf]

    def parse_config_file(obj, additional_configs):
        return {  # noqa
            'archiver_storage': {
                'cls': 'db',
                'args': {
                    'dbconn': swh_archiver_db,
                },
            },
            'retention_policy': 2,
            'archival_max_age': 3600,
            'batch_max_size': 5000,
            'asynchronous': False,
            'max_queue_length': 100000,
            'queue_throttling_delay': 120,
        }

    orig_director_cfg = ArchiverWithRetentionPolicyDirector.parse_config_file
    ArchiverWithRetentionPolicyDirector.parse_config_file = (
        parse_config_file)

    def parse_config_file(obj, additional_configs):
        return {  # noqa
            'archiver_storage': {
                'cls': 'db',
                'args': {
                    'dbconn': swh_archiver_db,
                },
            },
            'retention_policy': 2,
            'archival_max_age': 3600,
            'storages': archiver_storages,
            'source': 'src',
            'sources': ['src'],
        }
    orig_worker_cfg = ArchiverWithRetentionPolicyWorker.parse_config_file
    ArchiverWithRetentionPolicyWorker.parse_config_file = (
        parse_config_file)

    # Create the base archiver
    archiver = ArchiverWithRetentionPolicyDirector(start_id=None)
    try:
        yield archiver, storages
    finally:
        ArchiverWithRetentionPolicyDirector.parse_config_file = (
            orig_director_cfg)
        ArchiverWithRetentionPolicyWorker.parse_config_file = (
            orig_worker_cfg)
        shutil.rmtree(src_root)
        shutil.rmtree(dest_root)


@pytest.fixture
def swh_archiver_storage(swh_archiver):

    log_root = tempfile.mkdtemp()

    config = {
        'cls': 'stub',
        'args': {
            'archives': {
                'present_archive': 'http://src:5003',
                'missing_archive': 'http://dest:5003',
            },
            'present': ['present_archive'],
            'missing': ['missing_archive'],
            'logfile_base': os.path.join(log_root, 'log_'),
        }
    }
    try:
        yield get_archiver_storage(**config)
    finally:
        shutil.rmtree(log_root)
