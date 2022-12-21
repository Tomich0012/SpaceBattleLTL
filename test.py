import unittest
from classes import *
from functions import *


team_one_name = "Loic"
team_two_name = "Louis"

start = 'A1'
end = 'A2'

columns = ["A", "B", "C"]
lines = [1, 2, 3, 4]

ships_available = {"SpaceCruiser": 2}

liste = board(lines, columns)


class TestImportClasses(unittest.TestCase):

    def test_Ship_init(self):
        ship = Ship("SpaceCruiser", 2, "La team", [], "A1", "A2")

        self.assertIsNotNone(ship)
        self.assertEqual(ship.get_ship_name, "SpaceCruiser")
        self.assertEqual(ship.coord, ["A1", "A2"])

    def test_Board_init(self):
        ship1 = Ship("SpaceCruiser", 2, "La team", [], "A1", "A2")
        ship2 = Ship("SpaceCruiser", 2, "La team", [], "B4", "B5")

        b = Board("Board", [], [ship1, ship2])
        self.assertIsNotNone(b)
        # Ici mettre les assert pour board

    def test_Team_init(self):
        ship1 = Ship("SpaceCruiser", 2, "La team", [], "A1", "A2")
        ship2 = Ship("SpaceCruiser", 2, "La team", [], "B4", "B5")
        b = Board("Board", [], [ship1, ship2])

        t = Team("Loic", b)

        self.assertIsNotNone(t)
        self.assertEqual(t.get_name, "Loic")

