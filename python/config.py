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
    """
    Simple configuration manager

    This expects TOREE_GATEWAY_HOME environment variable
    to be set and will look for the config file in
    TOREE_GATEWAY_HOME/conf/toree-gateway.properties

    In dev environment, it will fallback to reading
    the config file
    """
    config = configparser.RawConfigParser()
    homePath = None
    configPath = None
    profilesPath = None

    def __init__(self):
        if os.environ["TOREE_GATEWAY_HOME"]:
            self.homePath = os.environ["TOREE_GATEWAY_HOME"]
            self.configPath = os.environ["TOREE_GATEWAY_HOME"] + '/conf'
            self.profilesPath = os.environ["TOREE_GATEWAY_HOME"] + '/profiles'
        else:
            self.homePath = os.getcwd()[:-7]
            self.configPath = self.homePath + '/conf'
            self.profilesPath = self.homePath + '/profiles'

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


    def has_key(self, key):
        """
        if the given key existis, return True otherwise False
        :param key: the configuration key
        :return:
        """
        return self.config.has_option('general', key)

    def get(self, key):
        """
        Return a configuration from general section
        :param key: the configuration key
        :return:
        """
        return self.config.get('general', key)

    def get_as_int(self, key, default=0):
        """
        return a configuration from general section as integer
        :param key: the configuration key
        :return:
        """
        if self.has_key(key):
            return int(self.get(key))
        else:
            return default

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
print( c.getHomeFolder() )
print( c.getConfigurationFolder() )
print( c.getProfilesFolder() )
print( c.get_as_int('toree.excution.timeout') )
print( c.get_as_int('toree.excution.timeout', 70) )
print( c.get_as_int('toree.invalid', 50) )
"""