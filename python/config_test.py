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
import unittest
import configparser
from config import *

class TestConfigManager(unittest.TestCase):

    def setUp(self):
        parser = configparser.ConfigParser()
        parser.read_dict({'general': {'key1': 'value1', "key2": 2}})

        self.config_manager = ConfigManager(config_parser=parser)
        self.home = os.environ["TOREE_GATEWAY_HOME"]


    def test_home(self):
        self.assertEqual(self.config_manager.getHomeFolder(), self.home, 'Default home folder should be running folder')

    def test_conf_is_relative_to_home(self):
        self.assertEqual(self.config_manager.getConfigurationFolder(), self.home +'/conf', 'Default home folder should be running folder')

    def test_profiles_is_relative_to_home(self):
        self.assertEqual(self.config_manager.getProfilesFolder(), self.home +'/profiles', 'Default home folder should be running folder')

    def test_retrieve_value(self):
        self.assertEqual(self.config_manager.get('key1'), 'value1', 'Can not retrieve value for key')

    def test_retrieve_value_as_int(self):
        self.assertEqual(self.config_manager.get_as_int('key2'), 2, 'Can not retrieve value as int for key')

    def test_retrieve_default_value_when_key_does_not_exist(self):
        self.assertEqual(self.config_manager.get('invalid_key','some_value'), 'some_value', 'Can not retrieve default value for key')

    def test_retrieve_default_value__as_int_when_key_does_not_exist(self):
        self.assertEqual(self.config_manager.get_as_int('invalid_key', 2), 2, 'Can not retrieve default value as int for key')

    def test_has_key_return_true_for_valid_key(self):
        self.assertEqual(self.config_manager.has_key('key1'), True, 'hasKey should return True for valid keys')

    def test_has_key_return_false_for_invalid_key(self):
        self.assertEqual(self.config_manager.has_key('invalid_key'), False, 'hasKey should return False for invalid keys')

    def test_none_is_returned_for_invalid_key(self):
        self.assertEqual(self.config_manager.get('invalid_key'), None, 'Invalid key should return None')


if __name__ == "__main__":
    unittest.main()