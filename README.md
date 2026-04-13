# GNSS RTK Integration for Robotics (ROS2)

## Overview

This repository provides a complete, end-to-end tutorial to achieve **centimeter-level positioning** on a robot using:

- GNSS receiver + multi-band antenna (L1/L2)
- RTK corrections via Centipede RTK Network (NTRIP)
- A Raspberry Pi 4B running a custom ROS2 package
- Internet connectivity (4G / WiFi / smartphone tethering) for receiving RTK corrections

The goal is to make the system fully reproducible, from hardware setup to ROS topic publishing.

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
  - Runs ROS2  
  - Hosts GNSS driver + your custom package  
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
