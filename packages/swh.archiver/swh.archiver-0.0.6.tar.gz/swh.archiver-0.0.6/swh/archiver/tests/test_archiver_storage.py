# Copyright (C) 2015-2019  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import pytest
from glob import glob


# Generated with:
#
# id_length = 20
# random.getrandbits(8 * id_length).to_bytes(id_length, 'big')
#
content_ids = [
    b"\xc7\xc9\x8dlk!'k\x81+\xa9\xc1lg\xc2\xcbG\r`f",
    b'S\x03:\xc9\xd0\xa7\xf2\xcc\x8f\x86v$0\x8ccq\\\xe3\xec\x9d',
    b'\xca\x1a\x84\xcbi\xd6co\x14\x08\\8\x9e\xc8\xc2|\xd0XS\x83',
    b'O\xa9\xce(\xb4\x95_&\xd2\xa2e\x0c\x87\x8fw\xd0\xdfHL\xb2',
    b'\xaaa \xd1vB\x15\xbd\xf2\xf0 \xd7\xc4_\xf4\xb9\x8a;\xb4\xcc',
]


def test_archive_ls(swh_archiver_storage):
    assert dict(swh_archiver_storage.archive_ls()) == {
        'present_archive': 'http://src:5003',
        'missing_archive': 'http://dest:5003'}


def test_content_archive_get(swh_archiver_storage):
    for content_id in content_ids:
        assert swh_archiver_storage.content_archive_get(content_id) == \
            (content_id, {'present_archive'}, {})


def test_content_archive_get_copies(swh_archiver_storage):
    assert list(swh_archiver_storage.content_archive_get_copies()) == []


def test_content_archive_get_unarchived_copies(swh_archiver_storage):
    retention_policy = 2
    assert list(swh_archiver_storage.content_archive_get_unarchived_copies(
            retention_policy)) == []


def test_content_archive_get_missing(swh_archiver_storage):
    assert list(swh_archiver_storage.content_archive_get_missing(
        content_ids, 'missing_archive')) == content_ids

    assert list(swh_archiver_storage.content_archive_get_missing(
        content_ids, 'present_archive')) == []

    with pytest.raises(ValueError):
        list(swh_archiver_storage.content_archive_get_missing(
            content_ids, 'unknown_archive'))


def test_content_archive_get_unknown(swh_archiver_storage):
    assert list(swh_archiver_storage.content_archive_get_unknown(
            content_ids)) == []


def test_content_archive_update(swh_archiver_storage):
    for content_id in content_ids:
        swh_archiver_storage.content_archive_update(
            content_id, 'present_archive', 'present')
        swh_archiver_storage.content_archive_update(
            content_id, 'missing_archive', 'present')

    swh_archiver_storage.close_logfile()

    # Make sure we created a logfile
    logfile_base = swh_archiver_storage.logfile_base
    files = glob('%s*' % logfile_base)
    assert len(files) == 1

    # make sure the logfile contains all our lines
    lines = open(files[0]).readlines()
    assert len(lines) == (2 * len(content_ids))
