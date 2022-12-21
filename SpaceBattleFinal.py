import cmd
from datetime import datetime, timedelta
import os
import time
import random
ships_available = {"SpaceCruiser": 2, "USS Enterprise": 3, "X-Wing": 3, "Millennium Falcon": 4, "Star Destroyer": 5}
alpha_columns = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
num_lines = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
mixed_coord = ["A", "1", "B", "2", "C", "3", "D", "4", "E", "5", "F", "6", "G", "7," "H", "8", "I", "9", "J", "10"]
team = []
all_coord = []
time_event = (datetime.now() + timedelta(minutes=random.randint(1, 15))).strftime("%H:%M")
storm_activate = []


def tempete():
    """Fonction qui initialise un évènement aléatoire sur le board"""

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


def save(start_time, winner, win_condition):
    """Fonction qui permet de sauvegarder les statistiques d'une partie terminée à chaque fin de jeu"""

    try:
        response = input("Voulez vous sauvegarder les données de cette partie ? [YES/NO]\n : ").upper()
        if str(response) == "YES":
            ld = os.listdir()
            if "RECORDS" not in ld:
                os.mkdir("RECORDS")
            os.chdir("RECORDS")
            try:
                with open('statistics.txt', 'a') as file:
                    file.write(f"Partie commencée le {start_time} -- finie à {datetime.now().strftime('%H:%M')} -- le "
                               f"gagnant est {winner} car {win_condition}\n")
                    file.close()
            except FileNotFoundError:
                print('Fichier introuvable.')
            except IOError:
                print('Erreur IO.')
            print("Partie sauvegardée, à bientôt...")
            time.sleep(2)
        elif str(response) == "NO":
            print("Partie non sauvegardée, à bientôt...")
            time.sleep(2)
        else:
            raise ValueError
    except ValueError:
        save(start_time, winner, win_condition)


def ask_boat_position(ship, coord_occupied):
    """Fonction qui demande à chaque équipe les cases pour positionner chaque bateau"""

    start_coord = input(f"Entrez maintenant la PREMIERE coordonnée de votre {ship.name} qui nécessite "
                        f"{ships_available[ship.name]} cases : \n").upper()
    end_coord = input(f"Entrez maintenant la DERNIERE coordonnée de votre {ship.name} "
                      f"qui nécessite {ships_available[ship.name]} cases : \n").upper()
    ship.all_checking(start_coord, end_coord, coord_occupied)


def board():
    """Fonction qui initialise un plateau complet de 100 cases"""

    for letter in alpha_columns:
        for digit in num_lines:
            all_coord.append(letter + str(digit))


def cls():
    """Fonction qui permet de nettoyer la console"""
    os.system('cls')


def initialize_teams():
    """Fonction qui initialise les équipes et leurs bateaux respectifs"""

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


def time_ended(start_time):
    """Fonction qui s'exécute si le timer est écoulé et annonce le gagnant en fonction des bateaux restants"""

    print("La partie s'est finie à cause de la limite de temps\n")
    time.sleep(1)
    for i in team:
        print(f"Il reste {len(i.board.ships)} bateaux à l'équipe de {i.name}\n")
    time.sleep(1)
    if len(team[0].board.ships) > len(team[1].board.ships):
        print(f"Bravo, c'est l'équipe de {team[0].name} qui à gagné\n")
        save(start_time, team[0].name, "plus de bateaux vivants que l'autre équipe à la fin du timer")
    elif len(team[0].board.ships) < len(team[1].board.ships):
        print(f"Bravo, c'est l'équipe de {team[1].name} qui à gagné\n")
        save(start_time, team[1].name, "plus de bateaux vivants que l'autre équipe à la fin du timer")
    else:
        print(f"Aucun gagnant, ex-aequo\n")
        save(start_time, str(team[0].name + " et " + team[1].name),
             "ex-aequo, il reste autant de bateaux vivants aux deux équipes")


def start_battle():
    """Fonction qui lance le jeu et permet de tirer sur le plateau de l'équipe adverse chacun à son tour"""

    start_time = datetime.now().strftime("%d:%m:%Y :%H:%M")
    time_limit = (datetime.now() + timedelta(minutes=15)).strftime("%H:%M")
    cls()
    print("Il est", datetime.now().strftime("%H:%M"), "Une tempête arrivera sur le plateau à : ", time_event)
    print(f"La partie se finira automatiquement à {time_limit}")
    time.sleep(3)
    try:
        while datetime.now().strftime("%H:%M") < time_limit:
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
                            time.sleep(2)
                            cls()
                            print(
                                f"Bien joué {i.name} vous avez coulé tout les bateaux adverses, vous avez donc gagné\n")
                            save(start_time, i.name, "il à coulé tout les bateaux adverses")
                            raise Wiped
                        break
                    else:
                        print("Votre tir n'est pas correct, recommencez")
    except Wiped:
        pass
    if datetime.now().strftime("%H:%M") >= time_limit:
        time_ended(start_time)


class Wiped(Exception):
    pass


class Start(cmd.Cmd):
    intro = "\nWelcome to The Space Battle Game.\nhelp or ? : to list commands."
    prompt = 'Space Battle : '
    file = None

    def do_start(self, arg=0):
        """Méthode qui lance le jeu"""

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
        """Méthode qui permet de valider le tir sur le plateau de l'équipe adverse"""

        for j in team:
            if j.name != self.name:
                for a in j.board.ships:
                    if case_shot in a.coord:
                        print(f"\nLa case {case_shot} du {a.name} à été touchée ! Feu à bord\n")
                        a.coord.remove(case_shot)
                        time.sleep(2)
                        if len(a.coord) == 0:
                            j.board.ships.remove(a)
                            cls()
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
        """Méthode qui vérifie les coordonnées de placement du bateau"""

        try:
            if start_coord not in all_coord or end_coord not in all_coord:
                raise ValueError
            self.boat_orientation(start_coord, end_coord, self.name, coord_occupied)
        except ValueError:
            print("Mauvaise coordonnée, recommencez")
            ask_boat_position(self, coord_occupied)

    def boat_orientation(self, start_coord, end_coord, ship_name, coord_occupied):
        """Méthode qui permet de vérifier si le bateau a été placé horizontalement ou verticalement, et qui appelle create_boat()"""

        if start_coord[0] == end_coord[0]:
            if (int(end_coord[1:]) - int(start_coord[1:])) + 1 == ships_available[ship_name]:
                self.create_boat(start_coord, end_coord, coord_occupied, "x")
            else:
                print("Erreur, le bateau n'a pas la taille demandée, Recommencez")
                ask_boat_position(self, coord_occupied)
        else:
            if (alpha_columns.index(end_coord[0]) - alpha_columns.index(start_coord[0])) + 1 == ships_available[
                ship_name]:
                self.create_boat(start_coord, end_coord, coord_occupied, "y")
            else:
                print("Erreur, le bateau n'a pas la taille demandée, Recommencez")
                ask_boat_position(self, coord_occupied)

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
                ask_boat_position(self, coord_occupied)
        else:
            coord_boat_y = []
            for i in range(alpha_columns.index(start_coord[0]), alpha_columns.index(end_coord[0]) + 1):
                coord_boat_y.append(alpha_columns[i] + start_coord[1])
            if len(set(coord_boat_y) & set(coord_occupied)) == 0:
                self.coord = coord_boat_y
                for i in coord_boat_y:
                    coord_occupied.append(i)
            else:
                print("Un bateau occupe déjà une ou plusieurs de ces positions, recommencez")
                ask_boat_position(self, coord_occupied)


if __name__ == '__main__':
    Start().cmdloop()
