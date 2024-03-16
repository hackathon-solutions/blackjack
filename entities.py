from random import shuffle
from config import config, PLAYER_INIT_BALANCE, DEALER_DROP_FROM, MIN_BET, MAX_BET, INCREASE_ALLOW, INCREASE_COUNT, \
    DEALER_NAME
from exceptions import *


class Player:
    def __init__(self, name: str, balance: int = config(PLAYER_INIT_BALANCE)):
        self._name = name
        self._balance = balance
        self._is_me = False

    def update_balance(self, more: int):
        self._balance += more

    def me(self):
        self._is_me = True
        return self

    @property
    def name(self):
        return self._name

    @property
    def balance(self):
        return self._balance

    @property
    def is_me(self):
        return self._is_me


class Dealer(Player):
    def __init__(self, balance: int, name: str = config(DEALER_NAME), drop_from: int = config(DEALER_DROP_FROM)):
        super().__init__(name, balance)
        self._drop_from = drop_from

    @property
    def drop_from(self):
        return self._drop_from


class Card:
    def __init__(self, suit: str, rank: str):
        self._suit = suit
        self._rank = rank

    @property
    def suit(self):
        return self._suit

    @property
    def rank(self):
        return self._rank

    def __str__(self):
        return f'{self.rank} of {self.suit}'

    COVER = 'card_cover'
    SUIT_CLUB = 'club'
    SUIT_DIAMOND = 'diamond'
    SUIT_HEART = 'heart'
    SUIT_SPADE = 'spade'
    RANK_2 = '2'
    RANK_3 = '3'
    RANK_4 = '4'
    RANK_5 = '5'
    RANK_6 = '6'
    RANK_7 = '7'
    RANK_8 = '8'
    RANK_9 = '9'
    RANK_10 = '10'
    RANK_JACK = 'J'
    RANK_QUEEN = 'Q'
    RANK_KING = 'K'
    RANK_ACE = 'A'


class CardSequenceGenerator:
    def __init__(self):
        self._ranks = [Card.RANK_2, Card.RANK_3, Card.RANK_4, Card.RANK_5, Card.RANK_6, Card.RANK_7, Card.RANK_8,
                       Card.RANK_9, Card.RANK_10, Card.RANK_JACK, Card.RANK_QUEEN, Card.RANK_KING, Card.RANK_ACE]
        self._suits = [Card.SUIT_CLUB, Card.SUIT_SPADE, Card.SUIT_HEART, Card.SUIT_DIAMOND]

    @staticmethod
    def wrap_shuffle(seq: list) -> list:
        cp = [*seq]
        shuffle(cp)
        return cp

    @property
    def sequence(self) -> list[Card]:
        seq = []
        for suit in self.wrap_shuffle(self._suits):
            for rank in self.wrap_shuffle(self._ranks):
                seq.append(Card(suit, rank))
        return seq


class CardDeck:
    seq_gen = CardSequenceGenerator()

    def __init__(self):
        self._deck_size = 52
        self._count = 0
        self._cards = []

        for card in CardDeck.seq_gen.sequence:
            self._count += 1
            self._cards.append(card)

        if self._count != self._deck_size:
            raise CardDeckGenerationException()

    def take(self):
        self._count -= 1
        return self._cards.pop(0)

    @property
    def count(self):
        return self._count

    @property
    def size(self):
        return self._deck_size

    def __str__(self):
        return list(map(lambda card: card.__str__(), self._cards)).__str__()


class PlayerRound:
    def __init__(self, player: Player):
        self._player = player
        self._bet = 0
        self._count_increases = 0
        self._cards: list[Card] = []
        self._folded = False
        self._double = False
        self._quantity_takes_card = -1

    def place_bet(self, bet: int):
        if bet > self.player.balance:
            raise IncorrectBetException()
        self._player.update_balance(-bet)
        self._bet += bet
        self.increase()

    def increase(self):
        self._count_increases += 1

    def put_card(self, card: Card):
        if self._quantity_takes_card == 0:
            raise CannotCardTakenException()
        if self._quantity_takes_card > 0:
            self._quantity_takes_card -= 1
        self._cards.append(card)

    def double(self):
        self._double = True
        self._quantity_takes_card = 1

    def fold(self):
        part_of_bet = self._bet // 2
        self._bet -= part_of_bet
        self.player.update_balance(part_of_bet)
        self._folded = True

    @property
    def player(self):
        return self._player

    @property
    def bet(self):
        return self._bet

    @property
    def count_increases(self):
        return self._count_increases

    @property
    def cards(self):
        return [*self._cards]

    @property
    def folded(self):
        return self._folded

    @property
    def is_double(self):
        return self._double


class Round:
    def __init__(self):
        self._active_players: list[PlayerRound] = []
        self._card_deck = CardDeck()
        self._bank = 0
        self._min_bet = config(MIN_BET)
        self._max_bet = config(MAX_BET)
        self._increase_allow = config(INCREASE_ALLOW)
        self._max_increase_count = config(INCREASE_COUNT)

    def take_card(self, player: PlayerRound):
        player.put_card(self.card_deck.take())

    def place_bet(self, player: PlayerRound, bet: int):
        if player.count_increases > self._max_increase_count:
            raise CannotPlaceBetException()
        if self._min_bet < bet < self._max_bet:
            raise IncorrectBetException()
        player.place_bet(bet)
        self._bank += bet

    def double_bet(self, player: PlayerRound):
        if player.is_double:
            raise CannotDoubleBetException()
        self.place_bet(player, player.bet)
        player.double()

    def fold(self, player: PlayerRound):
        if player.folded:
            raise CannotFoldException()
        self._bank -= player.bet // 2
        player.fold()

    @property
    def active_players(self):
        return [*self._active_players]

    def add_player(self, player: Player):
        self._active_players.append(PlayerRound(player))

    def kick_player(self, player: PlayerRound):
        self._active_players.remove(player)

    @property
    def card_deck(self):
        return self._card_deck

    @property
    def min_bet(self):
        return self._min_bet


class Game:
    def __init__(self, dealer: Dealer):
        self._dealer = dealer
        self._players: list[Player] = []
        self._cur_round = None
        self._quantity_rounds = 0

    def add_player(self, player: Player):
        self._players.append(player)

    def remove_player(self, player: Player):
        self._players.remove(player)

    def new_round(self) -> Round:
        self._cur_round = Round()
        for player in self.players:
            if player.balance >= self._cur_round.min_bet:
                self._cur_round.add_player(player)
        if len(self._cur_round.active_players) < 2:
            self._cur_round = None
            raise RoundStartException('Amount players less than 2.')
        self._quantity_rounds += 1
        return self._cur_round

    @property
    def dealer(self):
        return self._dealer

    @property
    def players(self):
        return [*self._players]

    @property
    def cur_round(self):
        return self._cur_round

    @property
    def quantity_rounds(self):
        return self._quantity_rounds
