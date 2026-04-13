#!/usr/bin/env python

import rospy
from gnss_rtk.msg import navpvt  # Import the NavPVT message type
from sensor_msgs.msg import NavSatFix  # Import the NavSatFix message type

def navpvt_callback(data):
    # Create a NavSatFix message
    navsatfix_msg = NavSatFix()
    # navsatfix_msg.header.stamp =  data.header.stamp
    navsatfix_msg.header.frame_id = "your_frame_id"
    navsatfix_msg.latitude = data.lat 
    navsatfix_msg.longitude = data.lon
    navsatfix_msg.altitude = data.height 
    navsatfix_msg.position_covariance = [float('nan')] * 9
    navsatfix_msg.position_covariance_type = NavSatFix.COVARIANCE_TYPE_UNKNOWN

    # Publish the NavSatFix message
    navsatfix_pub.publish(navsatfix_msg)

if __name__ == "__main__":
    # Initialize the ROS node
    rospy.init_node('navsatfix_publisher', anonymous=True)

    # Create a ROS subscriber for the NavPVT message
    rospy.Subscriber('/navpvt_topic', navpvt, navpvt_callback)

    # Create a ROS publisher for the NavSatFix message
    navsatfix_pub = rospy.Publisher('/navsatfix', NavSatFix, queue_size=1)

    # Spin ROS
    rospy.spin()
