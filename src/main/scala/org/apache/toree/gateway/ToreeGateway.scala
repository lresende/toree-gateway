/*
 * (C) Copyright IBM Corp. 2017
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

package org.apache.toree.gateway

import com.typesafe.config.ConfigFactory
import org.apache.toree.kernel.protocol.v5.client.boot.ClientBootstrap
import com.typesafe.config.Config
import org.apache.toree.kernel.protocol.v5.MIMEType
import org.apache.toree.kernel.protocol.v5.client.SparkKernelClient
import org.apache.toree.kernel.protocol.v5.client.boot.layers.{StandardHandlerInitialization, StandardSystemInitialization}
import org.apache.toree.kernel.protocol.v5.client.execution.DeferredExecution
import org.apache.toree.kernel.protocol.v5.content.{ExecuteReplyError, ExecuteReplyOk, ExecuteResult, StreamContent}
import py4j.GatewayServer

import scala.concurrent.{Await, Promise}
import scala.concurrent.duration.Duration
import org.slf4j.{Logger, LoggerFactory}

import play.api.libs.json._

import scala.util.Try

class ToreeGateway(client: SparkKernelClient) {
  final val log = LoggerFactory.getLogger(this.getClass.getName.stripSuffix("$"))


  private def handleResult(promise:Promise[String], result: ExecuteResult) = {
    log.info(s"Result was: ${result.data(MIMEType.PlainText)}")
    promise.success(result.data(MIMEType.PlainText))
    //promise.success(result.content)
  }

  private def handleSuccess(promise:Promise[String], executeReplyOk: ExecuteReplyOk) = {
    /*
    if(! promise.isCompleted) {
      log.info(s"Successful code completion")
      promise.complete(Try("done"))
    }
    */
  }

  private def handleError(promise:Promise[String], reply:ExecuteReplyError) {
    log.info(s"Error was: ${reply.ename.get}")
    //promise.failure(new Throwable("Error evaluating paragraph: " + reply.content))
    promise.success(reply.status + ":" + reply.ename.getOrElse("") + " - " + reply.evalue.getOrElse(""))
  }

  private def handleStream(promise:Promise[String], content: StreamContent) {
    log.info(s"Received streaming content ${content.name} was: ${content.text}")
    promise.success(content.text)
  }

  def eval(code: String): Object = {
    val promise = Promise[String]
    try {
      val exRes: DeferredExecution = client.execute(code)
      .onResult(executeResult => {
        handleResult(promise, executeResult)
      }).onError(executeReplyError =>{
        handleError(promise, executeReplyError)
      }).onSuccess(executeReplyOk => {
        handleSuccess(promise, executeReplyOk)
      }).onStream(streamResult => {
        handleStream(promise, streamResult)
      })

    } catch {
      case t : Throwable => {
        log.info("Error submitting request: " + t.getMessage, t)
        promise.success("Error submitting request: " + t.getMessage)
      }
    }

    Await.result(promise.future, Duration.Inf)
  }
}

object ToreeGatewayClient extends App {

  final val log = LoggerFactory.getLogger(this.getClass.getName.stripSuffix("$"))

  def getConfigurationFilePath: String = {
    var filePath = "/opt/toree-gateway/conf/profile.json"

    if (args.length > 0) {
      for (arg <- args) {
        if (arg.contains("json")) {
          filePath = arg
        }
      }
    }

    filePath
  }

  if (log.isDebugEnabled ) {
    log.debug("Application Initialized from " + new java.io.File(".").getCanonicalPath)
    log.debug("With the following parameters:" )
  }

  // Parse our configuration and create a client connecting to our kernel
  val configFileContent = scala.io.Source.fromFile(getConfigurationFilePath).mkString
  if (log.isDebugEnabled()) {
    log.debug(">>> Configuration in use " + configFileContent)
  }
  val config: Config = ConfigFactory.parseString(configFileContent)

  val client = (new ClientBootstrap(config)
    with StandardSystemInitialization
    with StandardHandlerInitialization).createClient()

  val toreeGateway = new ToreeGateway(client)

  val jsonValue = Json.parse(configFileContent)
  val port = (jsonValue \ "py4j_java").as[Int]

  if(log.isDebugEnabled()) {
    log.debug(">>> Starting GatewayServer with port " + port)
  }

  val gatewayServer: GatewayServer = new GatewayServer(toreeGateway, port)
  gatewayServer.start()
}