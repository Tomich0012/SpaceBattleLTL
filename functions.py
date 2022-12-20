import classes
import main
import errors
import time
import os


def tempete():
    """This function start a random storm on the board in the game. 
    PRE : /
    POST : A random row automatically switches to “touch”.
    """
    if main.datetime.now().strftime("%H:%M") == main.time_event and main.storm_activate == []:
        main.storm_activate.append("storm happened")
        print("Attention, la tempête frappe\n")
        time.sleep(2)
        random_num = main.random.randint(0, 20)
        print(f"La rangée {main.mixed_coord[random_num]} a été touchée par la tempête\n")
        for i in main.team:
            for j in i.board.ships:
                for pos in j.coord:
                    if main.mixed_coord[random_num] in pos:
                        print(f"Le bateau {j.get_ship_name} de {i.get_name} à été frappé par la tempête")
                        j.coord.remove(pos)


def save(start_time, winner, win_condition):
    """This function save the game if the answer is “YES”
    PRE : /
    POST :  If the answer is “YES” the game is saved in 'statistics.txt' in the directory 'RECORDS', and a message is print.
            If the answer is “NO”, the game isn't saved, and the program shuts.
    RAISES : ValueError if the answer is not “YES” or “NOT”.
    """

    try:
        response = input("Voulez vous sauvegarder les données de cette partie ? [YES/NO]\n : ").upper()
        if str(response) == "YES":
            ld = os.listdir()
            if "RECORDS" not in ld:
                os.mkdir("RECORDS")
            os.chdir("RECORDS")
            try:
                with open('statistics.txt', 'a') as file:
                    file.write(f"Partie commencée le {start_time} -- finie à {main.datetime.now().strftime('%H:%M')} -- le "
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
    """This function asks each team the boxes to position each boat.
    PRE : /
    POST : The coordinates of each boat is sent to the method 'all.checking' from the Ship class.
    """

    start_coord = input(f"Entrez maintenant la PREMIERE coordonnée de votre {ship.get_ship_name} qui nécessite "
                        f"{main.ships_available[ship.get_ship_name]} cases : \n").upper()
    end_coord = input(f"Entrez maintenant la DERNIERE coordonnée de votre {ship.get_ship_name} "
                      f"qui nécessite {main.ships_available[ship.get_ship_name]} cases : \n").upper()
    ship.all_checking(start_coord, end_coord, coord_occupied)


def board():
    """This function initializes a complete board of 100 cells.
    PRE : /
    POST : A board of 10×10 cells is created.
    """

    for letter in main.alpha_columns:
        for digit in main.num_lines:
            main.all_coord.append(letter + str(digit))


def cls():
    """This function clean the console.
    PRE : / 
    POST : The console is clean.
    """
    os.system('cls')


def initialize_teams():
    """This function initializes the teams, and their respective boats
    PRE : /
    POST : Two teams are add to 'team' with the chosen name in the class 'main'.
    """

    main.team.clear()
    equipe1 = input("Entrez le nom de l'équipe 1 ")
    equipe2 = input("Entrez le nom de l'équipe 2 ")
    cls()
    print(f"\n \nC'est au tour de {equipe1} d'initialiser ses bateaux\n")
    time.sleep(1)
    main.team.append(classes.Team(equipe1))
    cls()
    print(f"\n \nC'est au tour de {equipe2} d'initialiser ses bateaux\n")
    time.sleep(1)
    main.team.append(classes.Team(equipe2))


def time_ended(start_time):
    """This function runs if the timer is over and announces the winner according to the remaining boats
    PRE : /
    POST :  If a team win the winner is announced
            If both team have the same boats alive at the end of the timer, it is ex-aequo.
    """

    print("La partie s'est finie à cause de la limite de temps\n")
    time.sleep(1)
    for i in main.team:
        print(f"Il reste {len(i.board.ships)} bateaux à l'équipe de {i.get_name}\n")
    time.sleep(1)
    if len(main.team[0].board.ships) > len(main.team[1].board.ships):
        print(f"Bravo, c'est l'équipe de {main.team[0].get_name} qui à gagné\n")
        save(start_time, main.team[0].get_name, "plus de bateaux vivants que l'autre équipe à la fin du timer")
    elif len(main.team[0].board.ships) < len(main.team[1].board.ships):
        print(f"Bravo, c'est l'équipe de {main.team[1].get_name} qui à gagné\n")
        save(start_time, main.team[1].get_name, "plus de bateaux vivants que l'autre équipe à la fin du timer")
    else:
        print(f"Aucun gagnant, ex-aequo\n")
        save(start_time, str(main.team[0].get_name + " et " + main.team[1].get_name),
             "ex-aequo, il reste autant de bateaux vivants aux deux équipes")


def start_battle():
    """This function start the game and allows you to shoot at the opposing team's board in turn
    PRE : /
    POST : Starts the game and runs the game.
    """

    start_time = main.datetime.now().strftime("%d:%m:%Y :%H:%M")
    time_limit = (main.datetime.now() + main.timedelta(minutes=15)).strftime("%H:%M")
    cls()
    input(f"Il est {main.datetime.now().strftime('%H:%M')} Une tempête arrivera sur le plateau à : {main.time_event}\n"
          f"La partie se finira automatiquement à {time_limit}\n"
          f"Appuyez sur [ENTER] pour continuer...")
    cls()
    try:
        while main.datetime.now().strftime("%H:%M") < time_limit:
            for i in main.team:
                tempete()
                time.sleep(2)
                cls()
                print(f"\nC'est au tour de {i.get_name} de tirer \n")
                print(f"Voici votre historique de tirs: {i.fired_shot}")
                while True:
                    case_shot = input(f"C'est au tour de {i.get_name} de tirer, où voulez-vous tirer ?\n").upper()
                    if str(case_shot) in main.all_coord:
                        i.fired_shot.append(case_shot)
                        result = i.shoot(case_shot)
                        if result == "stop":
                            time.sleep(2)
                            cls()
                            print(
                                f"Bien joué {i.get_name} vous avez coulé tout les bateaux adverses, vous avez donc gagné\n")
                            save(start_time, i.get_name, "il à coulé tout les bateaux adverses")
                            raise errors.Wiped
                        break
                    else:
                        print("Votre tir n'est pas correct, recommencez")
    except errors.Wiped:
        pass
    if main.datetime.now().strftime("%H:%M") >= time_limit:
        time_ended(start_time)
