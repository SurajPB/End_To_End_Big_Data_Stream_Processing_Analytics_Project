package com.orendainx.trucking.simulator.transmitters

import akka.actor.{ActorLogging, Props}
import better.files.File
import com.orendainx.trucking.simulator.transmitters.DataTransmitter.Transmit

/**
  * FileTransmitter records data to the filesystem, specifically to the file whose path is passed in as the constructor parameter.
  *
  * 2018AB04032 - Suraj P B - BITS Pilani Dissertation
  */
object FileTransmitter {
  def props(filepath: String) = Props(new FileTransmitter(filepath))
}

class FileTransmitter(filepath: String) extends DataTransmitter with ActorLogging {

  private val writer = File(filepath).createIfNotExists(createParents = true).newPrintWriter(true)

  def receive = {
    case Transmit(data) => writer.println(data.toCSV)
  }

  override def postStop(): Unit = {
    writer.close()
    log.info("FileTransmitter closed output file stream.")
  }
}
