import errors
import functions
import time
import main
import cmd
import sys


class Team:
    def __init__(self, name, board=None):
        self.__team_name = name
        self.__coord_occupied = []
        self.__fired_shot = []

        if board:
            self.board = board
        else:
            self.board = Board(self.__team_name, self.__coord_occupied)

    @property
    def get_team_name(self):
        """Ce getter donne accès à l'attribut privé name
        PRE : /
        POST : retourne le nom de l'équipe
        """
        return self.__team_name

    @property
    def get_coord_occupied(self):
        """Ce getter donne accès à l'attribut privé coord_occupied
        PRE : /
        POST : retourne la liste des coordonnées occupées par l'équipe
        """
        return self.__coord_occupied

    @property
    def get_fired_shot(self):
        """Ce getter donne accès à l'attribut privé fired_shot
        PRE : /
        POST : retourne la liste des positions sur lesquelles l'équipe a déjà tiré
        """
        return self.__fired_shot

    def shoot(self, case_shot):
        """Cette methode vérifie si le tir touche un bateau ou est raté.

        PRE : case_shoot est une string correspondant à une coordonnée de tir
        POST : Si la case était occupée par un bateau, c'est touché et la case est retirée de la liste 'coord'
               Si la case est touchée et que c'est la dernière caisse de bateau, le bateau est coulé.
               Si la case était vide, le tir est raté.
        """
        is_touched = False
        for j in main.team:
            if j.__team_name != self.__team_name:
                for a in j.board.ships:
                    if case_shot in a.coord:
                        print(f"\nLa case {case_shot} du {a.get_ship_name} à été touchée ! Feu à bord\n")
                        is_touched = True
                        a.coord.remove(case_shot)
                        time.sleep(2)
                        if len(a.coord) == 0:
                            j.board.ships.remove(a)
                            functions.cls()
                            print(f"Vous avez coulé le {a.get_ship_name}\n")
                            if len(j.board.ships) == 0:
                                return "stop"
                    else:
                        continue
        if not is_touched:
            print("Dommage, vous avez raté")
            time.sleep(2)


class Board:
    def __init__(self, name, coord_occupied, ships=None):
        self.__team_name = name
        self.__coord_occupied = coord_occupied

        if ships:
            self.ships = ships
        else:
            self.ships = self.initialize_ships(coord_occupied)

    def initialize_ships(self, coord_occupied, start_coord=None, end_coord=None, nom=None, taille=None):
        """Cette methode lance l'initialisation des bateaux.

            PRE : coord_occupied est liste de string correspondant des coordonées utilisées par les autres bateaux
            POST : La fonction retourne une liste d'objets de la classe Ship, initialisés avec les informations
            contenues
                    dans le dictionnaire main.ships_available, le nom de l'équipe (self.__team_name)
                        et la liste de coordonnées occupées (coord_occupied)
            """
        if start_coord and end_coord:
            ships = []
            ships.append(Ship(nom, taille, self.__team_name, coord_occupied, start_coord, end_coord))
            return ships
        else:
            ships = []
            for i in main.ships_available:
                ships.append(
                    Ship(i, main.ships_available[i], self.__team_name, coord_occupied))
            return ships


class Ship:
    def __init__(self, name, size, team_name, coord_occupied, start_coord=None, end_coord=None):
        self.__team = team_name
        self.__ship_name = name
        self.__size = size
        self.__coord = []

        if start_coord and end_coord:
            functions.board()
            functions.test_all_checking(self, start_coord, end_coord, coord_occupied)
        else:
            functions.ask_boat_position(self, coord_occupied)

    @property
    def get_ship_name(self):
        """Ce getter donne accès à l'attribut privé ship_name
        PRE : /
        POST : retourne le nom du bateau
        """
        return self.__ship_name

    @property
    def coord(self):
        """Ce getter donne accès à l'attribut privé coord
        PRE : /
        POST : retourne la liste des coordonnées occupées par le bateau
        """
        return self.__coord

    @coord.setter
    def coord(self, coord_list):
        """Ce setter permet de modifier l'attribut privé coord
        PRE : /
        POST : attribue comme valeur coord_list à l'attribut coord
        """
        self.__coord = coord_list

    def all_checking(self, start_coord, end_coord, coord_occupied):
        """Cette methode vérifie que les coordonnées données par l'utilisateur soient sur le plateau.
        PRE : start_coord et end_coord sont des coordonnées (string) et coord_occupied est une liste de coordonnées (
        string).

        POST : la fonction boat_orientation est appelée avec les arguments start_coord, end_coord, self.__ship_name
        et coord_occupied.

        RAISES : Si start_coord ou end_coord ne se trouvent pas dans main.all_coord, l'exception IncorrectCoordinates
                 est levée avec le message "Au minimum une des coordonnées ne se trouve pas sur le plateau, recommencez"
        """
        if start_coord not in main.all_coord or end_coord not in main.all_coord:
            raise errors.IncorrectCoordinates(
                "Au minimum une des coordonnées ne se trouve pas sur le plateau, recommencez")
        else:
            self.boat_orientation(start_coord, end_coord, self.__ship_name, coord_occupied)

    def boat_orientation(self, start_coord, end_coord, ship_name, coord_occupied):
        """Cette méthode vérifie si le bateau a été placé horizontalement ou verticalement.
        PRE : start_coord et end_coord sont des coordonnées (string), coord_occupied est une liste de coordonnées (
        string)
                ship_name est le nom du bateau (string)
        POST : En fonction de la fonction du bateau, create_boat est appelée avec les arguments start_coord,
        end_coord, coord_occupied et "x" ou "y"

        RAISES : Si le bateau n'a pas la taille demandée l'erreur IncorrectSize est levée
        """

        if start_coord[0] == end_coord[0]:
            if (int(end_coord[1:]) - int(start_coord[1:])) + 1 == main.ships_available[ship_name]:
                self.create_boat(start_coord, end_coord, coord_occupied, "x")
            else:
                raise errors.IncorrectSize("Erreur, le bateau n'a pas la taille demandée, Recommencez")
        else:
            if (main.alpha_columns.index(end_coord[0]) - main.alpha_columns.index(start_coord[0])) + 1 == \
                    main.ships_available[ship_name]:
                self.create_boat(start_coord, end_coord, coord_occupied, "y")
            else:
                raise errors.IncorrectSize("Erreur, le bateau n'a pas la taille demandée, Recommencez")

    def create_boat(self, start_coord, end_coord, coord_occupied, x_or_y):
        """Cette méthode crée le bateau horizontalement ou verticalement en fonction des coordonnées entrées par
        l'utilisateur
        PRE : start_coord et end_coord sont des coordonnées (string), coord_occupied est une liste de coordonnées (
        string)
              et x_or_y est une string
        POST :  Crée le bateau et actualise la liste des positions occupées par l'équipe
        """

        if x_or_y == "x":
            coord_boat_x = []
            for j in range(int(start_coord[1:]), int(end_coord[1:]) + 1):
                coord_boat_x.append(start_coord[0] + str(j))
            if len(set(coord_boat_x) & set(coord_occupied)) == 0:
                self.coord = coord_boat_x
                for i in coord_boat_x:
                    coord_occupied.append(i)
            else:
                print("Un bateau occupe déjà une ou plusieurs de ces positions, recommencez")
                functions.ask_boat_position(self, coord_occupied)
        else:
            coord_boat_y = []
            for j in range(main.alpha_columns.index(start_coord[0]), main.alpha_columns.index(end_coord[0]) + 1):
                coord_boat_y.append(main.alpha_columns[j] + start_coord[1])
            if len(set(coord_boat_y) & set(coord_occupied)) == 0:
                self.coord = coord_boat_y
                for i in coord_boat_y:
                    coord_occupied.append(i)
            else:
                print("Un bateau occupe déjà une ou plusieurs de ces positions, recommencez")
                functions.ask_boat_position(self, coord_occupied)


class Start(cmd.Cmd):
    """Cette méthode permet le lancement du programme grâce à l'import Cmd
    PRE : La commande doit être connue pour être exécutée
    POST : Lance la méthode choisie par l'utilisateur
    """
    intro = "\nBienvenue dans le jeu Space Battle.\n[help] or [?] : pour la liste des commandes possibles." \
            "\n[start] pour lancer une nouvelle partie.\n[quit] pour quitter le programme."
    prompt = 'Space Battle : '
    file = None

    def do_start(self, arg=0):
        """Lance la partie
        PRE : /
        POST : La partie est lancée
        """

        functions.cls()
        functions.board()
        functions.initialize_teams()
        functions.start_battle()

    def do_quit(self, arg=0):
        """Quitte le programme
        PRE : /
        POST : Le programme est fermé.
        """
        sys.exit()
