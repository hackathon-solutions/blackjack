from json import loads

APP_TITLE = 'app.title'
ICON = 'app.icon'
MIN_BET = 'game.bet.min'
MAX_BET = 'game.bet.max'
INCREASE_ALLOW = 'game.bet.increase.allow'
INCREASE_COUNT = 'game.bet.increase.count'
PLACE_BACKGROUND = 'game.place.background'
CARDS_BACKGROUND = 'game.place.cards_style.background'
CARDS_FOREGROUND = 'game.place.cards_style.foreground'
HIDE_DEALER_CARDS = 'game.place.hide_dealer_cards'
HIDE_FIRST_DEALER_CARD = 'game.place.hide_first_dealer_card'
PLAYER_INIT_BALANCE = 'player.init.balance'
DEALER_NAME = 'dealer.name'
DEALER_DROP_FROM = 'dealer.behaviour.drop_from'


with open('./conf.json', 'r', encoding='utf-8') as f:
    _DATA = loads(f.read())


def config(key: str):
    """Allows you to get a value from the configuration by its key."""
    global _DATA
    keys = key.split('.')
    data = _DATA[keys[0]]
    for i in range(1, len(keys)):
        data = data[keys[i]]
    return data
