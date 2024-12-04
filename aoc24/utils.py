from pathlib import Path


DATA_DIR = Path(__file__).parents[1] / "data"


def load_txt_file(filepath: Path) -> str:
    with open(filepath, "r") as f:
        return f.read()