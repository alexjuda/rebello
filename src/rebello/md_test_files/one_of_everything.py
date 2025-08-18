from rebello.models import Board, Card, Column

board = Board(
    id="1",
    title="One of everything",
    columns=[
        Column(
            id="2",
            title="Col",
            cards=[
                Card(id="3", title="Say hello"),
            ],
        ),
    ],
)
