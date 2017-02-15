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

import time

from util import debug_print, debug_pprint
from jupyter_client import BlockingKernelClient
from pprint import pprint

try:
    from queue import Empty  # Python 3
except ImportError:
    from Queue import Empty  # Python 2

TIMEOUT = 30

class ToreeClient:
    def __init__(self, connectionFileLocation):
        self.client = BlockingKernelClient(connection_file=connectionFileLocation)
        self.client.load_connection_file(connection_file=connectionFileLocation)

    def is_alive(self):
        return self.client.is_alive()

    def is_ready(self):
        try:
            result = self.eval('1')
            if result == '1':
                return True
            else:
                return False
        except:
            return False

    def wait_for_ready(self, timeout=TIMEOUT):
        # Wait for initialization, by receiving an 'idle' message
        # Flush Shell channel

        abs_timeout = time.time() + timeout
        while True:
            try:
                msg = self.client.shell_channel.get_msg(block=True, timeout=0.2)
            except Empty:
                break

            # Check if current time is ready check time plus timeout
            if time.time() > abs_timeout:
                raise RuntimeError("Kernel didn't respond in %d seconds" % timeout)

        # Flush IOPub channel
        while True:
            try:
                msg = self.client.iopub_channel.get_msg(block=True, timeout=0.2)
            except Empty:
                break

            # Check if current time is ready check time plus timeout
            if time.time() > abs_timeout:
                raise RuntimeError("Kernel didn't respond in %d seconds" % timeout)


    def eval(self, code, timeout=TIMEOUT):

        if self.client.is_alive() == False:
            raise Exception('Problem connecting to remote kernel: Kernel is NOT alive')

        debug_print('-----------------------------------------')
        debug_print('Executing: ')
        debug_pprint(code)

        msg_id = self.client.execute(code=code, allow_stdin=False)
        debug_print('Message id for code execution:'  + msg_id)

        # now the kernel should be 'busy' with [parent_header][msg_id] being the current message
        busy_msg = self.client.iopub_channel.get_msg(timeout=1)
        debug_print('checking current kernel status')
        debug_print(busy_msg['parent_header']['msg_id'])
        debug_print(busy_msg['content']['execution_state'])
        debug_pprint(busy_msg)

        if busy_msg['content']['execution_state'] == 'busy':
            debug_print('busy_message')
        else:
            debug_print('error: not busy')

        reply = self.client.get_shell_msg(timeout=3)
        print('message reply')
        pprint(reply)

        results = []
        while True:
            msg = self.client.get_iopub_msg()
            debug_print('message')
            debug_pprint(msg)
            # validate that the responses are still related to current request
            if msg['parent_header']['msg_id'] != msg_id:
                debug_print('Ignoring messages related to ' + msg['parent_header']['msg_id'] + ' request')
                #raise Exception('Invalid message id received ' + msg['parent_header']['msg_id'] + '  expected ' + msg_id)

            # When idle, responses have all been processed/returned
            elif msg['msg_type'] == 'status':
                debug_print('current message status: ' + msg['msg_type'])
                if msg['content']['execution_state'] == 'idle':
                    break

            # validate execute_inputs are from current  code
            elif msg['msg_type'] == 'execute_input':
                debug_print('current message status: ' + msg['msg_type'])
                debug_print('current message content code: ' + msg['content']['code'])
                if msg['content']['code'] == code:
                    continue

            elif msg['msg_type'] == 'stream':
                results.append(msg['content']['text'])
                continue

            elif msg['msg_type'] == 'execute_result':
                results.append(msg['content']['data']['text/plain'])
                continue

        #return reply, output_msgs
        return ''.join(results)



"""
client = ToreeClient('/Users/lresende/opensource/jupyter/toree-gateway/profiles/profile.json')

print('is alive: %s' % client.is_alive())
print('is ready: %s' % client.is_ready())

command = '''print(1+1)\nprint(2+2)\n3'''
pprint(client.eval(command))

command = '''print(1/0)'''
pprint(client.eval(command))

#result = client.eval(command)
#print('Result: ' + pprint(result))
"""