from collections import Counter

from icecream import ic

from aoc24.utils import DATA_DIR, load_txt_file


def load_data() -> tuple[list[int], list[int]]:
    data: str = load_txt_file(DATA_DIR / "day01" / "input.txt")
    list1: list[int] = []
    list2: list[int] = []

    for line in data.split("\n"):
        list1.append(int(line.split()[0]))
        list2.append(int(line.split()[1]))

    return list1, list2


def part1() -> None:
    ic("part1")
    list1, list2 = load_data()
    list1 = sorted(list1)
    list2 = sorted(list2)

    distance: int = 0
    for i in range(len(list1)):
        distance += abs(list1[i] - list2[i])

    ic(distance)


def part2() -> None:
    ic("part2")
    list1, list2 = load_data()

    score: int = 0

    counter = Counter(list2)

    for number in list1:
        count: int = counter[number]
        if count > 0:
            score += count * number

    ic(score)


def main() -> None:
    part1()
    part2()


if __name__ == "__main__":
    main()
