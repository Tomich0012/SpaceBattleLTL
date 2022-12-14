import classes
import main
import errors
import time
import os


def tempete():
    """Fonction qui initialise un évènement aléatoire sur le board"""

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
    """Fonction qui demande à chaque équipe les cases pour positionner chaque bateau"""

    start_coord = input(f"Entrez maintenant la PREMIERE coordonnée de votre {ship.name} qui nécessite "
                        f"{main.ships_available[ship.name]} cases : \n").upper()
    end_coord = input(f"Entrez maintenant la DERNIERE coordonnée de votre {ship.name} "
                      f"qui nécessite {main.ships_available[ship.name]} cases : \n").upper()
    ship.all_checking(start_coord, end_coord, coord_occupied)


def board():
    """Fonction qui initialise un plateau complet de 100 cases"""

    for letter in main.alpha_columns:
        for digit in main.num_lines:
            main.all_coord.append(letter + str(digit))


def cls():
    """Fonction qui permet de nettoyer la console"""
    os.system('cls')


def initialize_teams():
    """Fonction qui initialise les équipes et leurs bateaux respectifs"""

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
    """Fonction qui s'exécute si le timer est écoulé et annonce le gagnant en fonction des bateaux restants"""

    print("La partie s'est finie à cause de la limite de temps\n")
    time.sleep(1)
    for i in main.team:
        print(f"Il reste {len(i.board.ships)} bateaux à l'équipe de {i.name}\n")
    time.sleep(1)
    if len(main.team[0].board.ships) > len(main.team[1].board.ships):
        print(f"Bravo, c'est l'équipe de {main.team[0].name} qui à gagné\n")
        save(start_time, main.team[0].name, "plus de bateaux vivants que l'autre équipe à la fin du timer")
    elif len(main.team[0].board.ships) < len(main.team[1].board.ships):
        print(f"Bravo, c'est l'équipe de {main.team[1].name} qui à gagné\n")
        save(start_time, main.team[1].name, "plus de bateaux vivants que l'autre équipe à la fin du timer")
    else:
        print(f"Aucun gagnant, ex-aequo\n")
        save(start_time, str(main.team[0].name + " et " + main.team[1].name),
             "ex-aequo, il reste autant de bateaux vivants aux deux équipes")


def start_battle():
    """Fonction qui lance le jeu et permet de tirer sur le plateau de l'équipe adverse chacun à son tour"""

    start_time = main.datetime.now().strftime("%d:%m:%Y :%H:%M")
    time_limit = (main.datetime.now() + main.timedelta(minutes=15)).strftime("%H:%M")
    cls()
    print("Il est", main.datetime.now().strftime("%H:%M"), "Une tempête arrivera sur le plateau à : ", main.time_event)
    print(f"La partie se finira automatiquement à {time_limit}")
    time.sleep(3)
    try:
        while main.datetime.now().strftime("%H:%M") < time_limit:
            for i in main.team:
                tempete()
                time.sleep(2)
                cls()
                print(f"\nC'est au tour de {i.name} de tirer \n")
                print(f"Voici votre historique de tirs: {i.fired_shot}")
                while True:
                    case_shot = input(f"C'est au tour de {i.name} de tirer, où voulez-vous tirer ?\n").upper()
                    if str(case_shot) in main.all_coord:
                        i.fired_shot.append(case_shot)
                        result = i.shoot(case_shot)
                        if result == "stop":
                            time.sleep(2)
                            cls()
                            print(
                                f"Bien joué {i.name} vous avez coulé tout les bateaux adverses, vous avez donc gagné\n")
                            save(start_time, i.name, "il à coulé tout les bateaux adverses")
                            raise errors.Wiped
                        break
                    else:
                        print("Votre tir n'est pas correct, recommencez")
    except errors.Wiped:
        pass
    if main.datetime.now().strftime("%H:%M") >= time_limit:
        time_ended(start_time)
