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

__OBFUSCATE = "OBF:"
__BASE64 = "B64:"


def _range(start, end, step):
    while start < end:
        yield start
        start += step

def _base36encode(number, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    """Converts an integer to a base36 string."""
    if not isinstance(number, int):
        raise TypeError('number must be an integer')

    base36 = ''
    sign = ''

    if number < 0:
        sign = '-'
        number = -number

    if 0 <= number < len(alphabet):
        return sign + alphabet[number]

    while number != 0:
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36

    return sign + base36

def _base36decode(number):
    return int(number, 36)


def _deobfuscate(s):
    if s.startswith(__OBFUSCATE):
        s = s[4:];

    b = []
    for i in _range(0, len(s), 4):
        if(s[i] == 'U'):
            i += 1
            x = s[i: i+4]
            i0 = _base36decode(x)
            bxint = int(i0>>8)
            bx = chr(bxint)
            b.append(bx)
        else:
            x = s[i: i+4]
            i0 = _base36decode(x)
            i1 = int(i0 / 256)
            i2 = int(i0 % 256)
            bxint = int((i1 + i2 - 254) / 2)
            bx = chr(bxint)
            b.append(bx)

    return ''.join(b)


def _base64_decode(s):
    if s.startswith(__BASE64):
        s = s[4:];

    return base64.b64decode(s).decode()

def decode_password(encoded):
    """
    Decode encoded password
    Supported schemas are :
       OBF: from Jetty password obfuscator tool
       B64: Base64 encoding
    :param encoded: the encoded string
    :return: if properly prefixed with encoding schema, the decoded string, otherwise the provided value
    """
    if encoded.startswith(__BASE64):
        return _base64_decode(encoded)
    elif encoded.startswith(__OBFUSCATE):
        return _deobfuscate(encoded)
    else:
        return encoded


"""
print(decode_password('OBF:1v2j1uum1xtv1zej1zer1xtn1uvk1v1v'))
print(decode_password('OBF:1xfx1vuf1x1b1x1b1vuv1xf5'))
print(decode_password('B64:d2hvb3BpCg=='))
"""