# gesture_swarm_ros2/gesture_swarm_ros2/symbol_filter.py
from typing import List


def deduplicate_consecutive(symbols: List[str], min_run: int = 2) -> List[str]:
    """
    Collapse consecutive runs of the same symbol into a single occurrence,
    but only if the run length is >= min_run.

    Example:
      ["F","F","F","B","B","A"] -> ["F","B","A"]
      ["F","B","F"]              -> ["F","B","F"]  (no runs >= min_run)
    """
    if not symbols:
        return []

    result = []
    current = symbols[0]
    count = 1

    for s in symbols[1:]:
        if s == current:
            count += 1
        else:
            if count >= min_run:
                result.append(current)
            else:
                # Treat short runs as noise and expand them as-is
                result.extend([current] * count)
            current = s
            count = 1

    # Last run
    if count >= min_run:
        result.append(current)
    else:
        result.extend([current] * count)

    return result