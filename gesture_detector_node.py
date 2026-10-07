# gesture_swarm_ros2/gesture_swarm_ros2/gesture_detector_node.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import cv2
from ultralytics import YOLO

class GestureDetectorNode(Node):
    def __init__(self):
        super().__init__("gesture_detector_node")

        model_path = self.declare_parameter(
            "model_path",
            "/home/robot/gesture_ws/models/asl_unified_webcam_yolo11n_mp_best.pt",
        ).value

        self.conf_thresh = self.declare_parameter("conf_thresh", 0.75).value
        self.iou_thresh = self.declare_parameter("iou_thresh", 0.45).value
        self.camera_id = self.declare_parameter("camera_id", 0).value

        self.model = YOLO(model_path)

        self.publisher = self.create_publisher(String, "/gesture/symbol", 10)
        self.cap = cv2.VideoCapture(self.camera_id)
        
        # Optimize internal frame size configurations to limit matrix processing overhead
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.timer = self.create_timer(0.05, self.timer_callback)  # ~20 Hz

    def timer_callback(self):
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().error("Failed to grab video frame.")
            return

        results = self.model(frame, conf=self.conf_thresh, iou=self.iou_thresh, verbose=False)
        boxes = results[0].boxes

        if len(boxes) > 0:
            idx = int(boxes.conf.argmax())
            cls = int(boxes.cls[idx])
            conf = float(boxes.conf[idx])
            symbol = self.model.names[cls]
            self.get_logger().info(f"Detected: {symbol} (conf={conf:.2f})")
            
            # Fixed: Only publish when a valid token is found.
            # This keeps the pipeline clean and prevents empty messages from resetting timeouts.
            msg = String()
            msg.data = symbol
            self.publisher.publish(msg)

    def destroy_node(self):
        self.cap.release()
        super().destroy_node()


def main():
    rclpy.init()
    node = GestureDetectorNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()


if __name__ == "__main__":
    main()
