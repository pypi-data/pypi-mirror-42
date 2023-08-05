#!/usr/bin/env python

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

"""
Osvmexpire worker server.
"""
from os_vm_expire.common import config
from os_vm_expire.queue import server
from os_vm_expire import version

import eventlet
import os
import sys

from oslo_log import log
from oslo_service import service

# Oslo messaging RPC server uses eventlet.
eventlet.monkey_patch()

# 'Borrowed' from the Glance project:
# If ../barbican/__init__.py exists, add ../ to Python search path, so that
# it will override what happens to be installed in /usr/(local/)lib/python...
possible_topdir = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]),
                                   os.pardir,
                                   os.pardir))
if os.path.exists(
        os.path.join(possible_topdir, 'os_vm_expire', '__init__.py')
):
    sys.path.insert(0, possible_topdir)


def fail(returncode, e):
    sys.stderr.write("ERROR: {0}\n".format(e))
    sys.exit(returncode)


def main():
    try:
        CONF = config.CONF
        CONF(sys.argv[1:], project='os-vm-expire',
             version=version.version_info.version_string)

        # Import and configure logging.
        log.setup(CONF, 'osvmexpire')
        LOG = log.getLogger(__name__)
        LOG.debug("Booting up os-vm-expire worker node...")

        service.launch(
            CONF,
            server.TaskServer(),
            workers=CONF.queue.asynchronous_workers
        ).wait()
    except RuntimeError as e:
        fail(1, e)


if __name__ == '__main__':
    main()
