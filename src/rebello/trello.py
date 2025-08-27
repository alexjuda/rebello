from dataclasses import dataclass
from typing import cast
from trello import TrelloClient as GenericClient, Card as APICard
from .settings import TrelloSettings
from .models import Board, CardWithID, List


@dataclass
class BoardShallow:
    id: str
    name: str


type ListID = str


class TrelloClient:
    def __init__(self, generic_client: GenericClient, board_id: str):
        self._client = generic_client
        self._board_id = board_id

    @classmethod
    def from_env(cls) -> "TrelloClient":
        settings = TrelloSettings()  # type: ignore
        client = GenericClient(
            api_key=settings.trello_api_key,
            api_secret=settings.trello_api_secret,
        )
        return cls(client, settings.trello_board_id)

    def list_boards(self) -> list[BoardShallow]:
        boards = self._client.list_boards()
        return [BoardShallow(id=cast(str, b.id), name=b.name) for b in boards]

    def get_board(self) -> Board:
        api_board = self._client.get_board(board_id=self._board_id)

        api_lists = api_board.open_lists()
        api_cards = api_board.open_cards()

        # We need to match cards with lists. It's a many-to-one relationship.
        grouped_cards: dict[ListID, list[APICard]] = {}
        for api_card in api_cards:
            grouped_cards.setdefault(api_card.list_id, []).append(api_card)

        # We wanna retain the order the we received the lists in.
        lists: list[List] = []
        for api_list in api_lists:
            cards_for_this_list = grouped_cards.get(api_list.id, [])
            cards = [
                CardWithID(id=api_card.id, name=api_card.name)
                for api_card in cards_for_this_list
            ]
            lists.append(List(id=api_list.id, name=api_list.name, cards=cards))

        return Board(id=cast(str, api_board.id), name=api_board.name, lists=lists)

    def create_card(self, name: str, list_id: str):
        a_list = self._client.get_list(list_id)
        a_list.add_card(name=name)

    def change_parent(self, card_id: str, new_list_id: str):
        card = self._client.get_card(card_id)
        card.change_list(new_list_id)

    def rename_card(self, card_id: str, new_name: str):
        card = self._client.get_card(card_id)
        card.set_name(new_name)

    def archive_card(self, card_id: str):
        card = self._client.get_card(card_id)
        card.set_closed(True)


__all__ = ["TrelloClient"]
