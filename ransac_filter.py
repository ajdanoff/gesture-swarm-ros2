# gesture_swarm_ros2/gesture_swarm_ros2/ransac_filter.py
from typing import List, Optional, Dict, Any
import random

class TemporalRansacParser:
    def __init__(self, inlier_ratio_thresh: float = 0.60, min_buffer_size: int = 5):
        """
        Args:
            inlier_ratio_thresh: Minimum percentage of matching characters 
                                 needed to confirm a command (consensus).
            min_buffer_size: Minimum frames required before running evaluation.
        """
        self.inlier_ratio_thresh = inlier_ratio_thresh
        self.min_buffer_size = min_buffer_size
        
        # Valid single-character action definitions
        self.motion_map = {
            "A": "stop", "B": "back", "F": "forward", 
            "L": "left", "R": "right", "U": "up", "D": "down"
        }

    def evaluate_buffer(self, buffer: List[str]) -> Optional[Dict[str, Any]]:
        """
        Evaluates a noisy character buffer using a temporal consensus strategy.
        Returns a command dict immediately if consensus is reached, else None.
        """
        if len(buffer) < self.min_buffer_size:
            return None

        # --- Phase 1: High-Priority Short-Circuit (Emergency Stop) ---
        # If the last 2 frames are strictly 'A', override everything for safety.
        if len(buffer) >= 2 and buffer[-1] == "A" and buffer[-2] == "A":
            return {"type": "motion", "action": "stop"}

        # --- Phase 2: RANSAC Consensus Loop for Single-Letter Motions ---
        # Count frequencies within the current window
        total_elements = len(buffer)
        counts = {}
        for char in buffer:
            counts[char] = counts.get(char, 0) + 1

        # Check if any valid motion character has achieved consensus
        for char, count in counts.items():
            if char in self.motion_map:
                inlier_ratio = count / total_elements
                if inlier_ratio >= self.inlier_ratio_thresh:
                    # Consensus reached! Return the command model
                    return {"type": "motion", "action": self.motion_map[char]}

        # --- Phase 3: Consensus Loop for Complex String Commands (e.g., T F E T C H) ---
        # Look for prefix structural markers within the buffer window
        if "T" in buffer:
            # Calculate what percentage of non-noise characters are alphabetical
            letters = [c for c in buffer if c.isalpha() and c != "T"]
            if len(letters) >= 2: # Ensure we have enough frames to build a word
                # Extract unique characters in their relative order of appearance
                unique_word = []
                for c in letters:
                    if not unique_word or unique_word[-1] != c:
                        unique_word.append(c)
                word = "".join(unique_word).upper()
                return {"type": "task", "name": word}

        return None
