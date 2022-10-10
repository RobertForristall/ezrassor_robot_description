# Drum arm driver for the ezrassor rover in gazebo simulation
# Used to simplify command calls to each joint
# Written by Robert Forristall

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64, Float64MultiArray

# Main driver class
class DrumArmDriver(Node):

    def __init__(self):
        super().__init__("drum_arm_driver")

        self.logger = self.get_logger()
        
        # Front arm subscriber and publisher
        self.front_sub = self.create_subscription(
            Float64,
            "drum_arm_front_command",
            self.handle_front_command,
            10
        )
        self.front_pub = self.create_publisher(
            Float64MultiArray,
            "/arm_front_controller/commands",
            10
        )

        # Back drum arm subscriber and publisher
        self.back_sub = self.create_subscription(
            Float64,
            "drum_arm_back_command",
            self.handle_back_command,
            10
        )
        self.back_pub = self.create_publisher(
            Float64MultiArray,
            "/arm_back_controller/commands",
            10
        )

    # Subscriber callback functions to publish to the ros2 controller
    def handle_front_command(self, msg):
        new_msg = Float64MultiArray()
        new_msg.data = [msg.data]
        self.front_pub.publish(new_msg)

    def handle_back_command(self, msg):
        new_msg = Float64MultiArray()
        new_msg.data = [msg.data]
        self.back_pub.publish(new_msg)

# Entry point of node
def main(args=None):

    try:
        rclpy.init(args=args)
        node = DrumArmDriver()
        node.logger.info("Drum arm driver initalized...")
        rclpy.spin(node)
        node.logger.info("Drum arm driver spinning...")
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
