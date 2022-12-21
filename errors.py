class Wiped(Exception):
    """Personal exception to end the game if a team sank all th enemy boats."""
    pass


class IncorrectShot(Exception):
    """Personal exception to manage the user shot"""
    pass


class IncorrectCoordinates(Exception):
    """Personal exception to retry if the user enter bad boat coordinates."""
    pass


class IncorrectSize(Exception):
    """Personal exception to retry if the user enter a wrong ship size."""
    pass


class SaveError(Exception):
    """Personal exception to retry if the user doesn't enter YES/NO to save."""
    pass
