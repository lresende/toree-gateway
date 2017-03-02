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

from pprint import pprint
from config import *

configManager = ConfigManager()
isDebugging = configManager.get('gateway.debug') == 'True'

def _clean_message(message):

    if not isinstance(message, str):
        message = str(message)

    password_string = '''"password"'''
    quote_string = '''"'''

    clean_message = None
    if "password" in message:
        p1 = message.find(password_string) + len(password_string)
        p2 = message.find(quote_string, p1) + len(quote_string)
        p3 = message.find(quote_string, p2) + len(quote_string) -1
        clean_message = message[:p2] + "*******" + message[p3:]
    else:
        clean_message = message

    return clean_message


def debug_print(message):
    if isDebugging:
        print(_clean_message(message))

def debug_pprint(message):
    if isDebugging:
        pprint(_clean_message(message))
