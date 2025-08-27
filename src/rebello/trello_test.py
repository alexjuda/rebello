import json
from pathlib import Path
import re
import pytest
import responses
from .trello import TrelloClient


class TestTrelloClient:
    @staticmethod
    @pytest.fixture
    def client(monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("TRELLO_API_KEY", "api-key")
        monkeypatch.setenv("TRELLO_API_SECRET", "api-secret")
        monkeypatch.setenv("TRELLO_BOARD_ID", "board-id")
        return TrelloClient.from_env()

    @staticmethod
    def test_init_from_env_vars(client: TrelloClient, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv("TRELLO_API_KEY", "api-key2")
        monkeypatch.setenv("TRELLO_API_SECRET", "api-secret2")
        client2 = TrelloClient.from_env()

        assert client is not None
        assert client2 is not None

        assert client._client.api_key != client2._client.api_key
        assert client._client.api_secret != client2._client.api_secret

    @staticmethod
    def test_list_boards(client: TrelloClient):
        with (Path(__file__).parent / "trello_responses" / "boards.json").open() as f:
            boards_json = json.load(f)

        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET, re.compile(r"https://api.trello.com/"), json=boards_json
            )
            boards = client.list_boards()

        assert len(boards) == 1
        assert boards[0].id == "5abbe4b7ddc1b351ef961414"
        assert boards[0].name == "Trello Platform Changes"

    @staticmethod
    def test_get_board(client: TrelloClient):
        with (Path(__file__).parent / "trello_responses" / "board.json").open() as f:
            board_json = json.load(f)

        with (Path(__file__).parent / "trello_responses" / "lists.json").open() as f:
            lists_json = json.load(f)

        with (Path(__file__).parent / "trello_responses" / "cards.json").open() as f:
            cards_json = json.load(f)

        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                re.compile(r"https://api.trello.com/1/boards/\w+[^/]+$"),
                json=board_json,
            )
            rsps.add(
                responses.GET,
                re.compile(r"https://api.trello.com/1/boards/\w*/lists"),
                json=lists_json,
            )
            rsps.add(
                responses.GET,
                re.compile(r"https://api.trello.com/1/boards/\w*/cards"),
                json=cards_json,
            )

            board = client.get_board()

        assert board.id == "boardid1"
        assert board.name == "Trello Platform Changes"

        assert len(board.lists) > 0
        a_list = board.lists[0]
        assert a_list.id == "list-id"
        assert a_list.name == "Things to buy today"

        assert len(a_list.cards) > 0
        assert a_list.cards[0].id == "cardid1"
        assert a_list.cards[0].name == "trello CLI with editor interface"

    @staticmethod
    def test_create_card(client: TrelloClient):
        name = "foo bar"
        list_id = "abc123"

        with (Path(__file__).parent / "trello_responses" / "lists.json").open() as f:
            list_json = json.load(f)[0]

        with (Path(__file__).parent / "trello_responses" / "board.json").open() as f:
            board_json = json.load(f)

        with (Path(__file__).parent / "trello_responses" / "cards.json").open() as f:
            card_json = json.load(f)[0]

        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                re.compile(r"https://api.trello.com/1/lists/abc123[^/]+$"),
                json=list_json,
            )
            rsps.add(
                responses.GET,
                re.compile(r"https://api.trello.com/1/boards/\w+[^/]+$"),
                json=board_json,
            )
            rsps.add(
                responses.POST,
                re.compile(r"https://api.trello.com/1/cards[^/]+$"),
                json=card_json,
            )
            client.create_card(name=name, list_id=list_id)
