package com.orendainx.trucking.webapplication

import angulate2.std.{Component, OnInit}
import com.orendainx.trucking.webapplication.models.{PrettyEnrichedTruckAndTrafficData, PrettyTruckAndTrafficData}

import scala.scalajs.js

/**
  * 2018AB04032 - Suraj P B - BITS Pilani Dissertation
  */
@Component(
  selector = "event-list-component",
  templateUrl = "/assets/templates/event-list.component.html"
)
class EventListComponent(webSocketService: WebSocketService) extends OnInit {

  private val MaxEvents = 100
  val events: js.Array[PrettyEnrichedTruckAndTrafficData] = js.Array()

  override def ngOnInit(): Unit = {
    webSocketService.registerCallback(addEvent _)
  }

  def addEvent(event: PrettyEnrichedTruckAndTrafficData): Unit = {
    events += event
    if (events.size > MaxEvents) events.trimStart(1)
  }

}
