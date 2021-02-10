# Vehicle Black Box Simulator in Sandbox environment

This is a robust, extensible simulator engine that generates vehicle-sensors-related data for the larger Vehicle E2E Blackbox project.

## Outline

-   [Features](#features)
-   [Generating Data](#generating-data)
-   [Data Format](#data-format)
-   [For Developers](#for-developers)

## Features

-   The simulator can be used as a library or as a standlone application.
-   Different ways to store/transmit the generated data (to Kafka topics, the filesystem, Akka actors, standard out, a buffering queue for manual extraction).
-   Can run indefinitely or for a specified number of events.
-   Control of simulator parameters done through a single configuration file (`src/main/resources/application.conf`).
-   Complies with the data models defined by the `trucking-commons` project, providing custom and third party applications an interface for serializing/deserializing the generated data.

## Generating Data

If using NiFi: A custom NiFi processor has been developed that wraps this simulator and generates data entirely using NiFi's drag-and-drop interface.  **No code or terminal required**.  Check out the `trucking-nifi-bundle` project.

```
TODO: Describe how to run the simulator without NiFi (super easy, just need to get around to writing the docs.)

For now: if you have any questions, feel free to ping me.
```
