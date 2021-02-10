package com.orendainx.trucking.simulator.transmitters

import akka.actor.Actor
import com.orendainx.trucking.commons.models.TruckingData

/**
  * DataTransmitters are the sinks for generated simulator data.
  * They may record events to filesystems, stores over a network, standard out, etc.
  *
  * 2018AB04032 - Suraj P B - BITS Pilani Dissertation
  */
object DataTransmitter {
  case class Transmit(data: TruckingData)
}

trait DataTransmitter extends Actor

/*
 * A valid concern could be that by using actors over some singleton service that is equally as threadsafe, we are employing an antipattern.
 * However, considering not all DataTransmitters may leverage a data structure that can be accessed concurrently, using actors
 * to regulate resource access is a much better (and cleaner) way to approach the problem.
 */
