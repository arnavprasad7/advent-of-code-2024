import json
import re

from icecream import ic

from aoc24.utils import DATA_DIR, load_txt_file


def load_data() -> str:
    data: str = load_txt_file(DATA_DIR / "day03" / "input.txt")
    return data


def part1() -> None:
    ic("part1")
    data: str = load_data()

    result: int = 0

    matches: list[str] = re.findall(r"mul\(\d+,\d+\)", data)

    for match in matches:
        match = match.replace("mul(", "").replace(")", "")
        int1, int2 = match.split(",")

        result += int(int1) * int(int2)

    ic(result)


def part2() -> None:
    ic("part2")
    data: str = load_data()

    result: int = 0

    matches: list[str] = re.findall(
        r"mul\(\d+,\d+\)|" r"do\(\)|" r"don\'t\(\)",
        data,
    )

    enabled: bool = True

    for match in matches:
        if match == "do()":
            enabled = True
        elif match == "don't()":
            enabled = False
        else:
            if enabled:
                match = match.replace("mul(", "").replace(")", "")
                int1, int2 = match.split(",")

                result += int(int1) * int(int2)

    ic(result)


def main() -> None:
    part1()
    part2()


if __name__ == "__main__":
    main()
