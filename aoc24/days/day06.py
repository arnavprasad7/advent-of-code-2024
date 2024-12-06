from copy import deepcopy
from enum import Enum
from typing import Self

from icecream import ic
from tqdm import tqdm

from aoc24.utils import DATA_DIR, load_txt_file

Location = tuple[int, int]


class OutOfGridError(Exception): ...


class GuardInLoopError(Exception): ...


class GridObject(Enum):
    EMPTY = "."
    OBSTACLE = "#"
    GUARD = "^"


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @property
    def right_turn_90_deg(self) -> Self:
        match self:
            case self.UP:
                return self.RIGHT
            case self.RIGHT:
                return self.DOWN
            case self.DOWN:
                return self.LEFT
            case self.LEFT:
                return self.UP

        raise ValueError("Not a valid direction")


class Grid(dict[Location, GridObject]):

    DEFAULT_GUARD_DIRECTION: Direction = Direction.UP

    def __init__(self) -> None:
        super().__init__()
        self.guard_location: Location | None = None
        self.guard_direction: Direction = self.DEFAULT_GUARD_DIRECTION
        self.num_steps: int = 1
        self.distinct_locations: set[Location] = set()
        self.direction_location_combos: set[tuple[Direction, Location]] = set()

    def move_guard(self, stop_on_loop: bool = False) -> None:

        self.set_valid_guard_direction(stop_on_loop=stop_on_loop)

        guard_location: Location = self.get_guard_location()
        guard_direction: Direction = self.get_guard_direction()

        new_location: Location = (
            guard_location[0] + guard_direction.value[0],
            guard_location[1] + guard_direction.value[1],
        )

        self[guard_location] = GridObject.EMPTY
        self[new_location] = GridObject.GUARD

        self.guard_location = new_location
        self.num_steps += 1
        self.distinct_locations.add(new_location)
        self.direction_location_combos.add((guard_direction, new_location))

    def set_valid_guard_direction(self, stop_on_loop: bool) -> bool:
        guard_location: Location = self.get_guard_location()
        guard_direction: Direction = self.get_guard_direction()

        new_location: Location = (
            guard_location[0] + guard_direction.value[0],
            guard_location[1] + guard_direction.value[1],
        )

        if (guard_direction, new_location) in self.direction_location_combos:
            raise GuardInLoopError("Guard is in a loop")

        if self.get(new_location, None) == GridObject.EMPTY:
            return True

        if new_location not in self:
            raise OutOfGridError("Next step is out of bounds")

        self.guard_direction = self.guard_direction.right_turn_90_deg

        if not self.set_valid_guard_direction(stop_on_loop=stop_on_loop):
            self.set_valid_guard_direction(stop_on_loop=stop_on_loop)

        return False

    def get_guard_location(self) -> Location:
        if self.guard_location is not None:
            return self.guard_location

        for location, grid_object in self.items():
            if grid_object == GridObject.GUARD:
                self.guard_location = location
                self.distinct_locations.add(location)
                self.direction_location_combos.add(
                    (self.DEFAULT_GUARD_DIRECTION, location)
                )
                return location

        raise ValueError("Guard not found")

    def get_guard_direction(self) -> Direction:
        if self.guard_direction is not None:
            return self.guard_direction
        return self.guard_direction

    @property
    def num_distinct_locations(self) -> int:
        return len(self.distinct_locations)

    @property
    def width(self) -> int:
        return max(x for x, _ in self.keys())

    @property
    def height(self) -> int:
        return max(y for _, y in self.keys())

    def show(self) -> None:
        for y in range(self.height + 1):
            row: str = "|"
            for x in range(self.width + 1):
                grid_object: GridObject = self[(x, y)]
                row += grid_object.value
                row += "|"
            print(row)
        print()


def load_data() -> Grid:
    data: str = load_txt_file(DATA_DIR / "day06" / "input.txt")

    grid = Grid()

    for y, line in enumerate(data.split("\n")):
        for x, char in enumerate(line):
            grid[(x, y)] = GridObject(char)

    return grid


def part1() -> None:
    ic("part1")
    grid: Grid = load_data()

    try:
        while True:
            grid.move_guard()
    except OutOfGridError:
        result: int = grid.num_distinct_locations
        ic(result)
        ic(f"Moved {grid.num_steps} steps")


def part2() -> None:
    ic("part2")
    grid: Grid = load_data()

    num_loop_positions: int = 0

    for location in tqdm(grid):

        if grid[location] != GridObject.EMPTY:
            continue

        test_grid: Grid = deepcopy(grid)
        test_grid[location] = GridObject.OBSTACLE

        try:
            while True:
                test_grid.move_guard()

        except GuardInLoopError:
            ic(f"Found loop position ({location})")
            num_loop_positions += 1
            continue

        except OutOfGridError:
            continue

    ic(num_loop_positions)


def main() -> None:
    part1()
    part2()


if __name__ == "__main__":
    main()
