from PySide2 import QtWidgets, QtGui, QtCore

from config import config, APP_TITLE, ICON, PLACE_BACKGROUND
from entities import Game, Player, Dealer, Card, CardCounting
from exceptions import RoundStartException, GameOperationException
from widgets.helpers import CardImageLoader, CardIdBuilder

std_font = QtGui.QFont('Arial', 16, QtGui.QFont.Bold)

m_dealer = Dealer(1_000_000_000)
m_player = Player('Name').me()
game = Game(m_dealer)
game.add_player(m_dealer)
game.add_player(m_player)


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

    def clear(self):
        self.clear_player_cards()
        self.clear_dealer_cards()

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

        self._hit_btn = ControlButton('Hit', self._layout)
        self._bet_btn = ControlButton('Bet', self._layout)
        self._double_btn = ControlButton('Double', self._layout)
        self._stand_btn = ControlButton('Stand', self._layout)
        self._surrender_btn = ControlButton('Surrender', self._layout)
        self._start_btn = ControlButton('Start', self._layout)

    def set_onclick_hit(self, onclick):
        self._hit_btn.clicked.connect(onclick)

    def set_onclick_bet(self, onclick):
        self._bet_btn.clicked.connect(onclick)

    def set_onclick_double(self, onclick):
        self._double_btn.clicked.connect(onclick)

    def set_onclick_stand(self, onclick):
        self._stand_btn.clicked.connect(onclick)

    def set_onclick_surrender(self, onclick):
        self._surrender_btn.clicked.connect(onclick)

    def set_onclick_start(self, onclick):
        self._start_btn.clicked.connect(onclick)

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
        self._control_bar.set_onclick_start(self.start)
        self._control_bar.set_onclick_hit(self.hit)
        self._control_bar.set_onclick_bet(self.bet)
        self._control_bar.set_onclick_double(self.double)
        self._control_bar.set_onclick_stand(self.stand)
        self._control_bar.set_onclick_surrender(self.surrender)

        self.layout.addWidget(self._game_info, 5)
        self.layout.addWidget(self._poker_table, 9)
        self.layout.addWidget(self._control_bar, 3)

    def start(self):
        try:
            game.new_round()
            game.cur_round.take_card(game.cur_round.as_player_round(m_dealer))
            card_dealer1 = game.cur_round.take_card(game.cur_round.as_player_round(m_dealer))
            card_player1 = game.cur_round.take_card(game.cur_round.as_player_round(m_player))
            card_player2 = game.cur_round.take_card(game.cur_round.as_player_round(m_player))

            self._poker_table.add_dealer_card(CardIdBuilder(Card.COVER, Card.COVER).get())
            self._poker_table.add_dealer_card(CardIdBuilder(card_dealer1.suit, card_dealer1.rank).get())
            self._poker_table.add_player_card(CardIdBuilder(card_player1.suit, card_player1.rank).get())
            self._poker_table.add_player_card(CardIdBuilder(card_player2.suit, card_player2.rank).get())

            self.update_game_info()

            self.place_bet()
        except RoundStartException:
            QtWidgets.QMessageBox(text='Невозможно начать новый раунд, пока не закончен текущий!').exec_()

    def place_bet(self):
        bet = PlaySpace.try_input_bet()
        while m_player.balance < bet:
            QtWidgets.QMessageBox(text='Недостаточный баланс.').exec_()
            bet = PlaySpace.try_input_bet()

        game.cur_round.place_bet(game.cur_round.as_player_round(m_dealer), bet)
        game.cur_round.place_bet(game.cur_round.as_player_round(m_player), bet)

        self._game_info.set_player_bet(game.cur_round.as_player_round(m_player).bet)
        self._game_info.set_player_balance(m_player.balance)

    @staticmethod
    def try_input_bet() -> int:
        inp = ''
        while not inp.isdigit():
            prompt = PromptDialog('Ставка', 'Введите ставку (число)')
            prompt.exec_()
            inp = '' if prompt.result is None else prompt.result
        return int(inp)

    def update_game_info(self):
        self._game_info.set_count_card_deck(game.cur_round.card_deck.count)
        self._game_info.set_player_bet(game.cur_round.as_player_round(m_player).bet)
        self._game_info.set_player_balance(m_player.balance)
        self._game_info.set_count_rounds(game.quantity_rounds)

    def hit(self):
        try:
            card_player = game.cur_round.take_card(game.cur_round.as_player_round(m_player))
            self._poker_table.add_player_card(CardIdBuilder(card_player.suit, card_player.rank).get())

            if CardCounting(game.cur_round.as_player_round(m_dealer).cards).blackjack_count < m_dealer.drop_from:
                card_dealer = game.cur_round.take_card(game.cur_round.as_player_round(m_dealer))
                self._poker_table.add_dealer_card(CardIdBuilder(card_dealer.suit, card_dealer.rank).get())
        except GameOperationException:
            QtWidgets.QMessageBox(text='Вы не можете взять карту.').exec_()

        self._game_info.set_count_card_deck(game.cur_round.card_deck.count)

    def bet(self):
        try:
            self.place_bet()
        except GameOperationException:
            QtWidgets.QMessageBox(text='Превышено количество ставок.').exec_()

    def double(self):
        try:
            game.cur_round.double_bet(game.cur_round.as_player_round(m_player))
            game.cur_round.place_bet(game.cur_round.as_player_round(m_dealer), game.cur_round.as_player_round(m_dealer).bet)
        except GameOperationException:
            QtWidgets.QMessageBox(text='Удвоение ставки невозможно.').exec_()
        self._game_info.set_player_bet(game.cur_round.as_player_round(m_player).bet)
        self._game_info.set_player_balance(m_player.balance)

    def stand(self):
        dealer_score = CardCounting(game.cur_round.as_player_round(m_dealer).cards).blackjack_count
        while dealer_score < m_dealer.drop_from:
            card = game.cur_round.take_card(game.cur_round.as_player_round(m_dealer))
            self._poker_table.add_dealer_card(CardIdBuilder(card.suit, card.rank).get())
            dealer_score = CardCounting(game.cur_round.as_player_round(m_dealer).cards).blackjack_count
        winners = game.cur_round.finish()
        if m_player in winners:
            QtWidgets.QMessageBox(text='Раунд окончен. Вы выиграли!').exec_()
        elif len(winners) > 0:
            QtWidgets.QMessageBox(text='Раунд окончен. Вы проиграли!').exec_()
        else:
            QtWidgets.QMessageBox(text='Раунд окончен. Ничья!').exec_()
        self.update_game_info()
        self._poker_table.clear()

    @staticmethod
    def surrender():
        QtWidgets.QMessageBox(text='Не реализовано :(').exec_()

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


class PromptDialog(QtWidgets.QDialog):
    def __init__(self, title: str | None = None, hint: str = ''):
        super().__init__()
        self.setWindowTitle(title)
        self._layout = QtWidgets.QVBoxLayout(self)
        self._result = None

        self._input_box = QtWidgets.QLineEdit()
        self._input_box.setPlaceholderText(hint)
        self._layout.addWidget(self._input_box)

        self._ok_btn = QtWidgets.QPushButton('OK')
        self._layout.addWidget(self._ok_btn)

        self._ok_btn.clicked.connect(self.onclick_ok)

    def onclick_ok(self):
        self._result = self._input_box.text()
        self.close()

    @property
    def result(self):
        return self._result
