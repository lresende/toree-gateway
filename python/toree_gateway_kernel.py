#
# (C) Copyright IBM Corp. 2017
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import sys
import time

from metakernel import MetaKernel

from config import *
from lifecycle import *
from toree_client import *
from toree_profile import *
from util import debug_print, debug_pprint

class TextOutput(object):
    """Wrapper for text output whose repr is the text itself.
       This avoids `repr(output)` adding quotation marks around already-rendered text.
    """
    def __init__(self, output):
        self.output = output

    def __repr__(self):
        return self.output

class ToreeGatewayKernel(MetaKernel):
    implementation = 'toree_gateway_kernel'
    implementation_version = '2.0'
    langauge = 'scala'
    language_version = '2.11'
    banner = "toree_gateway_kernel"
    language_info = {'name': 'scala',
                     'mimetype': 'application/scala',
                     'file_extension': '.scala'}

    isReady = False
    executionTimeout = 30

    configManager = None
    toreeLifecycleManager = None
    toreeProfile = None
    toreeClient = None

    def __init__(self, **kwargs):
        super(ToreeGatewayKernel, self).__init__(**kwargs)
        self.configManager = ConfigManager()
        """Help on error logging"""
        if self.configManager.get('gateway.debug') == 'True':
            ts = str(time.time()).split('.')[0]
            sys.stdout = open(os.environ["TOREE_GATEWAY_HOME"] + '/logs/toree_gateway_out_' + ts + '.log', 'w')
            sys.sterr = open(os.environ["TOREE_GATEWAY_HOME"] + '/logs/toree_gateway_err_' + ts + '.log', 'w')
        """"""
        try:
            debug_print('Starting Toree Gateway Kernel Initialization')
            self.toreeLifecycleManager = LifecycleManager()
            self._start_toree()
            time.sleep(10)
            debug_print('Reserved profile:' + self.toreeProfile.configurationLocation())
            self.toreeClient = ToreeClient(self.toreeProfile.configurationLocation())
            self.executionTimeout = self.configManager.get_as_int('toree.excution.timeout', 30)
            debug_print('Execution timeout: %s' % self.executionTimeout)
            # pause, to give time to Toree to start at the backend
        except Exception as e:
            debug_print('__init__: Error initializing Toree Gateway Kernel')
            debug_print(format(e))
            """
            if self.toreeProfile:
                self.toreeProfile.release()
                self.toreeProfile = None
            """

    def sig_handler(signum, frame):
        self._stop_toree()

    def do_shutdown(self, restart):
        super(ToreeGatewayKernel, self).do_shutdown(restart)
        self._stop_toree()

    def _start_toree(self):
        self.toreeProfile = self.toreeLifecycleManager.start_toree()

    def _stop_toree(self):
        self.toreeLifecycleManager.stop_toree(self.toreeProfile)
        self.toreeProfile = None

    def Error(self, output):
        if not output:
            return

        super(ToreeGatewayKernel, self).Error(output)

    def do_execute_direct(self, code, silent=False):
        """
        :param code:
            The code to be executed.
        :param silent:
            Whether to display output.
        :return:
            Return value, or None

        MetaKernel code handler.
        """

        if self.toreeProfile is None:
            debug_print('do_execute_direct: Not connected to a Toree instance')
            return 'Notebook is offline, due to no resource availability on the server. Please try again later or contact an Administrator'

        if not self.toreeClient.is_alive():
            debug_print('do_execute_direct: Kernel client is not alive')
            return 'Not connected to a Kernel'

        if code is None or code.strip() is None:
            return None

        if not code.strip():
            return None

        if not self.isReady:
            retries = self.configManager.get_as_int('toree.initialization.retries', 3)
            retry_interval = self.configManager.get_as_int('toree.initialization.retry.interval', 5)

            debug_print('Trying to verify Toree has been initialized with options: retries %d times / retry interval %d seconds' % (retries, retry_interval))
            n = 1
            while n <= retries:
                debug_print('Trying to connect to remote Toree for %d time' % n)
                if self.toreeClient.is_ready():
                    self.isReady = True
                    break
                else:
                    time.sleep(retry_interval)

                n += 1

            if not self.isReady:
                return 'Kernel is not ready to process yet'

        debug_print('Evaluating: ' + code.strip())

        retval = None
        try:
            retval = self.toreeClient.eval(code.rstrip(), self.executionTimeout)
        except Exception as e:
            if not silent:
                self.Error(format(e))

        if retval is None:
            return
        elif isinstance(retval, str):
            return TextOutput(retval)
        else:
            return retval

if __name__ == '__main__':
    ToreeGatewayKernel.run_as_main()

