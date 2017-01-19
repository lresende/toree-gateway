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
import os.path
import fcntl
import time
import json
import datetime

import base64
import paramiko
from paramiko import SSHClient, SSHException
from pprint import pprint
from socket import *

from toree_profile import *
from config import *

class ToreeManager:
    configManager = None

    def __init__(self):
        self.configManager = ConfigManager()

    def getSSHClient(self):
        client = SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect( \
            self.configManager.get('toree.ip'), \
            username=self.configManager.get('toree.username'), \
            password=self.configManager.get('toree.password'))

        #print('Client connected successfuly')

        return client

    def getSSHChannel(self, client):
        channel = client.invoke_shell()
        channel.settimeout(20)
        channel.set_combine_stderr(True)

        return channel

    def start_toree(self, profile):
        try:
            client = self.getSSHClient()
            channel = self.getSSHChannel(client)

            channel = client.invoke_shell()
            channel.settimeout(30)
            channel.set_combine_stderr(True)

            stdin = channel.makefile('w')
            stdout = channel.makefile('r')
            stderr = channel.makefile_stderr('r')

            config = profile.config()
            command = '''
            cd {} &&
            . tkarra.sh --ip {} --stdin-port {} --control-port {} --shell-port {} --iopub-port {} --heartbeat-port {} &&
            exit
            '''.format( \
                self.configManager.get('toree.home') + "/bin", \
                config['ip'], \
                config['stdin_port'], \
                config['control_port'], \
                config['shell_port'], \
                config['iopub_port'], \
                config['hb_port'])


            #print(command)

            stdin.write(command)

            pid = None
            for line in stdout:
                pid = line.strip()

            profile.updatePid(pid)

        except SSHException as e:
            pprint(e)
        except timeout:
            print('caught a timeout')
        finally:
            print('closing connection')
            if stderr:
                stderr.close()
            if stdout:
                stdout.close()
            if stdin:
                stdin.close()
            if channel:
                channel.close()
            if client:
                client.close()
            print('all closed')

    def stop_toree(self, profile):
        try:
            client = self.getSSHClient()
            channel = self.getSSHChannel(client)

            stdin = channel.makefile('w')
            stdout = channel.makefile('r')
            stderr = channel.makefile_stderr('r')

            command = '''
            kill -9 {}
            '''.format(profile.pid())

            print(command)

            stdin.write(command)

        except timeout:
            print('caught a timeout')
        finally:
            print('closing connection')
            if stdout:
                stdout.close()
            if channel:
                channel.close()
            if client:
                client.close()
            print('all closed')


"""
p = Profile('/Users/lresende/opensource/jupyter/toree-gateway/src/main/resources/profiles/kernel-1')
t = ToreeManager()

t.start_toree(p)
t.stop_toree(p)
"""