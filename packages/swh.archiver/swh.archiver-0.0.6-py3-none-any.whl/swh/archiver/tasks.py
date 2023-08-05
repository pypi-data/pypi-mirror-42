# Copyright (C) 2015-2016  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from celery import current_app as app

from .worker import ArchiverWithRetentionPolicyWorker
from .worker import ArchiverToBackendWorker


@app.task(name=__name__ + '.SWHArchiverWithRetentionPolicyTask')
def archive_with_retention(*args, **kwargs):
    ArchiverWithRetentionPolicyWorker(*args, **kwargs).run()


@app.task(name=__name__ + '.SWHArchiverToBackendTask')
def archive_to_backend(*args, **kwargs):
    """Main task that archive a batch of content in the cloud.
    """
    ArchiverToBackendWorker(*args, **kwargs).run()
