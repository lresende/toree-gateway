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


ROOT=`dirname $0`
ROOT=`cd $ROOT; pwd`

if [ -z "$1" ]
then
  echo "Usage:"
  echo "  dev/deploy-gateway.sh host"
  echo " "
  exit 1
fi

LOCALHOST="$(/bin/hostname -f)"
PYTHON_VERSION="2"
INSTALL_HOME="/opt"
TOREE_GATEWAY_HOME="/opt/toree-gateway"
ANACONDA_HOME="/opt/anaconda2"
JUPYTER_DATA_DIR="/root/.local/share/jupyter"
HOST=$1

scp target/toree-gateway-3.0-bin.tgz root@$HOST:$INSTALL_HOME/toree-gateway-3.0-bin.tgz

ssh root@$HOST "rm -rf $TOREE_GATEWAY_HOME/lib"
ssh root@$HOST "rm -rf $TOREE_GATEWAY_HOME/python"
ssh root@$HOST "rm -rf $TOREE_GATEWAY_HOME/kernel.json"
ssh root@$HOST "mkdir -p $TOREE_GATEWAY_HOME"
ssh root@$HOST "tar -xvf $INSTALL_HOME/toree-gateway-3.0-bin.tgz -C $TOREE_GATEWAY_HOME --strip 1"

ssh root@$HOST "rm -rf /root/.local/share/jupyter/kernels/toree-gateway"
ssh root@$HOST "mkdir -p /root/.local/share/jupyter/kernels/toree-gateway"
ssh root@$HOST "cp /opt/toree-gateway/kernel.json /root/.local/share/jupyter/kernels/toree-gateway/kernel.json"

ssh root@$HOST "rm -rf $INSTALL_HOME/toree-gateway-3.0-bin.tgz"

echo "Installation completed"
echo "Start Jupyter using : $ANACONDA_HOME/bin/jupyter notebook --ip=<your public ip>"
