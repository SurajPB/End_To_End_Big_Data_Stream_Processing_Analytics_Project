package com.orendainx.trucking.simulator.transmitters

import akka.actor.Props
import com.orendainx.trucking.simulator.transmitters.DataTransmitter.Transmit

/**
  * StandardOutTransmitter records data to standard output.
  *
  * 2018AB04032 - Suraj P B - BITS Pilani Dissertation
  */
object StandardOutTransmitter {
  def props() = Props(new StandardOutTransmitter)
}

class StandardOutTransmitter extends DataTransmitter {

  def receive = {
    case Transmit(data) => println(data.toCSV)
  }

}
