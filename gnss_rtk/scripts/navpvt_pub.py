#!/usr/bin/env python

import rospy
from gnss_rtk.msg import navpvt  # Import the NavPVT message type
from queue import Queue, Empty
from threading import Event
from time import sleep

from pygnssutils import VERBOSITY_LOW, GNSSNTRIPClient
from gnssapp import GNSSSkeletonApp
import numpy as np

CONNECTED = 1

if __name__ == "__main__":
    # Initialize the ROS node
    rospy.init_node('navpvt_publisher', anonymous=True)

    # Create a ROS publisher for the NavPVT message
    navpvt_pub = rospy.Publisher('navpvt_topic', navpvt, queue_size=1)

    # GNSS receivehhr serial port parameters - AMEND AS REQUIRED:
    SERIAL_PORT = "/dev/ttyUSB0"
    BAUDRATE = 460800
    TIMEOUT = 10

    # NTRIP caster parameters - AMEND AS REQUIRED:
    # Ideally, mountpoint should be <30 km from location.
    IPPROT = "IPv4"  # or "IPv6"
    NTRIP_SERVER = "caster.centipede.fr"
    NTRIP_PORT = 2101
    FLOWINFO = 0  # for IPv6
    SCOPEID = 0  # for IPv6
    MOUNTPOINT = "LLENX"  # leave blank to retrieve sourcetable
    NTRIP_USER = "centipede"
    NTRIP_PASSWORD = "centipede"

    # NMEA GGA sentence status - AMEND AS REQUIRED:
    GGAMODE = 1  # use fixed reference position (0 = use live position)
    GGAINT = -1  # interval in seconds (-1 = do not send NMEA GGA sentences)
    # Fixed reference coordinates (only used when GGAMODE = 1) - AMEND AS REQUIRED:
    REFLAT = 43.39376
    REFLON = 5.17464
    REFALT = 65.563
    REFSEP = 26.1743

    recv_queue = Queue()  # data from receiver placed on this queue
    send_queue = Queue()  # data to receiver placed on this queue
    stop_event = Event()
    idonly = True

    try:
        print(f"Starting GNSS reader/writer on {SERIAL_PORT} @ {BAUDRATE}...\n")
        with GNSSSkeletonApp(
            SERIAL_PORT,
            BAUDRATE,
            TIMEOUT,
            stopevent=stop_event,
            recvqueue=recv_queue,
            sendqueue=send_queue,
            idonly=idonly,
            enableubx=True,
            showhacc=True,
        ) as gna:
            gna.run()
            sleep(2)  # wait for receiver to output at least 1 navigation solution

            print(f"Starting NTRIP client on {NTRIP_SERVER}:{NTRIP_PORT}...\n")
            with GNSSNTRIPClient(gna, verbosity=VERBOSITY_LOW) as gnc:
                streaming = gnc.run(
                    ipprot=IPPROT,
                    server=NTRIP_SERVER,
                    port=NTRIP_PORT,
                    flowinfo=FLOWINFO,
                    scopeid=SCOPEID,
                    mountpoint=MOUNTPOINT,
                    ntripuser=NTRIP_USER,  # pygnssutils>=1.0.12
                    ntrippassword=NTRIP_PASSWORD,  # pygnssutils>=1.0.12
                    reflat=REFLAT,
                    reflon=REFLON,
                    refalt=REFALT,
                    refsep=REFSEP,
                    ggamode=GGAMODE,
                    ggainterval=GGAINT,
                    output=send_queue,  # send NTRIP data to receiver
                )

                while streaming and not stop_event.is_set():
                    if recv_queue is not None:
                        # consume any received GNSS data from queue
                        try:
                            while not recv_queue.empty():
                                (raw, parsed) = recv_queue.get(False)
                                if parsed.identity =="NAV-PVT":
                                    # Creating a NavPVT message
                                    navpvt_msg = navpvt()
                                    # navpvt_msg.header.stamp = rospy.Time.now()  # Add timestamp
                                    navpvt_msg.iTOW = parsed.iTOW
                                    navpvt_msg.year = parsed.year
                                    navpvt_msg.month = parsed.month
                                    navpvt_msg.day = parsed.day
                                    navpvt_msg.hour = parsed.hour
                                    navpvt_msg.min = parsed.min
                                    navpvt_msg.sec = parsed.second
                                    #navpvt_msg.valid = parsed.valid
                                    #navpvt_msg.tAcc = parsed.tAcc
                                    #navpvt_msg.nano = parsed.nano
                                    #navpvt_msg.fixType = parsed.fixType
                                    #navpvt_msg.flags = parsed.flags
                                    #navpvt_msg.flags2 = parsed.flags2
                                    #navpvt_msg.numSV = parsed.numSV
                                    navpvt_msg.lon = np.float32(parsed.lon)
                                    navpvt_msg.lat = np.float32(parsed.lat)
                                    navpvt_msg.height = np.float32(parsed.height)
                                    navpvt_msg.hMSL = parsed.hMSL
                                    navpvt_msg.hAcc = parsed.hAcc
                                    navpvt_msg.vAcc = parsed.vAcc
                                    navpvt_msg.velN = parsed.velN
                                    navpvt_msg.velE = parsed.velE
                                    navpvt_msg.velD = parsed.velD
                                    navpvt_msg.gSpeed = parsed.gSpeed
                                    navpvt_msg.heading = parsed.headMot
                                    navpvt_msg.sAcc = parsed.sAcc
                                    navpvt_msg.headAcc = parsed.headAcc
                                    navpvt_msg.pDOP = parsed.pDOP
                                    navpvt_msg.headVeh = parsed.headVeh
                                    navpvt_msg.magDec = parsed.magDec
                                    navpvt_msg.magAcc = parsed.magAcc

                                    # Publish the NavPVT message
                                    navpvt_pub.publish(navpvt_msg)

                                recv_queue.task_done()
                        except Empty:
                            pass
                    sleep(1)
                sleep(1)

    except KeyboardInterrupt:
        stop_event.set()
        print("Terminated by user")
