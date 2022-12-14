import cmd
from datetime import datetime, timedelta
import random
import functions
import sys

ships_available = {"SpaceCruiser": 2}
alpha_columns = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
num_lines = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
mixed_coord = ["A", "1", "B", "2", "C", "3", "D", "4", "E", "5", "F", "6", "G", "7," "H", "8", "I", "9", "J", "10"]
team = []
all_coord = []
time_event = (datetime.now() + timedelta(minutes=random.randint(1, 15))).strftime("%H:%M")
storm_activate = []


class Start(cmd.Cmd):
    intro = "\nBienvenue dans le jeu Space Battle.\n[help] or [?] : pour la liste des commandes possibles." \
            "\n[start] pour lancer une nouvelle partie.\n[quit] pour quitter le programme."
    prompt = 'Space Battle : '
    file = None

    def do_start(self, arg=0):
        """Méthode qui lance le jeu"""

        functions.board()
        functions.initialize_teams()
        functions.start_battle()

    def do_quit(self, arg=0):
        """Méthode qui permet de quitter le jeu"""
        sys.exit()


if __name__ == '__main__':
    Start().cmdloop()