# gesture_swarm_ros2/gesture_swarm_ros2/command_parser_node.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time

from .command_parser import CommandParser
from .symbol_filter import deduplicate_consecutive


class CommandParserNode(Node):
    def __init__(self):
        super().__init__("command_parser_node")

        self.subscription = self.create_subscription(
            String,
            "/gesture/symbol",
            self.symbol_callback,
            10,
        )

        self.command_pub = self.create_publisher(String, "/swarm/command", 10)

        self.parser = CommandParser()
        self.last_symbol_time = time.time()
        self.timeout = 1.5  # seconds

        self.current_symbols = []

        self.timer = self.create_timer(0.1, self.timer_callback)

    def symbol_callback(self, msg: String):
        symbol = msg.data.strip()
        if symbol:
            self.current_symbols.append(symbol)
            self.last_symbol_time = time.time()
            self.get_logger().info(f"Received symbol: {symbol}")

    def timer_callback(self):
        now = time.time()
        if now - self.last_symbol_time > self.timeout and self.current_symbols:
            # Deduplicate consecutive identical symbols
            filtered = deduplicate_consecutive(self.current_symbols, min_run=2)
            self.get_logger().info(f"Filtered symbols: {filtered}")

            cmd = self.parser.parse(filtered)
            if cmd:
                self.get_logger().info(f"Parsed command: {cmd}")
                msg = String()
                msg.data = repr(cmd)
                self.command_pub.publish(msg)
            else:
                self.get_logger().info(f"No command parsed from {filtered}")
            self.current_symbols = []


def main():
    rclpy.init()
    node = CommandParserNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()


if __name__ == "__main__":
    main()