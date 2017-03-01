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

import base64
import unittest
import security

class TestSecurity(unittest.TestCase):

    def setUp(self):
        self.VALID_OBF_PASSWORD = 'OBF:1v2j1uum1xtv1zej1zer1xtn1uvk1v1v'
        self.VALID_BASE64_PASSWORD = 'B64:cGFzc3dvcmQ='
        self.PLAIN_TEXT_PASSWORD = 'password'

    def test_decode_obf_password(self):
        self.assertEqual(security.decode_password(self.VALID_OBF_PASSWORD), self.PLAIN_TEXT_PASSWORD, 'Properly decode OBF passwords')

    def test_decode_base64_password(self):
        self.assertEqual(security.decode_password(self.VALID_BASE64_PASSWORD), self.PLAIN_TEXT_PASSWORD, 'Properly decode Base64 passwords')

    def test_return_provided_password_when_no_encoding_scheme_provided(self):
        self.assertEqual(security.decode_password(self.PLAIN_TEXT_PASSWORD), self.PLAIN_TEXT_PASSWORD, 'Properly return unencoded passwords')

if __name__ == "__main__":
    unittest.main()