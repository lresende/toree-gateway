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
from toree_profile import *
from toree_manager import *
from util import trace_print, debug_print, debug_pprint

class LifecycleManager:
    """
    A Orchestrator for Toree Lifecycle which select an available
    toree sloot, reserv it and start/stop when notebooks are
    started/stopped.

    Open slots are identified by a not having a toree.pid. In case
    of corruption or a requirement to kill the toree process, one
    should also remove the toree.id from the specific Toree slot.
    """
    configManager = None
    toreeManager = None

    def __init__(self):
        trace_print('__LifecycleManager.init__')
        self.configManager = ConfigManager()
        self.toreeManager = ToreeManager()

    def _reserve_profile(self):
        trace_print('__LifecycleManager._reserve_profile__')
        """
        Tries to reserve an available toree slot

        :return: the reserved Toree slot or None
        """
        profilesFolder = self.configManager.getProfilesFolder()
        profile = None
        """Select from the available kernel configurations"""
        for (path, dirs, files) in os.walk(profilesFolder):
            for folderName in dirs:
                profile = Profile(profilesFolder + '/' + folderName)
                if profile.isAvailable():
                    profile.reserve()
                    break
                else:
                    profile = None
        """Unlock the mutex enabling other processes to select same kernel config"""

        return profile

    def _release_profile(self, profile):
        """
        Release the provided Toree slot

        :param profile: the Toree slot that was previously reserved
        :return: None
        """
        trace_print('__LifecycleManager._release_profile__')
        profile.release()

    def start_toree(self):
        """
        Reserve a open Toree slot, and start a remote Toree
        instance with the configuration provided

        :return: the path to the Toree configuration file
        (profile.json) which was used to start Toree. A
        runtime error is thrown in case of no more available
        Toree slots.
        """
        trace_print('__LifecycleManager.start_toree__')
        profile = self._reserve_profile()
        #if profile is None:
        #    raise RuntimeError('No Toree slot available.')
        #self.toreeManager.start_toree(profile)

        return profile

    def stop_toree(self, profile):
        """
        Stop remote Toree instance and release Toree slot
        :param profile: the toree slot that was previously reserved
        :return: None
        """
        trace_print('__LifecycleManager.stop_profile__')
        #self.toreeManager.stop_toree(profile)
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
