import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64, Float64MultiArray

class DrumDriver(Node):

    def __init__(self):
        super().__init__("drum_driver")

        self.logger = self.get_logger()

        self.front_sub = self.create_subscription(
            Float64,
            "drum_front_command",
            self.handle_front_command,
            10
        )
        self.front_pub = self.create_publisher(
            Float64MultiArray,
            "/drum_front_controller/commands",
            10   
        )

        self.back_sub = self.create_subscription(
            Float64,
            "drum_back_command",
            self.handle_back_command,
            10
        )
        self.back_pub = self.create_publisher(
            Float64MultiArray,
            "/drum_back_controller/commands",
            10   
        )
    
    def handle_front_command(self, msg):
        new_msg = Float64MultiArray()
        new_msg.data = [msg.data]
        self.front_pub.publish(new_msg)

    def handle_back_command(self, msg):
        new_msg = Float64MultiArray()
        new_msg.data = [msg.data]
        self.back_pub.publish(new_msg)

def main(args=None):

    try:
        rclpy.init(args=args)

        node = DrumDriver()
        node.logger.info("Drum driver initalized...")

        rclpy.spin(node)
        node.logger.info("Drum driver spinning...")
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()