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

str="'$*'"

timestamp() {
  date +"%Y-%m-%d_%H-%M-%S"
}

echo "$str" > ../log/kernel_$(timestamp)_params.log

# Start the kernel as a background process.
nohup ./run.sh "$@" > ../log/kernel_$(timestamp).log &

# Acquire the pid for the kernel just started and write it to the pid file ...
echo $!

# Return with a status in $?, and output the kernel slot as the handle that
# the caller provides when stopping the kernel.
# echo "$free_handle"
exit 0