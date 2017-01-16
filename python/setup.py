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


setup(name='toree_proxy_kernel',
    version='0.1',
    description='Toree Client Proxy Kernel',
    long_description='A simple echo kernel for Jupyter/IPython, based on MetaKernel',
    py_modules=['toree_proxy_kernel'],
    install_requires=['metakernel', 'py4j'],
    classifiers = [
        'Framework :: IPython',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'Topic :: System :: Shells',
    ]
)
