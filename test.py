import unittest
import classes
import main
import functions


class TestImportClasses(unittest.TestCase):
    def test_Team_init(self):
        # Vérifie que l'initialisation de la classe Team crée une instance de Board
        team = classes.Team("Tom")
        self.assertIsInstance(team.board, classes.Board)

    def test_Board_init(self):
        # Vérifie que l'initialisation de la classe Board crée une liste de bateaux avec la bonne longueur
        coord_occupied = []
        board = classes.Board("player1", coord_occupied)
        self.assertEqual(len(board.ships), len(classes.ships_available))
        self.assertIsInstance(board.ships[0], classes.Ship)

    def test_Ship_init(self):
        # Vérifie que l'initialisation de la classe Ship crée une liste de coordonnées de la bonne longueur
        coord_occupied = []
        ship = classes.Ship("SpaceCruiser", 2, "player1", coord_occupied)
        self.assertEqual(len(ship.coord), 2)

    def test_board(self):
        # Vérifie que la fonction board() crée une liste de coordonnées de la bonne longueur
        main.all_coord = []
        functions.board()
        self.assertEqual(len(main.all_coord), 100)

    # --------------------------------------------
    # classe Board

    def test_initialize_ships(self):
        # Test que la méthode initialise bien tous les bateaux sans position
        board = classes.Board('team1', [])
        self.assertEqual(len(board.ships), len(main.ships_available))
        for ship in board.ships:
            self.assertEqual(ship.team, 'team1')
            self.assertEqual(ship.coordinates, [])

    def test_init(self):
        # Test que la méthode __init__ initialise correctement tous les attributs de l'objet
        board = classes.Board('team1', [[1, 2], [3, 4]])
        self.assertEqual(board.team, 'team1')
        self.assertEqual(len(board.ships), len(main.ships_available))
        for ship in board.ships:
            self.assertEqual(ship.team, 'team1')
            self.assertEqual(ship.coordinates, [[1, 2], [3, 4]])
