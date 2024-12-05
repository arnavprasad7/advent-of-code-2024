from icecream import ic

from aoc24.utils import DATA_DIR, load_txt_file


def load_data() -> tuple[dict[int, set[int]], list[list[int]]]:
    data: str = load_txt_file(DATA_DIR / "day05" / "input.txt")
    section1, section2 = data.split("\n\n")

    # dictionary mapping numbers that CANNOT be put after
    rules: dict[int, set[int]] = {}
    for rule in section1.splitlines():
        num1, num2 = (int(num) for num in rule.split("|"))

        if num2 not in rules:
            rules[num2] = set()

        rules[num2].add(num1)

    updates: list[list[int]] = []
    for update in section2.splitlines():
        updates.append([int(num) for num in update.split(",")])

    return rules, updates


def is_update_valid(update: list[int], *, rules: dict[int, set[int]]) -> bool:
    for i, page in enumerate(update):
        invalid_pages: set[int] = rules.get(page, set())
        if any(page_num in invalid_pages for page_num in update[i + 1 :]):
            return False
    return True


def get_page_weight(page: int, *, update: list[int], rules: dict[int, set[int]]) -> int:
    invalid_pages: set[int] = rules.get(page, set())

    page_weight: int = 0

    for other_page in update:
        if other_page in invalid_pages:
            page_weight += 1

    return page_weight


def part1() -> None:
    ic("part1")
    rules, updates = load_data()

    valid_updates: list[list[int]] = []
    for update in updates:
        if is_update_valid(update, rules=rules):
            valid_updates.append(update)

    result: int = 0
    for update in valid_updates:
        middle_page: int = update[len(update) // 2]
        result += middle_page

    ic(result)


def part2() -> None:
    ic("part2")
    rules, updates = load_data()

    invalid_updates: list[list[int]] = []
    for update in updates:
        if not is_update_valid(update, rules=rules):
            invalid_updates.append(update)

    corrected_updates: list[list[int]] = []
    for update in invalid_updates:

        page_weights: dict[int, int] = {
            page: get_page_weight(
                page,
                update=update,
                rules=rules,
            )
            for page in update
        }

        corrected_update: list[int] = sorted(update, key=lambda x: page_weights[x])
        corrected_updates.append(corrected_update)

    result: int = 0
    for update in corrected_updates:
        middle_page: int = update[len(update) // 2]
        result += middle_page

    ic(result)


def main() -> None:
    part1()
    part2()


if __name__ == "__main__":
    main()
