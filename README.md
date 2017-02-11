# A Gateway for Apache Toree

The 'toree-gateway' enables a Jupyter Notebook server to connect with an Apache Torre kernel running on a remote machine.

The 'toree-gateway' consists of two pieces:

  * A Jupyter kernel, responsible to bridge the communication between the Jupyter Notebook and the remote Toree Kernel.
  * A Lifecycle component that controls start/stop of remote Toree Kernel instances.


# Installing Server Side

The server side is where Spark and Toree components reside and will be processing your analytics.

   * Install and deploy your spark cluster
   * Install Toree Kernel
   * Copy bin/startrun.sh to Toree bin folder

# Installing Client Side

The following are the main steps to install toree-gateway:

   * Install Anaconda 3
   * Install following pip dependencies: metakernel, paramiko, configparser
   * Install toree gateway distribution (e.g. /opt/toree-gateway) and set TOREE_GATEWAY_HOME 

```
mkdir -p /opt/toree-gateway
tar -xvf /opt/toree-gateway-2.0-bin.tgz -C /opt/toree-gateway --strip 1

rm -rf /root/.local/share/jupyter/kernels/toree-gateway
mkdir -p /root/.local/share/jupyter/kernels/toree-gateway
cp /opt/toree-gateway/kernel.json /root/.local/share/jupyter/kernels/toree-gateway/kernel.json
```

   * Initialize set of Toree profiles (Comming soon)
   

# Troubleshooting

## Check logs
   * Enable logs on client side ($TOREE_GATEWAY_HOME/conf/toree-gateway.properties)
   * Check logs on the remote side side (e.g. $TOREE_HOME/logs)

## Cleanup after failure or crash
   * Kill all toree process instances are killed on the server (Spark) side (ps -ef | grep toree)
   * Kill Jupyter server
   * Delete all 'toree.pid' files from profiles folder (e.g. find $TOREE_GATEWAY_HOME | grep toree.pid)
    