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
import logging

from os import O_NONBLOCK, read
from fcntl import fcntl, F_GETFL, F_SETFL
from  subprocess import Popen, PIPE
from metakernel import MetaKernel
from py4j.java_gateway import JavaGateway, CallbackServerParameters, java_import
from py4j.protocol import Py4JError

class TextOutput(object):
    """Wrapper for text output whose repr is the text itself.
       This avoids `repr(output)` adding quotation marks around already-rendered text.
    """
    def __init__(self, output):
        self.output = output

    def __repr__(self):
        return self.output

class ToreeKernel(MetaKernel):
    implementation = 'toree_gateway_kernel'
    implementation_version = '1.0'
    langauge = 'scala'
    language_version = '2.11'
    banner = "toree_gateway_kernel"
    language_info = {'name': 'scala',
                     'mimetype': 'application/scala',
                     'file_extension': '.scala'}


    def __init__(self, **kwargs):
        super(ToreeKernel, self).__init__(**kwargs)
        self._start_toree_client()

    def sig_handler(signum, frame):
        self.gateway_proc.terminate()

    def do_shutdown(self, restart):
        super(ToreeKernel, self).do_shutdown(restart)
        self.gateway_proc.terminate()

    def _start_toree_client(self):
        args = [
            "java",
            "-classpath",
            "/opt/toree-gateway/lib/toree-gateway-1.0-jar-with-dependencies.jar",
            "org.apache.toree.gateway.ToreeGatewayClient"
        ]

        self.gateway_proc = Popen(args, stderr=PIPE, stdout=PIPE)
        time.sleep(1.5)
        self.gateway = JavaGateway(
            start_callback_server=True,
            callback_server_parameters=CallbackServerParameters())

        flags = fcntl(self.gateway_proc.stdout, F_GETFL) # get current p.stdout flags
        fcntl(self.gateway_proc.stdout, F_SETFL, flags | O_NONBLOCK)

        flags = fcntl(self.gateway_proc.stderr, F_GETFL) # get current p.stdout flags
        fcntl(self.gateway_proc.stderr, F_SETFL, flags | O_NONBLOCK)

        signal.signal(signal.SIGTERM, self.sig_handler)
        signal.signal(signal.SIGINT, self.sig_handler)
        signal.signal(signal.SIGHUP, self.sig_handler)


    def Error(self, output):
        if not output:
            return

        super(ToreeKernel, self).Error(output)

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
    ToreeKernel.run_as_main()

