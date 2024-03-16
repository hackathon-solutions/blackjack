from PySide2 import QtWidgets, QtGui, QtCore

from config import config, APP_TITLE, ICON, PLACE_BACKGROUND
from widgets.helpers import CardImageLoader

std_font = QtGui.QFont('Arial', 16, QtGui.QFont.Bold)


class MainTextLabel(QtWidgets.QLabel):
    def __init__(self, text: str, group: QtWidgets.QLayout | None = None):
        super().__init__(text)
        if group is not None:
            group.addWidget(self)
        self.setFont(std_font)
        self.setStyleSheet('color: white;')
        self.setContentsMargins(10, 10, 10, 10)


class GameInfo(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self._layout = QtWidgets.QHBoxLayout(self)
        self._layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)

        self._count_rounds = MainTextLabel('', self._layout)
        self._player_balance = MainTextLabel('', self._layout)
        self._count_card_deck = MainTextLabel('', self._layout)
        self._player_bet = MainTextLabel('', self._layout)

    def set_count_rounds(self, value: int):
        self._count_rounds.setText(f'Раунд: {value}')

    def set_player_balance(self, value: int):
        self._player_balance.setText(f'Баланс: {value}')

    def set_count_card_deck(self, value: int):
        self._count_card_deck.setText(f'Кард в колоде: {value}')

    def set_player_bet(self, value: int):
        self._player_bet.setText(f'Ставка: {value}')


class PokerTable(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(170, 15, 170, 70)
        self._main_layout = QtWidgets.QVBoxLayout(self)
        self._layout1 = QtWidgets.QHBoxLayout()
        self._layout1.setAlignment(QtCore.Qt.AlignCenter)
        self._layout2 = QtWidgets.QHBoxLayout()
        self._layout2.setAlignment(QtCore.Qt.AlignCenter)
        self._main_layout.addLayout(self._layout1, 1)
        self._main_layout.addLayout(self._layout2, 1)

    def add_dealer_card(self, card_id: str):
        self._layout1.addWidget(CardFrame(card_id))

    def clear_dealer_cards(self):
        PokerTable._clear_layout(self._layout1)

    def add_player_card(self, card_id: str):
        self._layout2.addWidget(CardFrame(card_id))

    def clear_player_cards(self):
        PokerTable._clear_layout(self._layout2)

    @staticmethod
    def _clear_layout(layout: QtWidgets.QLayout):
        while layout.count():
            layout.takeAt(0).widget().deleteLater()


class ControlButton(QtWidgets.QPushButton):
    def __init__(self, text: str, group: QtWidgets.QLayout | None = None):
        super().__init__(text)
        group.addWidget(self)

        self.setFont(std_font)
        self.setStyleSheet('background-color: darkgreen; color: white;')
        self.setCursor(QtCore.Qt.PointingHandCursor)


class ControlBar(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self._layout = QtWidgets.QHBoxLayout(self)
        self._layout.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)

        self._onclick_hit = self._onclick_stub
        self._onclick_bet = self._onclick_stub
        self._onclick_double = self._onclick_stub
        self._onclick_stand = self._onclick_stub
        self._onclick_surrender = self._onclick_stub
        self._onclick_start = self._onclick_stub

        self._hit_btn = ControlButton('Hit', self._layout)
        self._hit_btn.clicked.connect(self._onclick_hit)
        self._bet_btn = ControlButton('Bet', self._layout)
        self._bet_btn.clicked.connect(self._onclick_bet)
        self._double_btn = ControlButton('Double', self._layout)
        self._double_btn.clicked.connect(self._onclick_double)
        self._stand_btn = ControlButton('Stand', self._layout)
        self._stand_btn.clicked.connect(self._onclick_stand)
        self._surrender_btn = ControlButton('Surrender', self._layout)
        self._surrender_btn.clicked.connect(self._onclick_surrender)
        self._start_btn = ControlButton('Start', self._layout)
        self._start_btn.clicked.connect(self._onclick_start)

    def set_onclick_hit(self, onclick):
        self._onclick_hit = onclick

    def set_onclick_bet(self, onclick):
        self._onclick_bet = onclick

    def set_onclick_double(self, onclick):
        self._onclick_double = onclick

    def set_onclick_stand(self, onclick):
        self._onclick_stand = onclick

    def set_onclick_surrender(self, onclick):
        self._onclick_surrender = onclick

    def set_onclick_start(self, onclick):
        self._onclick_start = onclick

    def _onclick_stub(self, event):
        pass


class PlaySpace(QtWidgets.QWidget):
    def __init__(self, w: int = 900, h: int = 600):
        super().__init__()
        self._w = w
        self._h = h
        self.setWindowTitle(config(APP_TITLE))
        self.setWindowIcon(QtGui.QIcon(config(ICON)))
        self.setMinimumSize(self._w, self._h)
        self.setMaximumSize(self._w, self._h)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignTop)

        self._game_info = GameInfo()
        self._poker_table = PokerTable()
        self._control_bar = ControlBar()

        self.layout.addWidget(self._game_info, 5)
        self.layout.addWidget(self._poker_table, 9)
        self.layout.addWidget(self._control_bar, 3)

    def paintEvent(self, arg__1):
        pixmap = QtGui.QPixmap(config(PLACE_BACKGROUND)).scaled(self._w, self._h, QtCore.Qt.KeepAspectRatio)
        QtGui.QPainter(self).drawPixmap(0, 0, pixmap)


class CardFrame(QtWidgets.QFrame):
    def __init__(self, card_id: str, w: int = 64, h: int = 86):
        super().__init__()
        self._cover = CardImageLoader(card_id).get_image()
        self.setMinimumWidth(w)
        self._w = w
        self.setMinimumHeight(h)
        self._h = h

    def paintEvent(self, arg__1):
        painter = QtGui.QPainter(self)
        pixmap = QtGui.QPixmap.fromImage(self._cover).scaled(self._w, self._h, QtCore.Qt.KeepAspectRatio)
        painter.drawPixmap(0, 0, pixmap)
