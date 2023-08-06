# -*- coding: utf-8 -*-
"""replay module"""

__license__ = """
    Copyright (C) 2018  fjord-technologies

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA..
"""

import copy
import logging
import time
import uuid

from dwho.classes.modules import DWhoModuleBase, MODULES
from fd_replay.classes.plugins import FdReplayEPTObject, EPTS_SYNC
from httpdis.httpdis import HttpReqError, HttpResponse
from sonicprobe.libs.moresynchro import RWLock

LOG = logging.getLogger('fd-replay.modules.replay')


class ReplayModule(DWhoModuleBase):
    MODULE_NAME = 'replay'

    LOCK        = RWLock()

    def safe_init(self, options):
        self.results      = {}
        self.lock_timeout = self.config['general']['lock_timeout']

    def _set_result(self, obj):
        self.results[obj.get_uid()] = obj

    def _get_result(self, uid):
        r = {'error':  None,
             'result': None}

        while True:
            if uid not in self.results:
                time.sleep(0.1)
                continue

            res = self.results.pop(uid)
            if res.has_error():
                r['error'] = res.get_errors()
                LOG.error("failed on call: %r. (errors: %r)", res.get_uid(), r['error'])
            else:
                r['result'] = res.get_result()
                LOG.info("successful on call: %r", res.get_uid())
                LOG.debug("result on call: %r", r['result'])

            return r

    def _push_epts_sync(self, method, request, endpoint = None):
        if endpoint:
            if endpoint not in EPTS_SYNC:
                raise HttpReqError(404, "unable to find endpoint: %r" % endpoint)
            else:
                epts = {endpoint: EPTS_SYNC[endpoint]}
        else:
            epts = EPTS_SYNC

        for endpoint, ept_sync in epts.iteritems():
            uid = "%s:%s" % (ept_sync.name, uuid.uuid4())
            ept_sync.qput(FdReplayEPTObject(ept_sync.name,
                                            uid,
                                            endpoint,
                                            method,
                                            request))
        return uid

    def index(self, request):
        if not self.LOCK.acquire_read(self.lock_timeout):
            raise HttpReqError(503, "unable to take LOCK for reading after %s seconds" % self.lock_timeout)

        try:
            self._push_epts_sync('replay', copy.copy(request))

            return HttpResponse()
        except HttpReqError, e:
            raise
        except Exception, e:
            LOG.exception("%r", e)
        finally:
            self.LOCK.release()


if __name__ != "__main__":
    def _start():
        MODULES.register(ReplayModule())
    _start()
