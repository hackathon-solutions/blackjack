import os
import pathlib

from PySide2.QtGui import QImage

import config
from entities import Card


class CardIdBuilder:
    def __init__(self, suit: str, rank: str, mime: str | None = None):
        self._suit = suit
        self._rank = rank
        self._mime = mime

    @staticmethod
    def cover():
        return CardIdBuilder(Card.COVER, Card.COVER)

    def get(self):
        return f'{self._rank}_{self._suit}{("." + self._mime) if self._mime else ""}'


class CardImageLoader:
    def __init__(self, card_id: str):
        self._card_id = card_id

    def get_path(self) -> pathlib.Path:
        if self._card_id.count(Card.COVER) == 2:
            return config.config(config.CARDS_BACKGROUND)

        for file in os.listdir(config.config(config.CARDS_FOREGROUND)):
            if file.startswith(self._card_id):
                return pathlib.Path(f'{config.config(config.CARDS_FOREGROUND)}{file}').absolute()

        raise FileNotFoundError(f'card with id "{self._card_id}" not found.')

    def get_image(self) -> QImage:
        return QImage(self.get_path().__str__())

    @staticmethod
    def get_cover_path() -> pathlib.Path:
        return pathlib.Path(config.config(config.CARDS_BACKGROUND)).absolute()

    @staticmethod
    def get_cover_image() -> QImage:
        return QImage(CardImageLoader.get_cover_path().__str__())
