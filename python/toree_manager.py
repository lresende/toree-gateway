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


import paramiko
from paramiko import SSHClient, SSHException
from socket import *

from util import debug_print, debug_pprint
from config import *

class ToreeManager:
    """
    A Helper class that enables connecting to a remote machine
    via SSH and properly start/stop Toree instances
    """
    configManager = None

    def __init__(self):
        self.configManager = ConfigManager()

    def _getSSHClient(self):
        """
        Configure and initialize a SSH client
        :return: a configured SSH client
        """
        client = SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        debug_print('Connecting to remote system to start Toree : %s ' % self.configManager.get('toree.ip'))

        if len(self.configManager.get('toree.password')) > 0:
            # Connect passing user credentials
            client.connect( \
                self.configManager.get('toree.ip'), \
                username=self.configManager.get('toree.username'), \
                password=self.configManager.get('toree.password'))
        else:
            # Connect with ssh passwordless
            client.connect( \
                self.configManager.get('toree.ip'), \
                username=self.configManager.get('toree.username'))


        return client

    def _getSSHChannel(self, client):
        """
        Configure and initialize a new SSH session on the client
        :param client: The client to initialize the session
        :return: the new SSH session
        """
        channel = client.invoke_shell()
        channel.settimeout(20)
        channel.set_combine_stderr(True)

        return channel

    def start_toree(self, profile):
        """
        Connect to a remote system via SSH and
        start an instance of Toree
        :param profile: The Toree slot to read profile.json
        configuration file
        :return: None
        """
        try:
            client = self._getSSHClient()
            channel = self._getSSHChannel(client)

            channel = client.invoke_shell()
            channel.settimeout(30)
            channel.set_combine_stderr(True)

            stdin = channel.makefile('w')
            stdout = channel.makefile('r')
            stderr = channel.makefile_stderr('r')

            config = profile.config()
            command = '''
            cd {} &&
            . startrun.sh --ip {} --stdin-port {} --control-port {} --shell-port {} --iopub-port {} --heartbeat-port {} &&
            exit
            '''.format( \
                self.configManager.get('toree.home') + "/bin", \
                config['ip'], \
                config['stdin_port'], \
                config['control_port'], \
                config['shell_port'], \
                config['iopub_port'], \
                config['hb_port'])

            debug_print('Executing the following command to start Toree: \n %s' % command)

            stdin.write(command)

            pid = None
            for line in stdout:
                pid = line.strip()

            debug_print('Toree started with pid: %s ' % pid)

            profile.updatePid(pid)

        except SSHException as e:
            debug_pprint(e)
        except timeout:
            debug_print('caught a timeout')
        finally:
            debug_print('closing connection')
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
            debug_print('all closed')

    def stop_toree(self, profile):
        """
        Connect to a remote system via SSH and
        stop the associated Toree instance based on the
        process id information stored in toree.pid
        :param profile: The Toree slot to read toree.pid
        configuration file
        :return: None
        """
        try:
            client = self._getSSHClient()
            channel = self._getSSHChannel(client)

            stdin = channel.makefile('w')
            stdout = channel.makefile('r')
            stderr = channel.makefile_stderr('r')

            command = '''
            kill -9 {} &&
            exit
            '''.format(profile.pid())

            debug_print(command)

            stdin.write(command)

            debug_print(stdout.read())

        except timeout:
            debug_print('caught a timeout')
        finally:
            debug_print('closing connection')
            if stdout:
                stdout.close()
            if channel:
                channel.close()
            if client:
                client.close()
            debug_print('all closed')


"""
p = Profile('/Users/lresende/opensource/jupyter/toree-gateway/src/main/resources/profiles/kernel-1')
t = ToreeManager()

t.start_toree(p)
t.stop_toree(p)
"""