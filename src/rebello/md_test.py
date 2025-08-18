import pytest
from pathlib import Path
import importlib

from .models import Board
from .md import render_board


TEST_PKG = "rebello.md_test_files"
TEST_DIR = Path(__file__).parent / "md_test_files"


class TestRenderBoard:
    @staticmethod
    @pytest.mark.parametrize(
        "example_name",
        [
            "no_cols",
            "one_of_everything",
            "simple_kanban",
        ],
    )
    def test_output(example_name: str, tmp_path: Path):
        input_module = importlib.import_module(f"{TEST_PKG}.{example_name}")
        board: Board = input_module.board
        ref_out = (TEST_DIR / (example_name + ".md")).read_text()
        out_file = tmp_path / "out.md"

        render_board(out_file, board)

        rendered_text = out_file.read_text()
        assert rendered_text == ref_out
