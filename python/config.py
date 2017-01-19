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
import configparser

class ConfigManager:
    config = configparser.RawConfigParser()
    homePath = os.getcwd()[:-7]
    configPath = None
    profilesPath = None

    def __init__(self):
        if os.environ["TOREE_GATEWAY_HOME"]:
            self.configPath = os.environ["TOREE_GATEWAY_HOME"] + '/conf'
            self.profilesPath = os.environ["TOREE_GATEWAY_HOME"] + '/profiles'
        else:
            self.configPath = self.homePath + '/src/main/resources/'
            self.profilesPath = self.homePath + '/src/main/resources/profiles'

        self.config.read(self.configPath + '/toree-gateway.properties')

    def getHomeFolder(self):
        """
        Return home folder based on where app is running
        :return:
        """
        return self.homePath

    def getConfigurationFolder(self):
        """
        Return the location where configuration file is being read
        :return:
        """
        return self.configPath

    def getProfilesFolder(self):
        """
        Return the location where profiles information are is being read
        :return:
        """
        return self.profilesPath


    def get(self, key):
        """
        Return a configuration from gegeral section
        :param key: the configuration key
        :return:
        """
        return self.config.get('general', key)

    def getBySection(self, section, key):
        """
        Return a configuration from a specific section and key
        :param section: the configuration section
        :param key: the configuration key
        :return:
        """
        return self.config.get(section, key)


"""
c = ConfigManager()
print c.getHomeFolder()
print c.getConfigurationFolder()
print c.getProfilesFolder()
"""