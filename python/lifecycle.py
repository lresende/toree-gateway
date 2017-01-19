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
import time

from config import *
from toree_manager import *

class LifecycleManager:
    configManager = None
    toreeManager = None

    def __init__(self):
        self.configManager = ConfigManager()
        self.toreeManager = ToreeManager()

    def _reserve_profile(self):
        """
        Tries to reserv a profile configuration to access Toree
        :return: the reserved profile folder location, or None
        """
        profilesFolder = self.configManager.getProfilesFolder()
        profile = None
        """Lock mutext to avoid two processes to select same kernel config"""
        # mutex = open(self.configManager.getProfilesFolder() + "/mutex")
        # lock = fcntl.flock(mutex, fcntl.LOCK_EX)
        # print(lock)
        """Select from the available kernel configurations"""
        for (path, dirs, files) in os.walk(profilesFolder):
            for folderName in dirs:
                profile = Profile(profilesFolder + '/' + folderName)
                if profile.isAvailable():
                    profile.reserve()
                    break
        """Unlock the mutex enabling other processes to select same kernel config"""
        # fcntl.flock(self.mutex, fcntl.LOCK_UN)

        return profile

    def _release_profile(self, profile):
        profile.release()

    def start_toree(self):
        """
        Reserve a profile to use, and start a remote Toree instance with that configuration
        :return: the path to the configuration file (profile.json) to use when connecting
        """
        profile = self._reserve_profile()
        if profile is None:
            raise RuntimeError('No server resources available.')
        self.toreeManager.start_toree(profile)

        return profile

    def stop_toree(self, profile):
        self.toreeManager.stop_toree(profile)
        self._release_profile(profile)


"""
manager = LifecycleManager()
print('Starting first toree kernel')
p1 = manager.start_toree()
print(p1.profilePath)
print('Starting second toree kernel')
time.sleep(15)
#p2 = manager.start_toree()
#print p2.profilePath
#print'Stopping toree kernels'
manager.stop_toree(p1)
#manager.stop_toree(p2)
print('finished')
"""
