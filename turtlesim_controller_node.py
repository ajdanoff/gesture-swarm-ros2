# gesture_swarm_ros2/gesture_swarm_ros2/turtlesim_controller_node.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import json  # Fixed: Standard JSON parsing instead of ast


class TurtlesimControllerNode(Node):
    def __init__(self):
        super().__init__("turtlesim_controller_node")

        self.subscription = self.create_subscription(
            String,
            "/swarm/command",
            self.command_callback,
            10,
        )

        self.cmd_vel_pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)

        self.linear_speed = 2.0
        self.angular_speed = 2.0

    def command_callback(self, msg: String):
        raw = msg.data.strip()
        self.get_logger().info(f"Received command raw: {raw}")

        # Fixed: Enforce strict JSON deserialization
        try:
            cmd = json.loads(raw)
        except json.JSONDecodeError as e:
            self.get_logger().error(f"Malformed JSON payload dropped: {raw}. Error: {e}")
            return

        if not isinstance(cmd, dict):
            self.get_logger().warning(f"Invalid command format (expected dict): {cmd}")
            return

        twist = Twist()

        if cmd.get("type") == "motion":
            action = cmd.get("action")
            if action == "forward":
                twist.linear.x = self.linear_speed
            elif action == "back":
                twist.linear.x = -self.linear_speed
            elif action == "left":
                twist.angular.z = self.angular_speed
            elif action == "right":
                twist.angular.z = -self.angular_speed
            elif action == "stop":
                twist.linear.x = 0.0
                twist.angular.z = 0.0
            elif action == "up":
                self.get_logger().info("Up command recognized.")
            elif action == "down":
                self.get_logger().info("Down command recognized.")
        else:
            self.get_logger().info(f"Non-motion command passed to actuator: {cmd}")

        self.cmd_vel_pub.publish(twist)


def main():
    rclpy.init()
    node = TurtlesimControllerNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()


if __name__ == "__main__":
    main()
