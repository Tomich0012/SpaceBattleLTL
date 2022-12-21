import classes
import main
import errors
import time
import os


def tempete():
    """
    Cette fonction gère l'événement tempête dans le jeu.

    PRE : main.datetime.now().strftime("%H:%M") doit être égal à main.time_event et main.storm_activate doit être
    une liste vide.

    POST : la tempête est déclenchée et une rangée de la grille de jeu est choisie au hasard pour être touchée par
    la tempête. Les bateaux situés sur cette rangée sont affectés par la tempête.
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
    """
    Sauvegarde les données de la partie dans un fichier texte.

    PRE :
        - start_time est une chaîne de caractères représentant l'heure de début de la partie.
        - winner est une chaîne de caractères représentant le nom du gagnant de la partie.
        - win_condition est une chaîne de caractères représentant la raison pour laquelle le gagnant a gagné.

    POST :
        - Si l'utilisateur répond "YES" à la question de sauvegarde, les données de la partie sont ajoutées au
        fichier texte 'statistics.txt' dans le dossier 'RECORDS'.
        - Si l'utilisateur répond "NO" à la question de sauvegarde, la partie n'est pas sauvegardée.
        - Si l'utilisateur répond autre chose qu'un "YES" ou "NO", une exception de type 'SaveError' est levée.
        """
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
        raise errors.SaveError("Mauvaise entrée, réessayez")


def test_save(start_time, winner, win_condition):
    """
    Teste si la fonction save() renvoie une erreur

    PRE :
        - start_time est un objet datetime représentant l'heure de début de la partie.
        - winner est un objet représentant le gagnant de la partie.
        - win_condition est un objet représentant les conditions de victoire de la partie.
    POST :
        Si l'enregistrement de la partie a réussi, la fonction ne renvoie rien.
        Si l'enregistrement de la partie a échoué, la fonction imprime l'erreur et appelle récursivement la fonction test_save avec les mêmes arguments.
    """
    try:
        save(start_time, winner, win_condition)
    except errors.SaveError as e:
        print(e)
        test_save(start_time, winner, win_condition)


def test_all_checking(ship, start_coord, end_coord, coord_occupied):
    """
    Fonction qui teste si la fonction all_checking() renvoie une erreur

    PRE :
       - ship est une instance de la classe Ship
       - start_coord et end_coord sont des strings de coordonnées (colonnes,lignes) représentant les coordonnées de début et de fin du navire
       - coord_occupied est une liste de coordonnées (string) représentant les coordonnées occupées par des navires
    POST :
       - Si l'exception IncorrectCoordinates est levée, le message d'erreur est affiché et la fonction
       ask_boat_position est appelée avec les arguments ship et coord_occupied
       - Si l'exception IncorrectSize est levée, le message d'erreur est affiché et la fonction
       ask_boat_position est appelée avec les arguments ship et coord_occupied
    """
    try:
        ship.all_checking(start_coord, end_coord, coord_occupied)
    except errors.IncorrectCoordinates as v:
        print(v)
        ask_boat_position(ship, coord_occupied)
    except errors.IncorrectSize as s:
        print(s)
        ask_boat_position(ship, coord_occupied)


def ask_boat_position(ship, coord_occupied):
    """
    Demande et vérifie la position du navire sur la grille.

    PRE :
        - ship est un objet de type Ship.
        - coord_occupied est une liste de coordonnées (chaine de caractères) occupées sur la grille.

    POST :
        - Si la position du navire est valide, elle est ajoutée à coord_occupied et les coordonnées de début et
        de fin du navire sont définies sur les attributs start_coord et end_coord de l'objet ship.
        - Si la position du navire n'est pas valide, l'utilisateur est invité à entrer de nouvelles coordonnées
        jusqu'à ce qu'une position valide soit entrée.
    """
    start_coord = input(f"Entrez maintenant la PREMIERE coordonnée de votre {ship.get_ship_name} qui nécessite "
                        f"{main.ships_available[ship.get_ship_name]} cases : \n").upper()
    end_coord = input(f"Entrez maintenant la DERNIERE coordonnée de votre {ship.get_ship_name} "
                      f"qui nécessite {main.ships_available[ship.get_ship_name]} cases : \n").upper()
    test_all_checking(ship, start_coord, end_coord, coord_occupied)


def board():
    """
    Initialise le board

    PRE : -
    POST : Construit une liste de coordonnées de grille (en lettres et chiffres) en utilisant les valeurs de
    main.alpha_columns et main.num_lines.
    """
    for letter in main.alpha_columns:
        for digit in main.num_lines:
            main.all_coord.append(letter + str(digit))


def cls():
    """
    Nettoie la console

    PRE : -
    POST : Efface le contenu de la console.
    """
    os.system('cls')


def initialize_teams():
    """La fonction initialize_teams initialise les 2 équipes demandant à l'utilisateur de saisir le nom de chaque équipe
    PRE : /
    POST : ajoute ces objets de classe team à la liste main.team.
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
    """
    Fonction qui détermine le/les vainqueurs en cas de temps écoulé

    PRE : start_time est un objet datetime valide représentant le moment où la partie a débuté.
    POST : Affiche le résultat de la partie en fonction du nombre de bateaux restants de chaque équipe. Enregistre
    également les détails de la partie dans un fichier de test.
    """
    print("La partie s'est finie à cause de la limite de temps\n")
    time.sleep(1)
    for i in main.team:
        print(f"Il reste {len(i.board.ships)} bateaux à l'équipe de {i.get_name}\n")
    time.sleep(1)
    if len(main.team[0].board.ships) > len(main.team[1].board.ships):
        print(f"Bravo, c'est l'équipe de {main.team[0].get_name} qui à gagné\n")
        test_save(start_time, main.team[0].get_name, "plus de bateaux vivants que l'autre équipe à la fin du timer")
    elif len(main.team[0].board.ships) < len(main.team[1].board.ships):
        print(f"Bravo, c'est l'équipe de {main.team[1].get_name} qui à gagné\n")
        test_save(start_time, main.team[1].get_name, "plus de bateaux vivants que l'autre équipe à la fin du timer")
    else:
        print(f"Aucun gagnant, ex-aequo\n")
        test_save(start_time, str(main.team[0].get_name + " et " + main.team[1].get_name),
                  "ex-aequo, il reste autant de bateaux vivants aux deux équipes")


def shot_loop(i):
    """
    Fonction qui initialise la boucle de tir

    PRE : i est un objet de type Team
    POST : Retourne une erreur de type IncorrectShot si le tir de l'objet i n'est pas correct,
          sinon retourne une erreur de type Wiped si l'objet i a coulé tous les bateaux adverses.
    """
    while True:
        case_shot = input(f"C'est au tour de {i.get_name} de tirer, où voulez-vous tirer ?\n").upper()
        if str(case_shot) in main.all_coord:
            i.get_fired_shot.append(case_shot)
            result = i.shoot(case_shot)
            if result == "stop":
                time.sleep(2)
                cls()
                raise errors.Wiped(
                    f"Bien joué {i.get_name} vous avez coulé tout les bateaux adverses, vous avez donc gagné\n")
            break
        else:
            raise errors.IncorrectShot("Votre tir n'est pas correct, recommencez")


def test_shot_loop(i, start_time):
    """
    Fonction qui teste si la fonction shot_loop() renvoie une erreur

    PRE : i est un objet de type Team et start_time est un objet de type float
    POST : Si tous les bateaux du joueur i ont été coulés, la fonction renvoie False et affiche un message d'erreur.
          Ensuite, il sera demandé à l'utilisateur s'il veut sauvegarder la partie.
         Si le coup joué est incorrect, la fonction appelle à nouveau la fonction test_shot_loop avec les mêmes
         arguments.
         Sinon, la fonction ne renvoie rien.
    """
    try:
        shot_loop(i)
    except errors.Wiped as w:
        print(w)
        test_save(start_time, i.get_name, "il à coulé tout les bateaux adverses")
        return False
    except errors.IncorrectShot as e:
        print(e)
        test_shot_loop(i, start_time)


def start_battle():
    """ Cette fonction lance le début des tirs entre chaque équipe
    PRE : /
    POST : - L'utilisateur appuie sur la touche "Entrée" pour démarrer la guerre
           - Pour chaque objet Team de la liste main.team, la fonction tempete est appelée,
            puis la fonction test_shot_loop est appelée avec les arguments i (objet Team) et start_time
           - Si la fonction test_shot_loop retourne False, la boucle while est terminée
           - Si l'heure actuelle est supérieure ou égale à time_limit, la fonction time_ended est appelée avec l'argument start_time
    """
    start_time = main.datetime.now().strftime("%d/%m/%Y %H:%M")
    now = main.datetime.now().strftime("%H:%M")
    time_limit = (main.datetime.now() + main.timedelta(minutes=15)).strftime("%H:%M")
    cls()
    input(f"Il est {main.datetime.now().strftime('%H:%M')} Une tempête arrivera sur le plateau à : {main.time_event}\n"
          f"La partie se finira automatiquement à {time_limit}\n"
          f"Appuyez sur [ENTER] pour continuer...")

    while now < time_limit:
        now = main.datetime.now().strftime("%H:%M")
        for i in main.team:
            tempete()
            time.sleep(2)
            cls()
            print(f"\nC'est au tour de {i.get_name} de tirer \n")
            print(f"Voici votre historique de tirs: {i.get_fired_shot}")
            if test_shot_loop(i, start_time) is False:
                now = time_limit
                break
    if main.datetime.now().strftime("%H:%M") >= time_limit:
        time_ended(start_time)
