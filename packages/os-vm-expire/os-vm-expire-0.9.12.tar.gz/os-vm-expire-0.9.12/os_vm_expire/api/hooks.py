# Copyright (c) 2015 Rackspace, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pecan
import webob

from oslo_serialization import jsonutils

from os_vm_expire.model import repositories


class JSONErrorHook(pecan.hooks.PecanHook):
    def on_error(self, state, exc):
        if isinstance(exc, webob.exc.HTTPError):
            exc.body = jsonutils.dump_as_bytes({
                'code': exc.status_int,
                'title': exc.title,
                'description': exc.detail
            })
            state.response.content_type = "application/json"
            return exc.body


class OSVmExpireTransactionHook(pecan.hooks.TransactionHook):
    """Custom hook for Barbican transactions."""
    def __init__(self):
        super(OSVmExpireTransactionHook, self).__init__(
            start=repositories.start,
            start_ro=repositories.start_read_only,
            commit=repositories.commit,
            rollback=repositories.rollback,
            clear=repositories.clear
        )
