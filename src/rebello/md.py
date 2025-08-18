from pathlib import Path

from .models import Board


def render_board(path: Path, board: Board):
    with path.open("w") as f:
        f.write(f"# {board.title}\n")

        for col in board.columns:
            f.write("\n")
            f.write(f"## {col.title}\n")
            f.write("\n")

            for card in col.cards:
                f.write(f"* [{card.id}] {card.title}\n")
