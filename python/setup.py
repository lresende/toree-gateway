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

from setuptools import setup


setup(name='toree_gateway_kernel',
    version='0.1',
    description='Toree Gateway',
    long_description='A Gateway Kernel for Apache Toree, based on MetaKernel',
    py_modules=['toree_gateway_kernel'],
    install_requires=['metakernel', 'paramiko', 'configparser'],
    classifiers = [
        'Framework :: IPython',
        'License :: OSI Approved :: Apache License 2.0',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'Topic :: System :: Shells',
    ]
)
