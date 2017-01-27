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

import com.typesafe.config.{Config, ConfigFactory}
import org.apache.toree.kernel.protocol.v5.client.boot.ClientBootstrap
import org.apache.toree.kernel.protocol.v5.client.boot.layers.{StandardHandlerInitialization, StandardSystemInitialization}
import org.scalatest.{FlatSpec, Ignore}
import org.slf4j.LoggerFactory

@Ignore
class ToreeGatewaySpec extends FlatSpec {

  final val log = LoggerFactory.getLogger(this.getClass.getName.stripSuffix("$"))


  val profileJSON: String = """
  {
  "stdin_port":   48701,
  "control_port": 48702,
  "hb_port":      48705,
  "shell_port":   48703,
  "iopub_port":   48704,
  "ip": "9.30.137.220",
  "transport": "tcp",
  "signature_scheme": "hmac-sha256",
  "key": "",
  "py4j_java":     25433,
  "py4j_python":   25434
  }
  """.stripMargin

  val toreeGateway = {
    // Parse our configuration and create a client connecting to our kernel
    val config: Config = ConfigFactory.parseString(profileJSON)

    val client = (new ClientBootstrap(config)
      with StandardSystemInitialization
      with StandardHandlerInitialization).createClient()

    val toreeGateway = new ToreeGateway(client)

    toreeGateway

  }

  "gateway" should "receive dataframe show results" in {
    val result = toreeGateway.eval(
      """
        import org.apache.commons.io.IOUtils
        import java.net.URL
        import java.nio.charset.Charset

        val sqc = spark.sqlContext
        import sqc.implicits._

        val bankText = sc.parallelize(
            IOUtils.toString(
                new URL("https://s3.amazonaws.com/apache-zeppelin/tutorial/bank/bank.csv"),
                Charset.forName("utf8")).split("\n"))

        case class Bank(age: Integer, job: String, marital: String, education: String, balance: Integer)

        val bank = bankText.map(s => s.split(";")).filter(s => s(0) != "\"age\"").map(
            s => Bank(s(0).toInt,
                    s(1).replaceAll("\"", ""),
                    s(2).replaceAll("\"", ""),
                    s(3).replaceAll("\"", ""),
                    s(5).replaceAll("\"", "").toInt
                )
        ).toDF()

        bank.show(1)
      """.stripMargin
    ).toString.stripMargin

    assert(result.contains("only showing top 1 row"))
  }

  "gateway" should "evaluate simple math statements" in {
    val result = toreeGateway.eval(
      """
      1 + 1
      """.stripMargin
    ).toString.stripMargin

    assert(result.contains("2"))
  }

  "gateway" should "receive error messages when exception is thrown" in {
    val result = toreeGateway.eval(
      """
      println(1/0)
      """.stripMargin
    ).toString.stripMargin

    assert(result.contains("java.lang.ArithmeticException"))
  }

  "gateway" should "receive spark version" in {
    val result = toreeGateway.eval(
      """
      spark.sparkContext.version
      """.stripMargin
    ).toString.stripMargin

    assert(result.contains("2.0.2"))
  }

  "gateway" should "receive spark configuration" in {
    val result = toreeGateway.eval(
      """
      spark.conf.getAll
      """.stripMargin
    ).toString.stripMargin

    assert(result.contains("toree-assembly-0.2.0.dev1-incubating-SNAPSHOT.jar"))
  }

  "gateway" should "receive println result" in {
    val result = toreeGateway.eval(
      """
      println("Hi")
      """.stripMargin
    ).toString.stripMargin

    assert(result.contains("Hi"))
  }

  "gateway" should "import statement sucessfully" in {
    val result = toreeGateway.eval(
      """
      import org.apache.spark.sql.functions._
      """.stripMargin
    ).toString.stripMargin

    assert(result.contains("done"))
  }
}
