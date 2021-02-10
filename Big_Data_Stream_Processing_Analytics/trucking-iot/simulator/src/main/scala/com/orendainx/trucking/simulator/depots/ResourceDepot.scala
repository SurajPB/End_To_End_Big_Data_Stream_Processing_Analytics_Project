package com.orendainx.trucking.simulator.depots

import akka.actor.Actor
import com.orendainx.trucking.simulator.models.Truck
import com.orendainx.trucking.simulator.models.Route

/**
  * 2018AB04032 - Suraj P B - BITS Pilani Dissertation
  */
object ResourceDepot {
  // TODO: can generalize into RequestResource or ReturnResource
  case class RequestTruck(previous: Truck)
  case class RequestRoute(previous: Route)

  case class ReturnTruck(truck: Truck)
  case class ReturnRoute(route: Route)
}

trait ResourceDepot extends Actor
