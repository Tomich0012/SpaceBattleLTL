import cmd
from datetime import datetime, timedelta
import random

alpha_columns = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
num_lines = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
mixed_coord = ["A", "1", "B", "2", "C", "3", "D", "4", "E", "5", "F", "6", "G", "7," "H", "8", "I", "9", "J", "10"]
ships = {"SpaceCruiser": 2, "USS": 3}
board = []
team = []

""" TODO:  
            clear screen
            crée docstring   
            cfdvrtrghtrtg         
            clean le code 
            
             
"""


def reinit_case(team_name):
    for i in board:
        if team_name == 'all':
            for j in i.cases:
                j.free = "free"
        else:
            if i.team == team_name:
                for j in i.cases:
                    j.free = "free"


def verify_boat(name):
    for i in board:
        compteur = 0
        for j in i.cases:
            if j.free != "occupied":
                compteur += 1
        if compteur == 100:
            print(f"\n\n !!!!!!!!!! gg {name} a gagné \n\n")
            return "stop"


class Start(cmd.Cmd):
    intro = "\nWelcome to The Space Battle Game.\nhelp or ? : to list commands."
    prompt = 'Space Battle : '
    file = None

    def do_a(self, arg=0):
        """
        Start a new game
        """
        equipe1 = input("Entrez le nom de l'equipe 1 ")
        equipe2 = input("Entrez le nom de l'equipe 2 ")
        reinit_case("all")
        team.append(Team(equipe1))
        team.append(Team(equipe2))
        now = datetime.now()
        time_now = now.strftime("%H:%M")
        limit = now + timedelta(minutes=15)
        time_limit = limit.strftime("%H:%M")
        event = now + timedelta(minutes=random.randint(1, 2))
        time_event = event.strftime("%H:%M")

        for i in team:
            print(f"\nIt's up to {i.name} to initialize his boats !\n \n")
            i.placing_ship()
        print("All boat are setup \n")

        while time_now != time_limit:
            for j in team:
                if time_now == time_event or time_now == (event - timedelta(minutes=1)).strftime("%H:%M") \
                        or (event + timedelta(minutes=1)).strftime("%H:%M"):
                    print("Attention la tempête arrive\n")
                    random_num = random.randint(0, 20)
                    print(f"\nLa rangée {mixed_coord[random_num]} est touchée par la tempête ")
                    for a in board:
                        for b in a.cases:
                            if mixed_coord[random_num] in b.coord:
                                b.free = "touched"
                print(f"\nC'est au tour de {j.name} de tirer")
                j.shoot_on()
                if verify_boat(j.name) == "stop":
                    time_now = time_limit
                    break


class Team:
    def __init__(self, name):
        self.name = name
        self.turn = 1
        self.point = 0
        self.board = Board(self.name)
        self.ship = []

    def placing_ship(self):
        for j in ships:
            start_coord = input(f"Enter now the FIRST coordinate of your {j} "
                                f"with a total size of {ships[j]}\n").upper()
            end_coord = input(f"Enter now the LAST coordinate of your {j} with a total size of "
                              f"{ships[j]}\n").upper()
            if len(start_coord) == 2 and len(end_coord):
                if start_coord.isalnum() and end_coord.isalnum():
                    if start_coord[0] in alpha_columns and start_coord[1:] in str(num_lines):
                        if end_coord[0] in alpha_columns and end_coord[1:] in str(num_lines):
                            self.ship.append(Ship(start_coord, end_coord, j, self.name))
                        else:
                            print("Mauvaise coordonées de fin recommencez svp ")
                            reinit_case(self.name)
                            self.placing_ship()
                    else:
                        print("Mauvaise coordonées de debut recommencez svp ")
                        reinit_case(self.name)
                        self.placing_ship()
                else:
                    print("Mauvaise coordonées recommencez svp ")
                    reinit_case(self.name)
                    self.placing_ship()
            else:
                print("Veuillez entrer une coordonnée de taille 2")
                reinit_case(self.name)
                self.placing_ship()

    def shoot_on(self):
        shot = input("Where do you wanna shoot ? ").upper()
        if shot.isalnum() and shot[0] in alpha_columns and shot[1:] in str(num_lines):
            for i in board:
                if i.team != self.name:
                    for j in i.cases:
                        if shot == j.coord:
                            if j.free == "occupied":
                                j.free = "touched"
                                print("Touché bg ")
                            else:
                                print("Raté fdp")
        else:
            print("Mauvaise coordonnée de shot réessayez ")
            self.shoot_on()

    def ask_board_position(self):
        pass

    def __str__(self):
        return f"equipe {self.name} crée !  "


class Board:
    def __init__(self, team_name):

        self.team = team_name
        self.columns = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        self.lines = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        self.cases = []
        board.append(self)
        for letter in self.columns:
            for digit in self.lines:
                case = Case(letter + digit)
                self.cases.append(case)

    def __str__(self):
        return f"voici les cases  : {self.cases}"

    def ask_case_position(self):
        pass


class Case:
    def __init__(self, coord):
        # self.__class__.instances.append(self)
        self.coord = coord
        self.free = "free"

    def __str__(self):
        return f"voici les coord  : {self.coord} : {self.free}"


class Ship:

    def __init__(self, start, end, name, team_name):
        self.start = start
        self.end = end
        self.coord = []
        self.name = name
        self.team = team_name
        self.check_orientation(name, start, end)
        self.create_case()

    def check_coord_already_used(self):
        for a in self.coord:
            for i in board:
                if i.team == self.team:
                    for j in i.cases:
                        if j.coord == a:
                            if j.free == "free":
                                return True
                            else:
                                return False

    def reinit_case(self):
        for i in board:
            if i.team == self.team:
                for j in i.cases:
                    j.free = "free"

    def create_boat_x(self, start_coord, end_coord):
        """create the boat in X case"""
        coord_boat_x = []
        for i in range(int(start_coord[1:]), int(end_coord[1:]) + 1):
            coord_boat_x.append(start_coord[0] + str(i))
        self.coord = coord_boat_x
        self.check_coord_already_used()
        if not self.check_coord_already_used():
            print("a boat is already in those coord")
            for i in team:
                if i.name == self.team:
                    reinit_case(self.team)
                    i.placing_ship()

    def create_boat_y(self, start_coord, end_coord):
        """create the boat in Y case"""
        coord_boat_y = []
        for i in range(alpha_columns.index(start_coord[0]), alpha_columns.index(end_coord[0]) + 1):
            coord_boat_y.append(alpha_columns[i] + start_coord[1])
        self.coord = coord_boat_y
        if not self.check_coord_already_used():
            print("a boat is already in those coord")
            for i in team:
                if i.name == self.team:
                    reinit_case(self.team)
                    i.placing_ship()

    def check_orientation(self, nom, start_coord, end_coord):
        """this function check if the boat is in X way or Y way"""

        if start_coord[0] == end_coord[0]:
            if (int(end_coord[1:]) - int(start_coord[1:])) + 1 == ships[nom]:
                self.create_boat_x(start_coord, end_coord)
            else:
                print("Le bateau n'a pas la taille demandée, Recommencer")
                self.start = input(f"Enter now the FIRST coordinate of your {self.name} \n")
                self.end = input(f"Enter now the LAST coordinate of your {self.name}\n")
                self.check_orientation(nom, self.start, self.end)

        else:
            if (alpha_columns.index(end_coord[0]) - alpha_columns.index(start_coord[0])) + 1 == ships[nom]:
                self.create_boat_y(start_coord, end_coord)
            else:
                print("Le bateau n'a pas la taille demandée, Recommencer")
                self.start = input("Debut")
                self.end = input("Fin")
                self.check_orientation(nom, self.start, self.end)

    def create_case(self):
        """#map(lambda x: Case(x, False), self.coord)"""
        for i in board:
            if i.team == self.team:
                for j in i.cases:
                    if j.coord in self.coord:
                        j.free = "occupied"

    def __str__(self):
        return f"bateau team {self.team}  : {self.name} {self.coord}"


if __name__ == '__main__':
    Start().cmdloop()
