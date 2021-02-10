package com.orendainx.trucking.storm.bolts

import java.nio.charset.StandardCharsets
import java.util

import com.typesafe.scalalogging.Logger
import org.apache.nifi.storm.NiFiDataPacket
import org.apache.storm.task.{OutputCollector, TopologyContext}
import org.apache.storm.topology.OutputFieldsDeclarer
import org.apache.storm.topology.base.BaseRichBolt
import org.apache.storm.tuple.{Fields, Tuple, Values}

/**
  * Convert Tuples in the form of NiFiDataPackets into Tuples of their respective JVM objects.
  *
  */
class NiFiPacketToSerialized extends BaseRichBolt {

  private lazy val log = Logger(this.getClass)
  private var outputCollector: OutputCollector = _

  override def prepare(stormConf: util.Map[_, _], context: TopologyContext, collector: OutputCollector): Unit = {
    outputCollector = collector
  }

  override def execute(tuple: Tuple): Unit = {
    val dp = tuple.getValueByField("nifiDataPacket").asInstanceOf[NiFiDataPacket]

    val content = dp.getContent
    val str = new String(content, StandardCharsets.UTF_8)

    log.info(s"Content: $content")
    log.info(s"str: $str")

    //import java.util.Base64
    //val dec = Base64.getDecoder.decode(content)

    outputCollector.emit(new Values(dp.getAttributes.get("dataType"), str))
    outputCollector.ack(tuple)
  }

  override def declareOutputFields(declarer: OutputFieldsDeclarer): Unit = declarer.declare(new Fields("dataType", "data"))
}
