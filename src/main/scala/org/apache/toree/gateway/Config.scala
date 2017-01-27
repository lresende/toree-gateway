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

import java.io.{FileInputStream, InputStream}
import java.nio.file.{Files, Path, Paths}
import java.util.Properties

object Config {
  val CONFIG_FILE = "toree-gateway.properties"
  var properties = new Properties()

  // initialization
  {
    var home: String = ""
    scala.util.control.Exception.ignoring(classOf[java.util.NoSuchElementException]) {
      home = sys.env("TOREE_GATEWAY_HOME")
    }
    var configPath: Path = Paths.get(home + "/conf/"  + CONFIG_FILE)
    if (Files.exists(configPath) == false) {
      configPath = Paths.get(getClass.getResource("/"+ CONFIG_FILE).getPath)
    }
    this.properties.load(new FileInputStream(configPath.toString))
  }


  def get(key: String): String = {
    return this.properties.getProperty(key)
  }

  def getOrElse(key:String, default:String): String = {
    val value = get(key)
    if(value == null || value.isEmpty) {
      return default
    } else {
      return value
    }
  }

  def getAsInt(key: String): Int = {
    return this.properties.getProperty(key).toInt
  }

  def getOrElseAsInt(key:String, default:Int): Int = {
    val value = get(key)
    if(value == null || value.isEmpty) {
      return default
    } else {
      return value.toInt
    }
  }
}