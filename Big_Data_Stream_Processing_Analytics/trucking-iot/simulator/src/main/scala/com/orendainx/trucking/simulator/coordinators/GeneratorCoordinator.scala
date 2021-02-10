package com.orendainx.trucking.simulator.coordinators

import akka.actor.{Actor, ActorRef}

/**
  * [[GeneratorCoordinator]] objects coordinate [[com.orendainx.trucking.simulator.generators.DataGenerator]]
  * objects and how they generate data.
  * 2018AB04032 - Suraj P B - BITS Pilani Dissertation
  */
object GeneratorCoordinator {
  case class AcknowledgeTick(generator: ActorRef)
}

trait GeneratorCoordinator extends Actor
