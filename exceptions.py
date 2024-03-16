class CardDeckGenerationException(Exception):
    pass


class IncorrectBetException(Exception):
    pass


class GameOperationException(Exception):
    pass


class CannotCardTakenException(GameOperationException):
    pass


class CannotPlaceBetException(GameOperationException):
    pass


class CannotDoubleBetException(GameOperationException):
    pass


class CannotFoldException(GameOperationException):
    pass


class RoundStartException(Exception):
    pass
