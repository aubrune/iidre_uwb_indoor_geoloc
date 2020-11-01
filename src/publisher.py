#!/usr/bin/env python3
import time, serial, rospy
from tf import TransformBroadcaster

class UwbXyzPublisher(object):
    def __init__(self):
        rospy.init_node("iidre_uwb_wyz_publisher")
        self.tfb = TransformBroadcaster()
        self.device_name = rospy.get_param("name", "uwb")
        self.device_port = rospy.get_param("port", "/dev/ttyACM0")
        self.device_frame_id = rospy.get_param("frame_id", "map")
    
    def connect(self):
        rospy.loginfo("Connecting to {}...".format(self.device_port))
        self.serial = serial.Serial(self.device_port)
        rospy.loginfo("Connected! Now publishing tf frame '{}' in frame '{}'...".format(self.device_name, self. device_frame_id))

    def run(self):
        while not rospy.is_shutdown():
            line = self.serial.readline().decode("ascii")
            try:
                self.parse_and_publish(line)
            except (ValueError, IndexError):
                # Ignore the frame in case of any parsing error
                rospy.loginfo("Error when parsing a frame from serial")

    def parse_and_publish(self, line):
        fb = line.split(":")
        fb_cmd = fb[0]
        fb_data = fb[1].replace("\r\n","").split(",")
        time = fb_data[0]
        
        if fb_cmd == "+DIST":
            # This is usable even if the device has not been preconfigured with the uwbSupervisor
            # Just triangulate the distance (not done here)
            anchor_id = fb_data[1]
            anchor_dist = fb_data[2]
            anchor_xyz = fb_data[3:6]
        
        elif fb_cmd == "+MPOS":
            # This is usable if device has been preconfigured with the uwbSupervisor
            x, y, z = fb_data[1:4]
            # Convert from centimeters (in the JSON infra file) to meters
            x_m, y_m, z_m = map(lambda x: float(x)/100, [x, y, z])

            self.tfb.sendTransform(
                (x_m, y_m, z_m), (0, 0, 0, 1),   # device position, quaternion
                rospy.Time.now(),
                self.device_name,
                self.device_frame_id)

if __name__ == "__main__":
    node = UwbXyzPublisher()
    node.connect()
    node.run()