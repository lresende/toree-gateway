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


from yarn_api_client import ResourceManager

from util import debug_print, debug_pprint
from config import *
from security import decode_password
from pprint import pprint

class YarnToreeManager:

    def start_toree(self, profile):
        """
        Connect to a remote system via SSH and
        start an instance of Toree
        :param profile: The Toree slot to read profile.json
        configuration file
        :return: None
        """
        debug_print('__start_toree__')

    def stop_toree(self, profile):
        """
        Connect to a remote system via SSH and
        stop the associated Toree instance based on the
        process id information stored in toree.pid
        :param profile: The Toree slot to read toree.pid
        configuration file
        :return: None
        """
        debug_print('__stop_toree__')



manager = ResourceManager(address='9.30.109.149', port=8443, api_endpoint='/gateway/default/resourcemanager/v1', username='guest', password='guest-password')

info = manager.cluster_information()
#pprint(vars(info))
pprint(info.data['clusterInfo']['id'])
#pprint(info.data.clusterInfo.id)
#pprint(info[data].clusterInfo.hadoopVersion)