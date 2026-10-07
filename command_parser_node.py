# gesture_swarm_ros2/gesture_swarm_ros2/command_parser_node.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json

from .ransac_filter import TemporalRansacParser


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

        # Initialize the RANSAC temporal processor
        self.ransac_parser = TemporalRansacParser(inlier_ratio_thresh=0.65, min_buffer_size=6)
        
        # Sliding history window
        self.buffer_window = []
        self.max_window_size = 15  # Keeps a rolling history of the last ~0.75 seconds of data

    def symbol_callback(self, msg: String):
        symbol = msg.data.strip().upper()
        if not symbol:
            return  # Skip empty camera frames entirely

        # Append to our sliding window history
        self.buffer_window.append(symbol)
        if len(self.buffer_window) > self.max_window_size:
            self.buffer_window.pop(0)

        # Run RANSAC evaluation instantly on the rolling window
        cmd = self.ransac_parser.evaluate_buffer(self.buffer_window)
        
        if cmd:
            self.get_logger().info(f"RANSAC Consensus Met! Command: {cmd} | Window: {self.buffer_window}")
            
            # Publish immediately
            out_msg = String()
            out_msg.data = json.dumps(cmd)
            self.command_pub.publish(out_msg)
            
            # Flush buffer window completely upon successful execution to avoid double-triggers
            self.buffer_window.clear()


def main():
    rclpy.init()
    node = CommandParserNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()


if __name__ == "__main__":
    main()
