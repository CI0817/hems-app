# Home Energy Management Systems (HEMS) Application

## Project Overview

This project contains a containerised, end-to-end HEMS platform designed for a modern residential building with solar arrays, inverters, battery packs, EVs, chargers, and connection to the main grid.

This project mainly serves as a learning experience for a person who is interested in building sustainability, microgrids, control systems, and internet of things (IoT) solutions.

## System Architecture

The whole system can be broken down into five layers:

| Layer | Responsibility |
|-------|----------------|
| **5. Web UI (Presentation)** | Real-time dashboards, control toggles, and historical charts for homeowners and demo reviewers. |
| **4. HEMS Micro-Services (Application / Intelligence)** | Forecasting, optimisation (peak-shave, tariff arbitrage), rule engine, alerting. |
| **3. Message Bus (Integration)** | Decouples producers (devices) from consumers (services/UI). Provides durable, topic-based pub-sub. |
| **2. Edge Gateway (Device Aggregation)** | Polls heterogeneous hardware, normalises payloads, and publishes JSON packets upward. |
| **1. Device / Data Layer (Physical Assets)** | Get the data from Solar inverter, battery BMS, EV charger, smart meter, weather sensor. |

### Vendor-agnostic

All data coming from the edge gateway will be JSON packets with standardised structure, making it easier to scale and maintain when we add more devices that use different protocols.

### MQTT

Communications between the micro-services and the edge gateway are done via MQTT for its lightweight, pub/sub nature, and a strong developer's community.

### Database

A microservice is used to log the data coming from all the devices for future analysis and historical data graphing.

### Up-stream and Down-stream Communications

Up-stream communications are done from the devices to the HEMS micro-services, the UI, and the database, also known as data reporting. Down-stream communications are done from the HEMS micro-services that issue commands to the devices, alaso known as controlling.

## MQTT Topics Taxonomy

