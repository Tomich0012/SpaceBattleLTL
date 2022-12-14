import cmd
from datetime import datetime, timedelta
import os
import time
import random

ships_available = {"SpaceCruiser": 2, "uss": 3}
alpha_columns = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
num_lines = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
mixed_coord = ["A", "1", "B", "2", "C", "3", "D", "4", "E", "5", "F", "6", "G", "7," "H", "8", "I", "9", "J", "10"]
team = []
all_coord = []
time_event = (datetime.now() + timedelta(minutes=random.randint(0, 4))).strftime("%H:%M")
storm_activate = []


class LenghtError(Exception):
    print("tg")
    pass


class CoordError(Exception):
    pass


class OccupedError(Exception):
    pass


def tempete():
    if datetime.now().strftime("%H:%M") == time_event and storm_activate == []:
        storm_activate.append("storm happened")
        print("Attention, la tempête frappe\n")
        time.sleep(2)
        random_num = random.randint(0, 20)
        print(f"La rangée {mixed_coord[random_num]} a été touchée par la tempête\n")
        for i in team:
            for j in i.board.ships:
                for pos in j.coord:
                    if mixed_coord[random_num] in pos:
                        print(f"Le bateau {j.name} de {i.name} à été frappé par la tempête")
                        j.coord.remove(pos)


def ask_boat_position(ship, coord_occupied):
    start_coord = input(f"Entrez maintenant la PREMIERE coordonnée de votre {ship.name} qui nécessite "
                        f"{ships_available[ship.name]} cases : \n").upper()
    end_coord = input(f"Entrez maintenant la DERNIERE coordonnée de votre {ship.name} "
                      f"qui nécessite {ships_available[ship.name]} cases : \n").upper()
    ship.all_checking(start_coord, end_coord, coord_occupied)


def board():
    for letter in alpha_columns:
        for digit in num_lines:
            all_coord.append(letter + str(digit))


def cls():
    """Fonction qui permet de clean la console"""
    os.system('cls')


def initialize_teams():
    team.clear()
    equipe1 = input("Entrez le nom de l'équipe 1 ")
    equipe2 = input("Entrez le nom de l'équipe 2 ")
    cls()
    print(f"\n \nC'est au tour de {equipe1} d'initialiser ses bateaux\n")
    time.sleep(1)
    team.append(Team(equipe1))
    cls()
    print(f"\n \nC'est au tour de {equipe2} d'initialiser ses bateaux\n")
    time.sleep(1)
    team.append(Team(equipe2))


def start_battle():
    time_limit = (datetime.now() + timedelta(minutes=2)).strftime("%H:%M")
    cls()
    print("Il est", datetime.now().strftime("%H:%M"), "Une tempête arrivera sur le plateau à : ", time_event)
    print(f"La partie se finira automatiquement à {time_limit}")
    time.sleep(3)
    while datetime.now().strftime("%H:%M") != time_limit:
        for i in team:
            tempete()
            time.sleep(2)
            cls()
            print(f"\nC'est au tour de {i.name} de tirer \n")
            print(f"Voici votre historique de tirs: {i.fired_shot}")
            while True:
                case_shot = input(f"C'est au tour de {i.name} de tirer, où voulez-vous tirer ?\n").upper()
                if str(case_shot) in all_coord:
                    i.fired_shot.append(case_shot)
                    result = i.shoot(case_shot)
                    if result == "stop":
                        print(f"Bien joué {i.name} vous avez coulé tout les bateaux adverses, vous avez donc gagné\n")
                        break
                    break
                else:
                    print("Votre tir n'est pas correct, recommencez")
    print("La partie s'est finie à cause de la limite de temps\n")
    time.sleep(1)
    for i in team:
        print(f"Il reste {len(i.board.ships)} bateaux à l'équipe de {i.name}\n")
    time.sleep(1)
    if len(team[0].board.ships) > len(team[1].board.ships):
        print(f"Bravo, c'est l'équipe de {team[0].name} qui à gagné\n")
    elif len(team[0].board.ships) < len(team[1].board.ships):
        print(f"Bravo, c'est l'équipe de {team[1].name} qui à gagné\n")
    else:
        print(f"Aucun gagnant, ex-aequo\n")


class Start(cmd.Cmd):
    intro = "\nWelcome to The Space Battle Game.\nhelp or ? : to list commands."
    prompt = 'Space Battle : '
    file = None

    def do_s(self, arg=0):
        board()
        initialize_teams()
        start_battle()


class Team:

    def __init__(self, name):
        self.name = name
        self.coord_occupied = []
        self.board = Board(self.name, self.coord_occupied)
        self.fired_shot = []

    def shoot(self, case_shot):
        for j in team:
            if j.name != self.name:
                for a in j.board.ships:
                    if case_shot in a.coord:
                        print(f"\nLa case {case_shot} du {a.name} à été touchée ! Feu à bord\n")
                        a.coord.remove(case_shot)
                        time.sleep(2)
                        if len(a.coord) == 0:
                            j.board.ships.remove(a)
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
        ships = []
        for i in ships_available:
            ships.append(Ship(i, ships_available[i], self.team, coord_occupied))
        return ships


class Ship:
    def __init__(self, name, size, team_name, coord_occupied):
        self.team = team_name
        self.name = name
        self.size = size
        self.coord = []
        ask_boat_position(self, coord_occupied)

    def all_checking(self, start_coord, end_coord, coord_occupied):
        try:
            if start_coord not in all_coord or end_coord not in all_coord:
                raise ValueError
            self.boat_orientation(start_coord, end_coord, self.name, coord_occupied)
        except ValueError:
            print("Mauvaise coordonnée, recommencez")
            ask_boat_position(self, coord_occupied)

    def boat_orientation(self, start_coord, end_coord, ship_name, coord_occupied):
        try:
            if start_coord[0] == end_coord[0]:
                if not (int(end_coord[1:]) - int(start_coord[1:])) + 1 == ships_available[ship_name]:
                    raise ValueError
                self.create_boat_x(start_coord, end_coord, coord_occupied)
            else:
                if not (alpha_columns.index(end_coord[0]) - alpha_columns.index(start_coord[0])) + 1 == ships_available[ship_name]:
                    raise ValueError
                self.create_boat_y(start_coord, end_coord, coord_occupied)

        except LenghtError:
            # print("Erreur, le bateau n'a pas la taille demandée, Recommencez")
            ask_boat_position(self, coord_occupied)

    def create_boat_x(self, start_coord, end_coord, coord_occupied):
        """Create the boat in X case"""
        try:
            coord_boat_x = []
            for i in range(int(start_coord[1:]), int(end_coord[1:]) + 1):
                coord_boat_x.append(start_coord[0] + str(i))
            if not len(set(coord_boat_x) & set(coord_occupied)) == 0:
                raise ValueError
            self.coord = coord_boat_x
            for i in coord_boat_x:
                coord_occupied.append(i)
        except ValueError:
            print("Un bateau occupe déjà une ou plusieurs de ces positions, recommencez")
            ask_boat_position(self, coord_occupied)

    def create_boat_y(self, start_coord, end_coord, coord_occupied):
        """Create the boat in Y case"""
        try:
            coord_boat_y = []
            for i in range(alpha_columns.index(start_coord[0]), alpha_columns.index(end_coord[0]) + 1):
                coord_boat_y.append(alpha_columns[i] + start_coord[1])
            if not len(set(coord_boat_y) & set(coord_occupied)) == 0:
                raise ValueError
            self.coord = coord_boat_y
            for i in coord_boat_y:
                coord_occupied.append(i)
        except ValueError:
            print("Un bateau occupe déjà une ou plusieurs de ces positions, recommencez")
            ask_boat_position(self, coord_occupied)



if __name__ == '__main__':
    Start().cmdloop()
