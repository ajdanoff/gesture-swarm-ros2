# gesture_swarm_ros2/gesture_swarm_ros2/turtlesim_controller_node.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import ast


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

        # Try JSON first
        import json
        try:
            cmd = json.loads(raw)
        except Exception:
            # Fallback: use ast.literal_eval for Python dict-like strings
            try:
                cmd = ast.literal_eval(raw)
            except Exception:
                self.get_logger().warning(f"Invalid command (parse error): {raw}")
                return

        if not isinstance(cmd, dict):
            self.get_logger().warning(f"Invalid command (not a dict): {cmd}")
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
                self.get_logger().info("Up command (could map to color change).")
            elif action == "down":
                self.get_logger().info("Down command.")
        else:
            self.get_logger().info(f"Received command: {cmd}")

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