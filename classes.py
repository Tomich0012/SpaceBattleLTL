import functions
import time
import main
import cmd
import sys


class Team:
    def __init__(self, name):
        self.__name = name
        self.__coord_occupied = []
        self.board = Board(self.__name, self.__coord_occupied)
        self.__fired_shot = []

    @property
    def get_name(self):
        return self.__name

    @property
    def get_coord_occupied(self):
        return self.__coord_occupied

    @property
    def get_fired_shot(self):
        return self.__fired_shot

    def shoot(self, case_shot):
        """This Method validates the shot on the opponent's board
        PRE : The case_shot need to be a coordinate.
        POST :  If the case was occupied by a boat, is touched, and the case is remove from 'coord'
                If the case is touched and this is the last case of boat, the boat is sunk.
                If the case was empty, then the shoot is failed.
        """

        for j in main.team:
            if j.__name != self.__name:
                for a in j.board.ships:
                    if case_shot in a.coord:
                        print(f"\nLa case {case_shot} du {a.__ship_name} à été touchée ! Feu à bord\n")
                        a.coord.remove(case_shot)
                        time.sleep(2)
                        if len(a.coord) == 0:
                            j.board.ships.remove(a)
                            functions.cls()
                            print(f"Vous avez coulé le {a.__ship_name}\n")
                            if len(j.board.ships) == 0:
                                return "stop"
                        break
                    else:
                        print("Dommage, vous avez raté")
                        time.sleep(2)
                        break


class Board:
    def __init__(self, name, coord_occupied):
        self.__name = name
        self.ships = self.initialize_ships(coord_occupied)
        self.__coord_occupied = coord_occupied
        
    def initialize_ships(self, coord_occupied):
        """This method initializes all boats without their positions for each team
        PRE : /
        POST : All boats are in 'self.ships'
        """
        ships = []
        for i in main.ships_available:
            ships.append(Ship(i, main.ships_available[i], self.__name, coord_occupied))
        return ships


class Ship:
    def __init__(self, name, size, team_name, coord_occupied):
        self.__team = team_name
        self.__ship_name = name
        self.__size = size
        self.__coord = []
        functions.ask_boat_position(self, coord_occupied)

    @property
    def coord(self):
        return self.__coord

    @coord.setter
    def coord(self, coord_list):
        self.__coord = coord_list

    def all_checking(self, start_coord, end_coord, coord_occupied):
        """This method verifies the placement coordinates of the boat.
        PRE : /
        POST : Send the coordinates to 'boat_orientation'.
        RAISES : ValueError not a coordinates.
        """
        try:
            if start_coord not in main.all_coord or end_coord not in main.all_coord:
                raise ValueError
            self.boat_orientation(start_coord, end_coord, self.__ship_name, coord_occupied)
        except ValueError:
            print("Mauvaise coordonnée, recommencez")
            functions.ask_boat_position(self, coord_occupied)

    def boat_orientation(self, start_coord, end_coord, ship_name, coord_occupied):
        """This method checks if the boat has been placed horizontally or vertically, and calls create_boat().
        PRE : /
        POST :  Create all the position to a list if the boat is in the great position.
        """

        if start_coord[0] == end_coord[0]:
            if (int(end_coord[1:]) - int(start_coord[1:])) + 1 == main.ships_available[ship_name]:
                self.create_boat(start_coord, end_coord, coord_occupied, "x")
            else:
                print("Erreur, le bateau n'a pas la taille demandée, Recommencez")
                functions.ask_boat_position(self, coord_occupied)
        else:
            if (main.alpha_columns.index(end_coord[0]) - main.alpha_columns.index(start_coord[0])) + 1 == main.ships_available[
                ship_name]:
                self.create_boat(start_coord, end_coord, coord_occupied, "y")
            else:
                print("Erreur, le bateau n'a pas la taille demandée, Recommencez")
                functions.ask_boat_position(self, coord_occupied)

    def create_boat(self, start_coord, end_coord, coord_occupied, x_or_y):
        """This method creates the boat horizontally or vertically.
        PRE : /
        POST :  Create the boat and change the availability of the boxes it occupies.
        """

        if x_or_y == "x":
            coord_boat_x = []
            for i in range(int(start_coord[1:]), int(end_coord[1:]) + 1):
                coord_boat_x.append(start_coord[0] + str(i))
            if len(set(coord_boat_x) & set(coord_occupied)) == 0:
                self.coord = coord_boat_x
                for i in coord_boat_x:
                    coord_occupied.append(i)
            else:
                print("Un bateau occupe déjà une ou plusieurs de ces positions, recommencez")
                functions.ask_boat_position(self, coord_occupied)
        else:
            coord_boat_y = []
            for i in range(main.alpha_columns.index(start_coord[0]), main.alpha_columns.index(end_coord[0]) + 1):
                coord_boat_y.append(main.alpha_columns[i] + start_coord[1])
            if len(set(coord_boat_y) & set(coord_occupied)) == 0:
                self.coord = coord_boat_y
                for i in coord_boat_y:
                    coord_occupied.append(i)
            else:
                print("Un bateau occupe déjà une ou plusieurs de ces positions, recommencez")
                functions.ask_boat_position(self, coord_occupied)


class Start(cmd.Cmd):
    """
    PRE : The command must be known to be executed.
    POST : Start the requested method.
    """
    intro = "\nBienvenue dans le jeu Space Battle.\n[help] or [?] : pour la liste des commandes possibles." \
            "\n[start] pour lancer une nouvelle partie.\n[quit] pour quitter le programme."
    prompt = 'Space Battle : '
    file = None

    def do_start(self, arg=0):
        """Start the game.
        PRE : /
        POST : The game is started.
        """

        functions.cls()
        functions.board()
        functions.initialize_teams()
        functions.start_battle()

    def do_quit(self, arg=0):
        """Quit the game.
        PRE : /
        POST : The game is closed.
        """
        sys.exit()
        