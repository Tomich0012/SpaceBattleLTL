import classes
from datetime import datetime, timedelta
import random


ships_available = {"SpaceCruiser": 2, "USS Enterprise": 3}
alpha_columns = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
num_lines = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
mixed_coord = ["A", "1", "B", "2", "C", "3", "D", "4", "E",
               "5", "F", "6", "G", "7," "H", "8", "I", "9", "J", "10"]
team = []
all_coord = []
time_event = (datetime.now() + timedelta(minutes=random.randint(1, 15))).strftime("%H:%M")
storm_activate = []


if __name__ == '__main__':
    classes.Start().cmdloop()
