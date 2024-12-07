import itertools
from enum import Enum

from icecream import ic
from tqdm import tqdm

from aoc24.utils import DATA_DIR, load_txt_file


class Operation(Enum):
    ADD = "+"
    MULTIPLY = "*"
    CONCATENATE = "||"

    def compute(self, a: int, b: int) -> int:
        match self:
            case Operation.ADD:
                return a + b
            case Operation.MULTIPLY:
                return a * b
            case Operation.CONCATENATE:
                return int(str(a) + str(b))
        raise ValueError(f"Unknown operation: {self}")


class Equation:
    def __init__(self, *, result: int, values: list[int]) -> None:
        self.result: int = result
        self.values: list[int] = values
        self.correct_operation_order: list[Operation] | None = None
        self.is_possible: bool = False

    def __repr__(self) -> str:
        return f"Equation(result={self.result}, values={self.values})"

    def get_possibility(
        self,
        *,
        available_operations: set[Operation],
        render_correct: bool = False,
        debug: bool = False,
    ) -> bool:

        operation_combinations = itertools.product(
            available_operations, repeat=len(self.values) - 1
        )

        if debug:
            ic(self.result, self.values)
            ic(operation_combinations)

        for operations in operation_combinations:

            result: int = self.values[0]
            for i, value in enumerate(self.values[1:]):
                result = operations[i].compute(result, value)

            if result == self.result:
                self.is_possible = True
                self.correct_operation_order = list(operations)
                if render_correct:
                    print("Operation is possible:")
                    self.render(operations)
                    print()
                return True

        return False

    def render(self, operations: tuple[Operation, ...]) -> None:
        equation: str = f"{self.result} = {self.values[0]}"
        for i, value in enumerate(self.values[1:]):
            equation += f" {operations[i].value} {value}"
        print(equation)


def load_data() -> list[Equation]:
    data: str = load_txt_file(DATA_DIR / "day07" / "input.txt")

    equations: list[Equation] = []

    for line in data.splitlines():
        result, values = line.split(": ")
        equations.append(
            Equation(
                result=int(result),
                values=[int(v) for v in values.split(" ")],
            )
        )

    return equations


def part1() -> None:
    ic("part1")
    equations: list[Equation] = load_data()
    ic(equations)

    possible_equations: list[Equation] = []

    available_operations: set[Operation] = {
        Operation.ADD,
        Operation.MULTIPLY,
    }

    for equation in tqdm(equations):
        if equation.get_possibility(
            available_operations=available_operations,
            render_correct=False,
            debug=False,
        ):
            possible_equations.append(equation)

    ic(possible_equations)

    result: int = sum(equation.result for equation in possible_equations)

    ic(result)


def part2() -> None:
    ic("part2")
    equations: list[Equation] = load_data()

    possible_equations: list[Equation] = []

    available_operations: set[Operation] = {
        Operation.ADD,
        Operation.MULTIPLY,
        Operation.CONCATENATE,
    }

    for equation in tqdm(equations):
        if equation.get_possibility(
            available_operations=available_operations,
            render_correct=False,
            debug=False,
        ):
            possible_equations.append(equation)

    ic(possible_equations)

    result: int = sum(equation.result for equation in possible_equations)

    ic(result)


def main() -> None:
    part1()
    part2()


if __name__ == "__main__":
    main()
