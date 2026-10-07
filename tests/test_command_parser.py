# test_command_parser.py
from command_parser import CommandParser


def run_test(parser: CommandParser, name: str, symbols: list):
    cmd = parser.parse(symbols)
    print(f"[{name}] symbols={symbols} => command={cmd}")


def main():
    parser = CommandParser()

    # Motion commands
    run_test(parser, "A (stop)", ["A"])
    run_test(parser, "B (back)", ["B"])
    run_test(parser, "F (forward)", ["F"])
    run_test(parser, "L (left)", ["L"])
    run_test(parser, "R (right)", ["R"])
    run_test(parser, "U (up)", ["U"])
    run_test(parser, "D (down)", ["D"])

    # Subscribe: 192.168.1.42
    run_test(
        parser,
        "Subscribe 192.168.1.42",
        ["S", "1", "9", "2", "P", "1", "6", "8", "P", "1", "P", "4", "2"],
    )

    # Task: FETCH
    run_test(
        parser,
        "Task FETCH",
        ["T", "F", "E", "T", "C", "H"],
    )

    # Task: PATROL
    run_test(
        parser,
        "Task PATROL",
        ["T", "P", "A", "T", "R", "O", "L"],
    )

    # Converge example: 12.34 (you can redefine semantics)
    run_test(
        parser,
        "Converge 12.34",
        ["C", "1", "2", "P", "3", "4"],
    )

    # Noise + valid command: F then noise, should still detect F if you want
    run_test(
        parser,
        "Noise then F",
        ["X", "F"],
    )


if __name__ == "__main__":
    main()