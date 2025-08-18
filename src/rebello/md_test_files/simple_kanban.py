from rebello.models import Board, Card, Column

board = Board(
    id="1",
    title="Simple kanban",
    columns=[
        Column(
            id="2",
            title="To Do",
            cards=[
                Card(id="21", title="Say hello"),
                Card(id="22", title="Say goodnight"),
            ],
        ),
        Column(
            id="3",
            title="Done",
            cards=[
                Card(id="31", title="Basic project setup"),
            ],
        ),
    ],
)
