#!/usr/bin/env bash
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

# Create the specified directory.
create_dir(){
   echo "Creating $1 ..."
   mkdir -p $1
   status=$?
   if [ $status -ne 0 ]; then
      echo "Failed to create directory $1 ($status)"
      exit $status
   fi
}

# Build the connection profiles that the kernel will use.
build_connection_profiles(){
   let n=$1
   let p=$GLOBAL_FIRST_PORT_NUMBER

   for ((k=1; k<=n; k++))
   do
      # echo "--- Initialize kernel instance $k"
      KERNEL_STATE="kernel-$k"
      create_dir $TOREE_GATEWAY_HOME/profiles/$KERNEL_STATE
      PROFILE="$TOREE_GATEWAY_HOME/profiles/$KERNEL_STATE/profile.json"
      echo "{" > $PROFILE
      echo "    \"stdin_port\":        $p," >> $PROFILE; let p=p+1
      echo "    \"control_port\":      $p," >> $PROFILE; let p=p+1
      echo "    \"hb_port\":           $p," >> $PROFILE; let p=p+1
      echo "    \"shell_port\":        $p," >> $PROFILE; let p=p+1
      echo "    \"iopub_port\":        $p," >> $PROFILE; let p=p+1
      echo "    \"ip\":                \"$TOREE_IP\"," >> $PROFILE
      echo "    \"transport\":         \"$TOREE_TRANSPORT\"," >> $PROFILE
      echo "    \"signature_scheme\":  \"$TOREE_SIG_SCHEME\"," >> $PROFILE
      # echo "    \"key\":               \"$TOREE_KEY\"" >> $PROFILE
      echo "    \"key\": \"\"," >> $PROFILE
      echo "    \"py4j_java\":    $p," >> $PROFILE; let p=p+500
      echo "    \"py4j_python\":  $p" >> $PROFILE; let p=p+1
      echo "}" >> $PROFILE
      let p=p-501
   done
}

# Calculate the number of kernels we can initialize, given the number of ports provided.
#   $1 == number of ports available to use
#   sets num_kernels == number of kernels (global variable, side effect, I know ...)
get_num_kernels() {
   let m=$1%5
   if [ $m -ne 0 ]; then
      echo "Info: $1 is not a multiple of 5."
      echo "   $m ports will not be used."
   fi

   let num_kernels=$1/5
   echo "Number of kernels: $num_kernels"
}

# Source the specified config file.
#   $1 == specified config file
#   $2 == default config file
source_config(){
   if [ ! -z "$1" ]; then
     if [ ! -f $1 ]; then
           echo "File $1 not found!"
           exit 2
     else
       source $1
     fi
   else
     source ../conf/config
   fi
}

# Get the installation configuation settings.
source_config

# Get the number of kernels and build the connection profiles for all of
# the kernel instances.
get_num_kernels $GLOBAL_NUMBER_OF_PORTS   # sets num_kernels
build_connection_profiles $num_kernels
