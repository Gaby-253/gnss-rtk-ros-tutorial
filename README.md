# GNSS RTK Integration for Robotics (ROS)

## Overview

This repository provides a complete, end-to-end tutorial to achieve **centimeter-level positioning** on a robot using:

* a GNSS receiver and a multi-band antenna
* RTK corrections from the Centipede RTK Network through NTRIP
* a Raspberry Pi 4B running a custom ROS node
* internet connectivity (WiFi, smartphone tethering, or 4G dongle) to receive RTCM corrections

The system uses a SparkFun RTK Surveyor connected to the robot computer. The Raspberry Pi connects to the NTRIP caster, forwards correction data to the GNSS receiver, and publishes the resulting GNSS navigation data to ROS topics.

---

## System Architecture

### Components Used

* **GNSS Receiver**: [SparkFun RTK Surveyor](https://wwwCentipede.sparkfun.com/sparkfun-rtk-surveyor.html)

  * Based on u-blox ZED-F9P
  * Provides RTK-capable positioning (cm-level)

* **Antenna**: [GNSS Multi-Band L1/L2/L5 Surveying Antenna](https://www.sparkfun.com/gnss-multi-band-l1-l2-l5-surveying-antenna-tnc-spk6618h.html)

  * Dual/multi-band required for stable RTK FIX
  * Improves accuracy and convergence time

* **Onboard Computer**: Raspberry Pi 4B

  * Runs ROS (tested with ROS1)
  * Hosts the custom GNSS RTK ROS node
  * Handles NTRIP client for RTK corrections

* **Connectivity (required for RTK)**:

  * 4G USB dongle
  * Smartphone tethering (USB/WiFi)
  * WiFi connection

  → Required to receive RTCM corrections from the network

* **Robot Platform**: *Antcar robot (or your platform)*

* **Connections**:

  * GNSS Receiver ↔ Raspberry Pi: USB or UART
  * Raspberry Pi ↔ Internet: WiFi / 4G / tethering

---

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
      │  RTCM corrections (via NTRIP)
      │
[Raspberry Pi 4B]
      ▲
      │
      │ Internet connection
      │ (WiFi / 4G / smartphone tethering)
      ▼
[Centipede RTK Network (caster)]
```

The Raspberry Pi:

* connects to the NTRIP caster
* receives RTCM correction data
* forwards corrections to the GNSS receiver
* reads corrected GNSS data
* publishes it to ROS topics

---

## RTK Corrections Setup (Centipede / NTRIP)

To achieve centimeter-level accuracy, the GNSS receiver must receive **RTCM correction data** from a nearby base station.

This project uses the Centipede RTK Network cited as:

ANCELIN Julien, Stefal, Julien, Simon Moinard, Wilthezin, François, & Romain Bazile. (2022). jancelin/docs-centipedeRTK: v2.4 (v2_4). Zenodo. https://doi.org/10.5281/zenodo.6760153

---

### Step 1 — Find a nearby base station

1. Open the Centipede-compatible map interface [Centipede Map](https://map.centipede-rtk.org/index.php/view/map/?repository=cent&project=centipede)
2. . Locate the closest **mountpoint** to your robot and save the informations for later

👉 Important:

* Distance should ideally be **< 30 km**
* Closer base = better accuracy and faster RTK convergence

---

### Step 2 — Identify mountpoint parameters

You will need:

* **Caster**: `caster.centipede.fr`
* **Port**: `2101`
* **Mountpoint**: (example: `LLENX`) Name of the base station
* **Username / Password**: typically `centipede`
* **REFLAT** = (example: `43.39376`)
* **REFLON** = (example: `5.17464`)
* **REFALT** = (example: `65.563`)
* 
---

### Step 3 — Configure your node

These parameters are defined in the Python node located at: `scripts/navpvt_pub.py`

```python
NTRIP_SERVER = "caster.centipede.fr"
NTRIP_PORT = 2101
MOUNTPOINT = "LLENX"
NTRIP_USER = "centipede"
NTRIP_PASSWORD = "centipede"
```

---

#### Reference position

```python
REFLAT = 43.39376
REFLON = 5.17464
REFALT = 65.563
```

---

### Step 4 — Verify RTK status

Expected transition:

* `NO FIX` → `FLOAT` → `RTK FIXED`

👉 Only **RTK FIXED** provides centimeter-level accuracy. On the Surveyor or other sparkfun board, the led blue should stop blinking or show cm level accuracy.

---

## ROS Node

The main node is:

```
navpvt_pub.py
```

### Function

This node:

* connects to the GNSS receiver via serial
* connects to the NTRIP caster
* forwards RTCM corrections to the receiver
* reads UBX `NAV-PVT` messages
* publishes them as a ROS topic

---

## Launch

Launch file:

```xml
<launch>
    <node pkg="gnss_rtk" type="navpvt_pub.py" name="rtk_node" output="screen" />
</launch>
```

Run:

```bash
roslaunch gnss_rtk startup_gnss_image.launch
```

---

## Published Topic

* `/navpvt_topic` (`gnss_rtk/navpvt`)

Contains:

* latitude / longitude
* height
* velocity (N/E/D)
* ground speed
* heading
* accuracy metrics

---

## Installation

```bash
cd ~/catkin_ws/src
git clone <your-repo>
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```

Install dependencies:

```bash
pip install pygnssutils numpy
```

---

## Usage

1. Connect GNSS receiver to Raspberry Pi
2. Connect antenna
3. Ensure internet access (WiFi / 4G / tethering)
4. Launch node

```bash
roslaunch gnss_rtk startup_gnss_image.launch
```

Check:

```bash
rostopic list
rostopic echo /navpvt_topic
```

---

## Troubleshooting

### No GNSS data

* Check `/dev/ttyUSB0`
* Verify baudrate
* Check USB connection

---

### No RTK FIX

* Check mountpoint
* Check internet connection
* Verify RTCM data is received

---

### Poor accuracy

* Improve antenna placement
* Ensure clear sky view
* Reduce multipath (metal, buildings)

---

### Node does not start

* Check ROS environment
* Verify package build
* Ensure script is executable

---

## Future Improvements

* Move to ROS 2 
* Move parameters to ROS launch file
* Add RTK status topic
* Integrate with `robot_localization`
* Add RViz visualization

---

## License

MIT License

---

## Author

*Gabriel Gattaux*

---
