package com.ibm

import com.typesafe.config.ConfigFactory
import org.apache.toree.kernel.protocol.v5.client.boot.ClientBootstrap
import com.typesafe.config.Config
import org.apache.toree.kernel.protocol.v5.MIMEType
import org.apache.toree.kernel.protocol.v5.client.SparkKernelClient
import org.apache.toree.kernel.protocol.v5.client.boot.layers.{StandardHandlerInitialization, StandardSystemInitialization}
import org.apache.toree.kernel.protocol.v5.client.execution.DeferredExecution
import org.apache.toree.kernel.protocol.v5.content.ExecuteResult
import py4j.GatewayServer

import scala.concurrent.{Await, Promise}
import scala.concurrent.duration.Duration

import org.slf4j.LoggerFactory

class ToreeGateway(client: SparkKernelClient) {
  //  Define our callback
  def printResult(result: ExecuteResult) = {
    println(s"Result was: ${result.data.get(MIMEType.PlainText).get}")
  }

  def eval(code: String): Object = {
    val promise = Promise[String]
    val exRes: DeferredExecution = client.execute(code).onResult(er => {
      promise.success(er.data.get(MIMEType.PlainText).get)
    })

    Await.result(promise.future, Duration.Inf)
  }
}

object ToreeClient extends App {

  final val log = LoggerFactory.getLogger(this.getClass.getName.stripSuffix("$"))

  def getConfigurationFilePath: String = {
    var filePath = "/opt/toree_proxy/conf/profile.json"

    if (args.length == 0) {
      for (arg <- args) {
        if (arg.contains("json")) {
          filePath = arg
        }
      }
    }

    filePath
  }

  log.info("Application Initialized from " + new java.io.File(".").getCanonicalPath)
  log.info("With the following parameters:" )
  if (args.length == 0 ) {
    log.info(">>> NONE" )
  } else {
    for (arg <- args) {
      log.info(">>> Arg :" + arg )
    }
  }

  // Parse our configuration and create a client connecting to our kernel
  val configFileContent = scala.io.Source.fromFile(getConfigurationFilePath).mkString
  log.info(">>> Configuration in use " + configFileContent)
  val config: Config = ConfigFactory.parseString(configFileContent)

  val client = (new ClientBootstrap(config)
    with StandardSystemInitialization
    with StandardHandlerInitialization).createClient()

  val toreeGateway = new ToreeGateway(client)

  val gatewayServer: GatewayServer = new GatewayServer(toreeGateway)
  gatewayServer.start()
}
