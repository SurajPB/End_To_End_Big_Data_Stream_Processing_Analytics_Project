package com.orendainx.trucking.simulator.models

/**
  * The model for a driving pattern.
  *
  * 2018AB04032 - Suraj P B - BITS Pilani Dissertation
  */
case class DrivingPattern(name: String, minSpeed: Int, maxSpeed: Int, spreeFrequency: Int, spreeLength: Int, violationPercentage: Int)
