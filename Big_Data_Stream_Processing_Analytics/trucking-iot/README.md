# The vehicle Blackbox system

The Vehicle Blackbox project is a modern real-time streaming application serving as a reference framework for developing a big data pipeline, complete with a broad range of use cases and powerful reusable core components.

Modern applications can ingest data and leverage analytics in real-time.  These analytics are based on machine learning models typically built using historical big data.  This demo application provides examples of connecting data-in-motion analytics to your application based on Big Data.

From IoT sensor data collection, to flow management, real-time stream processing and analytics, through to machine learning and prediction, this reference project aims to demonstrate the power of open source solutions.

## Prerequisites

-   An instance of the [Hortonworks HDF Sandbox](#).
-   (or, alternatively) Your own Ambari-powered cluster with ZooKeeper, NiFi, Storm and Kafka
-   Integration with Schema Registry, download and run the single-script setup located at Scripts folder


Execute the script:
```
/root/nifi-to-nifi-with-schema.sh
```

Open the web applicaton: http://sandbox-hdf.hortonworks.com:25001

Optionally check out the NiFi Flow and Storm UI.

## Setup on existing HDF/HDP

> Note: If you're **not** on the HDF Sandbox, you'll need to replace the default cluster hostname "sandbox-hdf.hortonworks.com" in the following files, as well as check the port endpoints:
>
> trucking-schema-registrar/src/main/resources/application.conf
>
> trucking-storm-topology/src/main/resources/application.conf
>
> trucking-web-application/backend/conf/application.conf
>
> /scripts/*.sh

1.  On your sandbox/cluster, download this project.
```
https://github.com/SurajPB/AccidentDetectionPredictionAndPrevention.git
```

2.  Run the included automated deployment script.  Read a comicbook, this may take a few minutes.

> Note: By default the application deploys a Nifi -> Storm -> Nifi -> Kafka -> Web Application pipeline, with integration with Hortonworks Schema Registry.
>
> To use a different pre-built pipeline, open/edit `scripts/setup-environment.sh` and `scripts/builds/storm-topology.sh` before running the commands below.
```
cd trucking-iot
scripts/auto-deploy.sh
```

3.  On your local machine, open a browser and navigate to the web application: <http://sandbox-hdf.hortonworks.com:25001>

4.  Optionally check out the NiFi Flow and Storm UI. 
