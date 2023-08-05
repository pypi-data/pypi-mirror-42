# Copyright (C) 2015-2019  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import datetime
from contextlib import contextmanager
import pytest

from swh.archiver import ArchiverWithRetentionPolicyWorker
from swh.archiver.db import utcnow
from swh.objstorage.exc import ObjNotFoundError


def add_content(cursor, storage, content_data):
    """ Add really a content to the given objstorage

    This put an empty status for the added content.

    Args:
        storage_name: the concerned storage
        content_data: the data to insert
        with_row_insert: to insert a row entry in the db or not

    """
    # Add the content to the storage
    obj_id = storage.add(content_data)
    cursor.execute(""" INSERT INTO content (sha1)
                       VALUES (%s)
                       """, (obj_id,))
    return obj_id


def update_status(cursor, archiver, obj_id, storage_name, status, date=None):
    """ Update the db status for the given id/storage_name.

    This does not create the content in the storage.
    """
    cursor.execute("""insert into archive (name)
                      values (%s)
                      on conflict do nothing""", (storage_name,))

    archiver.archiver_storage.content_archive_update(
        obj_id, storage_name, status
    )


# Integration test
def test_archive_missing_content(swh_archiver_db, swh_archiver):
    """ Run archiver on a missing content should archive it.
    """
    archiver, storages = swh_archiver
    cursor = swh_archiver_db.cursor()
    obj_data = b'archive_missing_content'
    obj_id = add_content(cursor, storages['src'], obj_data)

    update_status(cursor, archiver, obj_id, 'src', 'present')
    # Content is missing on dest (entry not present in the db)
    with pytest.raises(ObjNotFoundError):
        storages['dest'].get(obj_id)

    archiver.run()
    # now the content should be present on remote objstorage
    remote_data = storages['dest'].get(obj_id)
    assert obj_data == remote_data


def test_archive_present_content(swh_archiver_db, swh_archiver):
    """ A content that is not 'missing' shouldn't be archived.
    """
    archiver, storages = swh_archiver
    cursor = swh_archiver_db.cursor()
    obj_data = b'archive_present_content'
    obj_id = add_content(cursor, storages['src'], obj_data)

    update_status(cursor, archiver, obj_id, 'src', 'present')
    update_status(cursor, archiver, obj_id, 'dest', 'present')

    # After the run, the content should NOT be in the archive.
    # As the archiver believe it was already in.
    archiver.run()
    with pytest.raises(ObjNotFoundError):
        storages['dest'].get(obj_id)


@contextmanager
def override_config(obj, **kw):
    orig = obj.config.copy()
    obj.config.update(kw)
    try:
        yield
    finally:
        obj.config = orig


def test_archive_already_enough(swh_archiver_db, swh_archiver):
    """ A content missing with enough copies shouldn't be archived.
    """
    archiver, storages = swh_archiver
    cursor = swh_archiver_db.cursor()
    obj_data = b'archive_alread_enough'
    obj_id = add_content(cursor, storages['src'], obj_data)

    update_status(cursor, archiver, obj_id, 'src', 'present')

    with override_config(archiver, retention_policy=1):
        # Obj is present in only one archive but only one copy is required.
        archiver.run()
    with pytest.raises(ObjNotFoundError):
        storages['dest'].get(obj_id)


def test_content_archive_get_copies(swh_archiver_db, swh_archiver):
    archiver, storages = swh_archiver
    assert not list(archiver.archiver_storage.content_archive_get_copies())

    cursor = swh_archiver_db.cursor()
    obj_id = add_content(cursor, storages['src'], b'archive_alread_enough')
    update_status(cursor, archiver, obj_id, 'src', 'present')
    assert list(archiver.archiver_storage.content_archive_get_copies()) == \
        [(obj_id, ['src'], {})]


# Unit tests for archive worker

def create_worker(batch={}):
    return ArchiverWithRetentionPolicyWorker(batch)


def archival_elapsed(mtime):
    return create_worker()._is_archival_delay_elapsed(mtime)


def test_vstatus_ongoing_remaining(swh_archiver):
    assert not archival_elapsed(utcnow())


def test_vstatus_ongoing_elapsed(swh_archiver):
    past_time = (utcnow()
                 - datetime.timedelta(
                     seconds=create_worker().archival_max_age))
    assert archival_elapsed(past_time)


def test_need_archival_missing(swh_archiver):
    """ A content should need archival when it is missing.
    """
    status_copies = {'present': ['uffizi'], 'missing': ['banco']}
    worker = create_worker()
    assert worker.need_archival(status_copies) is True


def test_need_archival_present(swh_archiver):
    """ A content present everywhere shouldn't need archival
    """
    status_copies = {'present': ['uffizi', 'banco']}
    worker = create_worker()
    assert worker.need_archival(status_copies) is False


def compute_copies_status(cursor, archiver, storage, status):
    """ A content with a given status should be detected correctly
    """
    obj_id = add_content(
        cursor, storage, b'compute_copies_' + bytes(status, 'utf8'))
    update_status(cursor, archiver, obj_id, 'dest', status)
    worker = create_worker()
    assert 'dest' in worker.compute_copies(
        set(worker.objstorages), obj_id)[status]


def test_compute_copies_present(swh_archiver, swh_archiver_db):
    """ A present content should be detected with correct status
    """
    archiver, storages = swh_archiver
    cursor = swh_archiver_db.cursor()
    compute_copies_status(cursor, archiver, storages['dest'], 'present')


def test_compute_copies_missing(swh_archiver, swh_archiver_db):
    """ A missing content should be detected with correct status
    """
    archiver, storages = swh_archiver
    cursor = swh_archiver_db.cursor()
    compute_copies_status(cursor, archiver, storages['dest'], 'missing')


def test_compute_copies_extra_archive(swh_archiver, swh_archiver_db):
    archiver, storages = swh_archiver
    cursor = swh_archiver_db.cursor()
    obj_id = add_content(cursor, storages['dest'], b'foobar')
    update_status(cursor, archiver, obj_id, 'dest', 'present')
    update_status(cursor, archiver, obj_id, 'random_archive', 'present')
    worker = create_worker()
    copies = worker.compute_copies(set(worker.objstorages), obj_id)
    assert copies['present'] == {'dest'}
    assert copies['missing'] == {'src'}


def get_backups(present=(), missing=()):
    """ Return a list of the pair src/dest from the present and missing
    """
    worker = create_worker()
    return list(worker.choose_backup_servers(present, missing))


def test_choose_backup_servers(swh_archiver, swh_archiver_db):
    assert len(get_backups(['src', 'dest'])) == 0
    assert len(get_backups(['src'], ['dest'])) == 1
    # Even with more possible destinations, do not take more than the
    # retention_policy require
    assert len(get_backups(['src'], ['dest', 's3'])) == 1
