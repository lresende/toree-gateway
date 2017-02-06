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
import signal
import sys
import time
import io

from os import O_NONBLOCK, read
from fcntl import fcntl, F_GETFL, F_SETFL
from  subprocess import Popen, PIPE
from metakernel import MetaKernel
from py4j.java_gateway import JavaGateway, GatewayParameters, CallbackServerParameters, java_import
from py4j.protocol import Py4JError

from config import *
from lifecycle import *
from toree_profile import *

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
    implementation_version = '1.0'
    langauge = 'scala'
    language_version = '2.11'
    banner = "toree_gateway_kernel"
    language_info = {'name': 'scala',
                     'mimetype': 'application/scala',
                     'file_extension': '.scala'}

    configManager = None
    toreeLifecycleManager = None
    toreeProfile = None

    gateway_proc = None
    gateway = None

    def __init__(self, **kwargs):
        super(ToreeGatewayKernel, self).__init__(**kwargs)
        """Help on error logging"""
        """
        sys.stdout = open(os.environ["TOREE_GATEWAY_HOME"] + '/logs/toree_gateway_out.log', 'w')
        sys.sterr = open(os.environ["TOREE_GATEWAY_HOME"] + '/logs/toree_gateway_err.log', 'w')
        """
        """"""
        try:
            print('Starting Toree Gateway Kernel Initialization')
            self.configManager = ConfigManager()
            self.toreeLifecycleManager = LifecycleManager()
            self._start_toree()
            # pause, to give time to Toree to start at the backend
            time.sleep(5)
            # start toree client and connect to backend
            self._start_toree_client()
        except Exception as e:
            print('__init__: Error initializing Toree Gateway Kernel')
            print(format(e))
            """
            if self.toreeProfile:
                self.toreeProfile.release()
                self.toreeProfile = None
            """

    def sig_handler(signum, frame):
        self.gateway_proc.terminate()
        self._stop_toree()

    def do_shutdown(self, restart):
        super(ToreeGatewayKernel, self).do_shutdown(restart)
        self.gateway_proc.terminate()
        self._stop_toree()

    def _start_toree(self):
        self.toreeProfile = self.toreeLifecycleManager.start_toree()

    def _stop_toree(self):
        self.toreeLifecycleManager.stop_toree(self.toreeProfile)
        self.toreeProfile = None

    def _start_toree_client(self):
        if self.toreeProfile is None:
            print('_start_toree_client: Could not find a Toree slot to use')
            return '_start_toree_client: Could not find a Toree slot to use'
        if len(self.toreeProfile.pid()) == 0:
            print('_start_toree_client: Invalid Toree PID')
            return '_start_toree_client: Invalid Toree PID'

        args = [
            "java",
            "-classpath",
            os.environ["TOREE_GATEWAY_HOME"] + "/lib/toree-gateway-1.0-jar-with-dependencies.jar",
            "org.apache.toree.gateway.ToreeGatewayClient",
            "--profile",
            self.toreeProfile.configurationLocation()
        ]

        print('_start_toree_client: Will start py4j server')
        self.gateway_proc = Popen(args, stderr=PIPE, stdout=PIPE)
        time.sleep(5)

        config = self.toreeProfile.config()
        print('Creating py4j gateway using port:{} and {} '.format(config['py4j_java'], config['py4j_python']))

        self.gateway = JavaGateway(
            gateway_parameters=GatewayParameters(port=config['py4j_java']),
            start_callback_server=True,
            callback_server_parameters=CallbackServerParameters(port=config['py4j_python']))

        #flags = fcntl(self.gateway_proc.stdout, fcntl.F_GETFL) # get current p.stdout flags
        #fcntl(self.gateway_proc.stdout, fcntl.F_SETFL, flags | os.O_NONBLOCK)

        #flags = fcntl(self.gateway_proc.stderr, fcntl.F_GETFL) # get current p.stdout flags
        #fcntl(self.gateway_proc.stderr, fcntl.F_SETFL, flags | os.O_NONBLOCK)

        signal.signal(signal.SIGTERM, self.sig_handler)
        signal.signal(signal.SIGINT, self.sig_handler)
        signal.signal(signal.SIGHUP, self.sig_handler)


    def Error(self, output):
        if not output:
            return

        super(ToreeGatewayKernel, self).Error(output)

    """
    def handle_output(self, fd, fn):
        stringIO = io.StringIO()
        while True:
            try:
                b = read(fd.fileno(), 1024)
                if b:
                    stringIO.write(b.decode('utf-8'))
            except OSError:
                break

        s = stringIO.getvalue()
        if s:
            fn(s.strip())

        stringIO.close()
    """

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
            print('do_execute_direct: Not connected to a Toree instance')
            return 'Notebook is offline, due to no resources available on the server. Please try again later or contact an Administrator'

        if not code.strip():
            return None

        retval = None
        try:
            retval = self.gateway.entry_point.eval(code.rstrip())
            """
            This would process stdin and stdout, which would generate
            garbage on the ui with any log or other related content
            on these streams. For now, disabling it, very useful for
            debuging purposes.

            self.handle_output(self.gateway_proc.stdout, self.Print)
            self.handle_output(self.gateway_proc.stderr, self.Error)
            """
        except Py4JError as e:
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

