# command_parser.py
from typing import Dict, List, Any, Optional


class CommandParser:
    """
    Parses a sequence of detected symbols (0-9, A-Z) into high-level commands.

    Supported commands (examples):
      - Motion: A, B, F, L, R, U, D
      - Subscribe: S 1 9 2 P 1 6 8 P 1 P 4 2  → {"type": "subscribe", "target": "192.168.1.42"}
      - Task: T F E T C H  → {"type": "task", "name": "FETCH"}
      - Converge: C 1 2 P 3 4  → {"type": "converge", "args": ["12", "34"]} (example encoding)
    """

    def __init__(self):
        pass

    def parse(self, symbols: List[str]) -> Optional[Dict[str, Any]]:
        """
        Parse a list of symbols into a command dict, or None if no valid command.
        """
        if not symbols:
            return None

        head = symbols[0]
        rest = symbols[1:]

        # Single-letter motion commands
        if len(symbols) == 1:
            return self._parse_motion_single(head)

        # Subscribe: S <digits and P>...
        if head == "S":
            return self._parse_subscribe(rest)

        # Task: T <letters>...
        if head == "T":
            return self._parse_task(rest)

        # Converge: C <digits and P>...
        if head == "C":
            return self._parse_converge(rest)

        # Fallback: try to interpret as motion if only one meaningful letter
        # (e.g., user showed F then noise)
        if len(symbols) == 2 and rest[0] in ("A", "B", "F", "L", "R", "U", "D"):
            return self._parse_motion_single(rest[0])

        return None

    def _parse_motion_single(self, symbol: str) -> Optional[Dict[str, Any]]:
        if symbol == "A":
            return {"type": "motion", "action": "stop"}
        if symbol == "B":
            return {"type": "motion", "action": "back"}
        if symbol == "F":
            return {"type": "motion", "action": "forward"}
        if symbol == "L":
            return {"type": "motion", "action": "left"}
        if symbol == "R":
            return {"type": "motion", "action": "right"}
        if symbol == "U":
            return {"type": "motion", "action": "up"}
        if symbol == "D":
            return {"type": "motion", "action": "down"}
        return None

    def _parse_subscribe(self, rest: List[str]) -> Optional[Dict[str, Any]]:
        """
        Example encoding:
          S 1 9 2 P 1 6 8 P 1 P 4 2
        P is treated as '.' separator.
        """
        parts = []
        current = []

        for s in rest:
            if s == "P":
                parts.append("".join(current))
                current = []
            elif s.isdigit():
                current.append(s)
            else:
                # Ignore non-digits in subscribe sequence
                pass

        if current:
            parts.append("".join(current))

        if not parts:
            return None

        ip = ".".join(parts)
        return {"type": "subscribe", "target": ip}

    def _parse_task(self, rest: List[str]) -> Optional[Dict[str, Any]]:
        """
        Example encoding:
          T F E T C H  → "FETCH"
        Only letters are used; digits are ignored.
        """
        name = "".join([s for s in rest if s.isalpha()])
        if not name:
            return None
        return {"type": "task", "name": name.upper()}

    def _parse_converge(self, rest: List[str]) -> Optional[Dict[str, Any]]:
        """
        Example encoding (you can redefine):
          C 1 2 P 3 4  → args = ["12", "34"]
        P is used as a separator between numeric groups.
        """
        parts = []
        current = []

        for s in rest:
            if s == "P":
                parts.append("".join(current))
                current = []
            elif s.isdigit():
                current.append(s)
            else:
                # Ignore non-digits in converge sequence
                pass

        if current:
            parts.append("".join(current))

        if not parts:
            return None

        return {"type": "converge", "args": parts}