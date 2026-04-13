# GNSS RTK Integration for Robotics (ROS)

## Overview

This repository provides a complete, end-to-end tutorial to achieve **centimeter-level positioning** on a robot using:

- a GNSS receiver and a multi-band antenna
- RTK corrections from the Centipede RTK Network through NTRIP
- a Raspberry Pi 4B running the ROS node
- internet connectivity (WiFi, smartphone tethering, or 4G dongle) to receive RTCM corrections

The system uses a SparkFun RTK Surveyor connected to the robot computer, which receives GNSS satellite measurements and RTK correction data. A custom ROS node reads the receiver output, injects NTRIP corrections into the receiver, and publishes the resulting GNSS navigation data to ROS topics.
 
---

## System Architecture

### Components Used

- **GNSS Receiver**: [SparkFun RTK Surveyor](https://www.sparkfun.com/sparkfun-rtk-surveyor.html)  
  - Based on u-blox ZED-F9P  
  - Provides RTK-capable positioning (cm-level)

- **Antenna**: [GNSS Multi-Band L1/L2/L5 Surveying Antenna](https://www.sparkfun.com/gnss-multi-band-l1-l2-l5-surveying-antenna-tnc-spk6618h.html)  
  - Dual/multi-band required for stable RTK FIX  
  - Improves accuracy and convergence time  

- **Onboard Computer**: Raspberry Pi 4B  
  - Runs ROS or ROS2 
  - Hosts GNSS driver + others custom package  
  - Handles NTRIP client for RTK corrections  

- **Connectivity (required for RTK)**:
  - 4G USB dongle  
  - Smartphone tethering (USB/WiFi)  
  - WiFi connection  

  → Needed to receive RTCM corrections from the network  

- **Robot Platform**: *Antcar robot (or your platform)*  

- **Connections**:
  - GNSS Receiver ↔ Raspberry Pi: USB or UART  
  - Raspberry Pi ↔ Internet: WiFi / 4G / tethering  

### High-Level Data Flow

```text
GNSS Satellites
      │
      ▼
[GNSS Antenna]
      │
      ▼
[SparkFun RTK Surveyor]
      ▲
      │  RTCM corrections
      │
[Raspberry Pi 4B]
      ▲
      │
      │ Internet connection
      │ (WiFi / 4G / smartphone tethering)
      ▼
[Centipede RTK Network]

The Raspberry Pi also runs the ROS node, reads GNSS data from the receiver,
forwards NTRIP corrections to the receiver, and publishes navigation data to ROS.
