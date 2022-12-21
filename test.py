import unittest
from classes import *

main.testunit = True


class TestImportClasses(unittest.TestCase):

    def test_Ship_init(self):
        ship = Ship("SpaceCruiser", 2, "La team", [], "A1", "A2")

        self.assertIsNotNone(ship)
        self.assertEqual(ship.get_ship_name, "SpaceCruiser")
        self.assertEqual(ship.coord, ["A1", "A2"])
        self.assertIsInstance(ship, Ship)

        with self.assertRaises(errors.IncorrectCoordinates):
            Ship("SpaceCruiser", 2, "La team", [], "A1", "A12")

    # test error

    def test_Board_init(self):
        ship1 = Ship("SpaceCruiser", 2, "La team", [], "A1", "A2")
        ship2 = Ship("SpaceCruiser", 2, "La team", [], "B4", "B5")

        b = Board("Board", [], [ship1, ship2])
        self.assertIsNotNone(b)
        # Ici mettre les assert pour board

        # test error

    def test_initialize_ships(self):
        ship1 = Ship("SpaceCruiser", 2, "La team", [], "A1", "A2")
        ship2 = Ship("SpaceCruiser", 2, "La team", [], "B4", "B5")

        b = Board("Board", [], [ship1, ship2])
        self.assertIsInstance(b.initialize_ships([], "A1", "A2")[0], Ship)

    # test error

    def test_Team_init(self):
        ship1 = Ship("SpaceCruiser", 2, "La team", [], "A1", "A2")
        ship2 = Ship("SpaceCruiser", 2, "La team", [], "B4", "B5")
        b = Board("Board", [], [ship1, ship2])

        t = Team("Loic", b)

        self.assertIsNotNone(t)
        self.assertEqual(t.get_name, "Loic")
        self.assertIsInstance(t.board, Board)
        self.assertIsInstance(t, Team)

    # test error
