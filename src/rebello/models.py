"""
The main models used across the app.

In bigger projects each "module" should depend on its own set of models for modularity, but it's a small project so
a single coupling point is fine.
"""
from dataclasses import dataclass


@dataclass
class Card:
    id: str
    title: str


@dataclass
class Column:
    id: str
    title: str
    cards: list[Card]


@dataclass
class Board:
    id: str
    title: str
    columns: list[Column]
