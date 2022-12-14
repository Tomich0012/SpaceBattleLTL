import functions
import time
import main


class Team:

    def __init__(self, name):
        self.name = name
        self.coord_occupied = []
        self.board = Board(self.name, self.coord_occupied)
        self.fired_shot = []

    def shoot(self, case_shot):
        """Méthode qui permet de valider le tir sur le plateau de l'équipe adverse"""

        for j in main.team:
            if j.name != self.name:
                for a in j.board.ships:
                    if case_shot in a.coord:
                        print(f"\nLa case {case_shot} du {a.name} à été touchée ! Feu à bord\n")
                        a.coord.remove(case_shot)
                        time.sleep(2)
                        if len(a.coord) == 0:
                            j.board.ships.remove(a)
                            functions.cls()
                            print(f"Vous avez coulé le {a.name}\n")
                            if len(j.board.ships) == 0:
                                return "stop"
                        break
                    else:
                        print("Dommage, vous avez raté")
                        time.sleep(2)
                        break


class Board:
    def __init__(self, team_name, coord_occupied):
        self.team = team_name
        self.ships = self.initialize_ships(coord_occupied)

    def initialize_ships(self, coord_occupied):
        """Méthode qui initialise tous les bateaux sans leurs positions pour chaque équipe"""

        ships = []
        for i in main.ships_available:
            ships.append(Ship(i, main.ships_available[i], self.team, coord_occupied))
        return ships


class Ship:
    def __init__(self, name, size, team_name, coord_occupied):
        self.team = team_name
        self.name = name
        self.size = size
        self.coord = []
        functions.ask_boat_position(self, coord_occupied)

    def all_checking(self, start_coord, end_coord, coord_occupied):
        """Méthode qui vérifie les coordonnées de placement du bateau"""

        try:
            if start_coord not in main.all_coord or end_coord not in main.all_coord:
                raise ValueError
            self.boat_orientation(start_coord, end_coord, self.name, coord_occupied)
        except ValueError:
            print("Mauvaise coordonnée, recommencez")
            functions.ask_boat_position(self, coord_occupied)

    def boat_orientation(self, start_coord, end_coord, ship_name, coord_occupied):
        """Méthode qui permet de vérifier si le bateau a été placé horizontalement ou verticalement, et qui appelle create_boat()"""

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
        """Méthode qui créer le bateau horizontalement ou verticalement"""

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
