class Wiped(Exception):
    """Personal exception to end the game if a team sank all th enemy boats."""
    pass


class IncorrectShot(Exception):
    pass


class IncorrectCoordinates(Exception):
    pass


class IncorrectSize(Exception):
    pass


class SaveError(Exception):
    pass
