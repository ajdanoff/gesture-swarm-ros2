from gesture_swarm_ros2.ransac_filter import TemporalRansacParser

def test_motion_consensus():
    parser = TemporalRansacParser(inlier_ratio_thresh=0.6, min_buffer_size=5)

    # Strong F consensus
    buf = ["F", "F", "X", "F", "F", "F"]
    cmd = parser.evaluate_buffer(buf)
    print("Buffer:", buf, "=>", cmd)

    # Emergency stop override
    buf_stop = ["F", "F", "X", "A", "A"]
    cmd_stop = parser.evaluate_buffer(buf_stop)
    print("Buffer:", buf_stop, "=>", cmd_stop)

    # Task: T F E T C H
    buf_task = ["T", "F", "E", "T", "C", "H", "T", "H"]
    cmd_task = parser.evaluate_buffer(buf_task)
    print("Buffer:", buf_task, "=>", cmd_task)

if __name__ == "__main__":
    test_motion_consensus()