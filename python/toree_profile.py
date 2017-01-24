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
import json
import time

class Profile:
    """
    Abstract the handling of a toree slot providing access
    to configuration, process id, and any manipulations
    """
    PROCESS_FILE_NAME = "toree.pid"
    CONFIGURATION_FILE_NAME = "profile.json"

    profilePath = None

    def __init__(self, profilePath):
        self.profilePath = profilePath

    def pidLocation(self):
        """
        The location for the pid file
        :return: absolute path to pid file
        """
        return self.profilePath + '/' + self.PROCESS_FILE_NAME

    def configurationLocation(self):
        """
        The location for the profile.json configuration file
        :return: absolute path to the profile.json
        """
        return self.profilePath + '/' + self.CONFIGURATION_FILE_NAME

    def isAvailable(self):
        """
        Weather or not the Toree slot is available
        :return: true in case the slot is available (no pid file)
        """
        taken = os.path.exists(self.pidLocation())
        return not taken

    def reserve(self):
        """
        Reserve the slot profile by adding a pid file into it
        :return:
        """
        open(self.pidLocation(), 'a').close()

    def release(self):
        """
        Release the slot profile by removing the pid file from it
        :return:
        """
        if os.path.exists(self.pidLocation()):
            os.remove(self.pidLocation())

    def pid(self):
        """
        The Toree process id
        :return: the pid number or None
        """
        with open(self.pidLocation(), 'r') as pid_file:
            data = pid_file.read()
        return data

    def updatePid(self, pid):
        """
        Update the contents of the pid file
        :param pid: The pid value
        :return:
        """
        try:
            file = open(self.pidLocation(), 'w')
            file.write(pid)
        finally:
            file.close

    def config(self):
        """
        The parsed content of the profile.json
        :return:
        """
        with open(self.configurationLocation(), 'r') as data_file:
            return json.load(data_file)  #, object_hook=util._byteify



"""
p = Profile('/Users/lresende/opensource/jupyter/toree-gateway/src/main/resources/profiles/kernel-1')
print(p.pidLocation())
print(p.configurationLocation())
print(p.isAvailable())
c = p.config()
print(c['stdin_port'])
p.reserve()
time.sleep(10)
p.release()
"""

