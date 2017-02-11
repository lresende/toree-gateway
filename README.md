# A Gateway for Apache Toree

The 'toree-gateway' enables a Jupyter Notebook server to connect with an Apache Torre kernel running on a remote machine.

The 'toree-gateway' consists of two pieces:

  * A Jupyter kernel, responsible to receive the original request from Jupyter server.
  * A gateway, which the kernel uses to actually submit/evaluate the requests on the Apache Toree instance on the server.