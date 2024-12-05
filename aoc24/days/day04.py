import re

from icecream import ic

from aoc24.utils import DATA_DIR, load_txt_file

Matrix = list[list[str]]


def load_data() -> Matrix:
    data: str = load_txt_file(DATA_DIR / "day04" / "input.txt")
    matrix: Matrix = []
    for line in data.split("\n"):
        matrix.append(list(line))
    return matrix


def display_matrix(matrix: Matrix) -> None:
    print()
    for row in matrix:
        print("|".join(row))
    print()


def get_keyword_count(string: str) -> int:
    # need overlapping matches (?=...)
    return len(re.findall(r"(?=XMAS|SAMX)", string))


def get_horizontal_strings(matrix: Matrix) -> list[str]:
    horizontal_strings: list[str] = []

    for row in matrix:
        string: str = "".join(row)
        horizontal_strings.append(string)

    return horizontal_strings


def get_vertical_strings(matrix: Matrix) -> list[str]:
    vertical_strings: list[str] = []

    num_cols: int = len(matrix[0])

    for i in range(num_cols):
        string: str = ""
        for j in range(len(matrix)):
            string += matrix[j][i]
        vertical_strings.append(string)

    return vertical_strings


def get_declining_diagonal_strings(matrix: Matrix) -> list[str]:
    declining_diagonal_strings: list[str] = []

    num_rows: int = len(matrix)
    num_cols: int = len(matrix[0])

    for col_index in range(num_cols):
        string: str = ""
        for row_index in range(num_rows):
            if col_index + row_index >= num_cols:
                break
            string += matrix[row_index][col_index + row_index]
        declining_diagonal_strings.append(string)

    for row_index in range(1, num_rows):
        string = ""
        for col_index in range(num_cols):
            if row_index + col_index >= num_rows:
                break
            string += matrix[row_index + col_index][col_index]
        declining_diagonal_strings.append(string)

    return declining_diagonal_strings


def get_inclining_diagonal_strings(matrix: Matrix) -> list[str]:
    inclining_diagonal_strings: list[str] = []

    num_rows: int = len(matrix)
    num_cols: int = len(matrix[0])

    for col_index in range(num_cols):
        string = ""
        for row_index in range(num_rows):
            if col_index - row_index < 0:
                break
            string += matrix[row_index][col_index - row_index]
        inclining_diagonal_strings.append(string)

    for row_index in range(1, num_rows):
        string = ""
        for col_index in reversed(range(num_cols)):
            if num_cols - 1 - col_index + row_index >= num_rows:
                break
            string += matrix[num_cols - 1 - col_index + row_index][col_index]
        inclining_diagonal_strings.append(string)

    return inclining_diagonal_strings


def get_reverse_diagonal_word_positive_intercept(
    *, matrix: Matrix, x_intercept: int, span_loc: int
) -> str:

    string: str = ""

    x_start: int = span_loc
    y_start: int = abs(x_intercept) + span_loc + 2

    string += matrix[x_start][y_start]
    string += matrix[x_start + 1][y_start - 1]
    string += matrix[x_start + 2][y_start - 2]

    return string


def get_reverse_diagonal_word_negative_intercept(
    *, matrix: Matrix, x_intercept: int, span_loc: int
) -> str:

    string: str = ""

    x_start: int = abs(x_intercept) + span_loc
    y_start: int = span_loc + 2

    string += matrix[x_start][y_start]
    string += matrix[x_start + 1][y_start - 1]
    string += matrix[x_start + 2][y_start - 2]

    return string


def part1() -> None:
    ic("part1")
    matrix: Matrix = load_data()

    strings: list[str] = (
        get_horizontal_strings(matrix)
        + get_vertical_strings(matrix)
        + get_declining_diagonal_strings(matrix)
        + get_inclining_diagonal_strings(matrix)
    )

    result: int = sum(get_keyword_count(string) for string in strings)

    ic(result)


def part2() -> None:
    ic("part2")
    matrix: Matrix = load_data()
    display_matrix(matrix)

    num_cols: int = len(matrix[0])

    declining_diagonal_strings: list[str] = get_declining_diagonal_strings(matrix)

    x_intercepts: list[int] = list(range(num_cols)) + list(range(-1, -num_cols, -1))

    diagonal_string_coords: list[tuple[str, int]] = list(
        zip(
            declining_diagonal_strings,
            x_intercepts,
            strict=True,
        )
    )

    result: int = 0

    for string, x_intercept in diagonal_string_coords:

        if x_intercept >= 0:
            word_func = get_reverse_diagonal_word_positive_intercept
        else:
            word_func = get_reverse_diagonal_word_negative_intercept

        matches: list[re.Match] = list(re.finditer(r"(?=MAS|SAM)", string))
        if matches:
            ic(string, x_intercept)

        for match in matches:
            span_loc: int = match.span()[0]

            word: str = word_func(
                matrix=matrix,
                x_intercept=x_intercept,
                span_loc=span_loc,
            )

            ic(span_loc, x_intercept, match, word)
            if word == "SAM" or word == "MAS":
                result += 1

    ic(result)


def main() -> None:
    part1()
    part2()


if __name__ == "__main__":
    main()
