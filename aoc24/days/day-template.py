from icecream import ic

from aoc24.utils import DATA_DIR, load_txt_file


def load_data() -> str:
    data: str = load_txt_file(DATA_DIR / "day-template" / "example.txt")
    return data


def part1() -> None:
    ic("part1")


def part2() -> None:
    ic("part2")


def main() -> None:
    part1()
    part2()


if __name__ == "__main__":
    main()
