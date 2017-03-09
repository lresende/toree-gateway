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
import sys
import unittest
import tempfile
import util

class TestUtils(unittest.TestCase):

    def setUp(self):
        """ capture stdout to a temp file """
        self.tempFile = tempfile.TemporaryFile()
        os.dup2(self.tempFile.fileno(), sys.stdout.fileno())

    def tearDown(self):
        """ remove temp file """
        self.tempFile.close()

    def test_output_is_clean_when_debug_is_disabled(self):
        util.isDebugging = False
        util.debug_print('Debug Message')
        self.assertEqual(self._readOutput(), '', 'Should not write messages when debug is disabled')

    def test_output_has_content_when_debug_is_enabled(self):
        util.isDebugging = True
        util.debug_print('Debug Message')
        self.assertEqual(self._readOutput(), 'Debug Message', 'Should write messages when debug is enabled')

    def test_output_has_content_when_byte_array_message_is_passed(self):
        util.isDebugging = True
        util.debug_print(b'Binary Debug Message')
        self.assertEqual(self._readOutput(), 'Binary Debug Message', 'Should write messages when debug is enabled')

    def _readOutput(self):
        self.tempFile.seek(0)
        return self.tempFile.read().decode().rstrip()

if __name__ == "__main__":
    unittest.main()

