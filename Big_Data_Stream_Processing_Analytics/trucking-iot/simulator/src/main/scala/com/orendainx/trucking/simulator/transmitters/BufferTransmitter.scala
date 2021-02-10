package com.orendainx.trucking.simulator.transmitters

import akka.actor.{ActorLogging, Props}
import com.orendainx.trucking.commons.models.TruckingData
import com.orendainx.trucking.simulator.transmitters.BufferTransmitter.Fetch
import com.orendainx.trucking.simulator.transmitters.DataTransmitter.Transmit

import scala.collection.mutable

/**
  * BufferTransmitter buffers data until fetched by an outside source.
  *
  * 2018AB04032 - Suraj P B - BITS Pilani Dissertation
  */
object BufferTransmitter {
  case object Fetch

  def props() = Props(new BufferTransmitter)
}

class BufferTransmitter extends DataTransmitter with ActorLogging {

  val buffer = mutable.ListBuffer.empty[TruckingData]

  def receive = {
    case Transmit(data) =>
      buffer += data
      log.debug(s"Data received: buffered ${buffer.size}")

    case Fetch =>
      sender() ! buffer.toList
      log.debug(s"Sent ${buffer.size} data. ${buffer.toString()}")
      buffer.clear()
  }

  override def postStop(): Unit = {
    log.info(s"BufferTransmitter stopped with ${buffer.length} items unfetched.")
  }
}
