import sys

from PySide2 import QtWidgets

from entities import Card, Game
from widgets.game import PlaySpace, CardFrame
from widgets.helpers import CardIdBuilder

game = Game()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = PlaySpace()
    layout = QtWidgets.QGridLayout(main)
    card1 = CardFrame(CardIdBuilder(Card.SUIT_HEART, Card.RANK_10).get(), 100, 144)
    card2 = CardFrame(CardIdBuilder(Card.SUIT_CLUB, Card.RANK_2).get(), 100, 144)
    card3 = CardFrame(CardIdBuilder.cover().get(), 100, 144)
    layout.addWidget(card1, 0, 0)
    layout.addWidget(card2, 0, 1)
    layout.addWidget(card3, 0, 2)
    main.show()

    sys.exit(app.exec_())
