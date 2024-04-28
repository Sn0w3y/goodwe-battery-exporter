# GoodWe Battery Exporter

This repository contains a way to extract the Values of the TCP-Payload sent to the GoodWe Server.

## SEMS MITM Exporter

This is a Prometheus exporter for Goodwe devices which integrate with the cloud-hosted Smart Energy Managment System (SEMS) portal.
It works by implementing a [MITM attack](https://en.wikipedia.org/wiki/Man-in-the-middle_attack) on the SEMS portal protocol, hence the name.

### Features

The SEMS GoodWe exporter has the following advantages over just using the SEMS Portal:

* Transparently forwards data to SEMS Portal (option not to forward traffic is a WIP).
* Allows you to store your data in a Prometheus instance that you control.
* Visualise your data using standard tools like Grafana.
* Because you connect your HF-LPB100 (GoodWe WiFi or LAN Dongle to the Script nothing can reach the Inverter - afaik. So Updates etc. do not reach it)
* Summons Batman to the SEMS Portal (optional, set env var `BATSIGNAL=true`).

### Hardware support

Currently hardware support in the SEMS MITM Exporter is limited to the equipment I own:

* [GW5K-ET - GW10K-ET]([https://www.goodwe.com.au/single-phase-homekit](https://de.goodwe.com/et-plus-series-three-phase-hybrid-solar-inverter))

PRs welcome if you want to add support for your device.

> [!NOTE]
> Battery included !
> Open issues to discuss how to improve this.

### How to get it

Simple - as everything in Python:

* Clone this Repo
* Edit your config.py File for your preferences
* Start the main.py

### How to use it

At a high level:

1. Start the exporter.
2. Get traffic to the exporter. Either:
    * Point the DNS of `tcp.goodwe-power.com` to the IP of the exporter; or
    * Reconfigure your hardware to connect to the IP of the exporter. (With the WebUI.bin you can reflash your WebUI to set up the Server to send the Data to directly in the UI of your Device!) -> See /files/HowTo.md
3. Right now thats all - look at the Console for the incoming Data
4. ToDo - Add a export function

Detailed instructions for supported hardware is a WIP.
