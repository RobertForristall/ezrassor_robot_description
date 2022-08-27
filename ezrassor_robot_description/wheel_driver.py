import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

from ezrassor_interfaces.msg import WheelCommand

class WheelDriver(Node):
    
    def __init__(self):
        super().__init__("wheel_driver")

        self.logger = self.get_logger()

        self.sub = self.create_subscription(
            WheelCommand,
            "wheel_command",
            self.handle_command,
            10
        )
        self.pub = self.create_publisher(
            Twist,
            "diff_drive_base_controller/cmd_vel_unstamped",
            10
        )

    def handle_command(self, msg):

        new_msg = Twist()

        if (msg.command == "drive"):
            new_msg.linear.x = msg.value
            self.pub.publish(new_msg)
        elif (msg.command == "turn"):
            new_msg.angular.z = msg.value
            self.pub.publish(new_msg)
        else:
            self.pub.publish(new_msg)

def main(args=None):

    try:
        rclpy.init(args=args)

        node = WheelDriver()
        node.logger.info("Wheel driver initalized...")

        rclpy.spin(node)
        node.logger.info("Wheel driver spinning...")
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()