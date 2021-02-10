package com.orendainx.trucking.simulator.transmitters

import akka.actor.{ActorLogging, ActorRef, Props}
import com.orendainx.trucking.simulator.transmitters.DataTransmitter.Transmit

/**
  * 2018AB04032 - Suraj P B - BITS Pilani Dissertation
  */
object ActorTransmitter {

  def props(outActr: ActorRef) = Props(new ActorTransmitter(outActr))
}

class ActorTransmitter(outActr: ActorRef) extends DataTransmitter with ActorLogging {

  def receive = {
    case Transmit(data) => outActr ! data
  }
}
