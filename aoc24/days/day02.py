from icecream import ic

from aoc24.utils import DATA_DIR, load_txt_file


def load_data() -> list[list[int]]:
    data: str = load_txt_file(DATA_DIR / "day02" / "input.txt")

    reports: list[list[int]] = []

    for report in data.split("\n"):
        reports.append([int(x) for x in report.split()])

    return reports


def is_monotonic(report: list[int]) -> bool:
    monotonic_increasing: bool = all(
        report[i] <= report[i + 1] for i in range(len(report) - 1)
    )

    monotonic_decreasing: bool = all(
        report[i] >= report[i + 1] for i in range(len(report) - 1)
    )

    return monotonic_increasing or monotonic_decreasing


def adjacent_levels_check(report: list[int]) -> bool:
    for i in range(len(report) - 1):
        diff: int = abs(report[i] - report[i + 1])
        if diff < 1 or diff > 3:
            return False
    return True


def is_report_valid(report: list[int]) -> bool:
    return is_monotonic(report) and adjacent_levels_check(report)


def is_valid_with_problem_dampener(report: list[int]) -> bool:

    for i, level in enumerate(report):
        adjusted_report: list[int] = report.copy()
        adjusted_report.pop(i)

        if is_report_valid(adjusted_report):
            return True

    return False


def part1() -> None:
    ic("part1")
    reports: list[list[int]] = load_data()

    num_safe: int = 0

    for report in reports:
        if is_report_valid(report):
            num_safe += 1

    ic(num_safe)


def part2() -> None:
    ic("part2")
    reports: list[list[int]] = load_data()

    num_safe: int = 0

    for report in reports:
        if is_report_valid(report):
            num_safe += 1
        else:
            if is_valid_with_problem_dampener(report):
                num_safe += 1

    ic(num_safe)


def main() -> None:
    part1()
    part2()


if __name__ == "__main__":
    main()
