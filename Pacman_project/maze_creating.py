import random
import math


from maze_showing import show_maze


# Die Funktion zum Erstellen eines Labyrinthgitters
def grid_creating(n):
    x = (2 ** n) + 1  # Zufallslabyrinthgenerierungsfunktion

    grid_to_create = []  # Zweidimensionales Array

    for i in range(0, x):  # Zyklus, um das Labyrinth mit einem Gitter zu füllen
        grid_to_create.append([])  # Fügen dem Hauptarray hinzu

        if i % 2 == 0:  # Gerade Zeilenindex
            for j in range(0, x):
                grid_to_create[i].append(True)  # True - gefüllter Käfig

        else:  # Ungerader Zeilenindex
            for j in range(0, x):
                if j % 2 == 0:  # Gerader Zellindex
                    grid_to_create[i].append(True)
                else:  # Ungerader Zellindex
                    grid_to_create[i].append(False)  # False - leerer Käfig

    return grid_to_create


def show_grid(grid_to_show):
    print()
    filled_cell = '▆'  # True
    empty_cell = ' '  # False

    for i in range(0, len(grid_to_show)):  # Zyklus zum Füllen des Gitters

        for j in range(0, len(grid_to_show)):

            if grid_to_show[i][j]:
                print(filled_cell, end=' ')

            else:
                print(empty_cell, end=' ')
        print()
    print()


def choose_direction():
    rand = random.random()
    if rand <= 0.25:
        return 'North'
    elif rand <= 0.5:
        return 'East'
    elif rand <= 0.75:
        return 'South'
    else:
        return 'West'


def centre_calculation(n):
    return ((2 ** n + 2) / 2) - 1  # Berechnungsformel für das Zentrum des Labyrinths


if __name__ == '__main__':

    # Funktion zum Erstellen von Löchern an drei Seiten
    def delete_three_sides(x, y):
        if remaining_side == 'North':  # Erzeugen Löcher auf der Nordseite
            grid[int(x)][int(y + 1)] = False
            grid[int(x + 1)][int(y)] = False
            grid[int(x)][int(y - 1)] = False
        elif remaining_side == 'East':  # Erzeugen Löcher auf der Ostseite
            grid[int(x - 1)][int(y)] = False
            grid[int(x + 1)][int(y)] = False
            grid[int(x)][int(y - 1)] = False
        elif remaining_side == 'South':  # Erzeugen Löcher auf der Südseite
            grid[int(x)][int(y + 1)] = False
            grid[int(x - 1)][int(y)] = False
            grid[int(x)][int(y - 1)] = False
        elif remaining_side == 'West':  # Erzeugen Löcher auf der Westseite
            grid[int(x)][int(y + 1)] = False
            grid[int(x + 1)][int(y)] = False
            grid[int(x - 1)][int(y)] = False

    # Rekursive Abstiegsfunktion
    def recursive_descent(x, y, level):
        delete_three_sides(x, y)

        step = 2 ** (n - 2)

        if level == 1:

            if n == 2:  # Sonderfall für n = 2
                step = 0

            # Alle Optionen für den rekursiven Abstieg in alle Richtungen
            recursive_descent(x + step, y + step, level + 1)
            recursive_descent(x + step, y - step, level + 1)
            recursive_descent(x - step, y + step, level + 1)
            recursive_descent(x - step, y - step, level + 1)
        
        # Alle Optionen für den rekursiven Abstieg in alle Richtungen mit festgelegten Schritten
        elif level < ((step - 2) / 2) + 2:
            recursive_descent(x + 2, y + 2, level + 1)
            recursive_descent(x + 2, y - 2, level + 1)
            recursive_descent(x - 2, y + 2, level + 1)
            recursive_descent(x - 2, y - 2, level + 1)

# Funktion zum Erstellen zufälliger Löcher
    def make_random_holes(center, amount, step):
        if step == 1:
            return
        elif step == 2:
            for i in range(0, amount):
                # West
                if i % 2 == 0:
                    empty_hole = math.ceil(random.random() * step)
                    grid[center][empty_hole * 2 - 1] = False
                # East
                if i % 2 == 1:
                    empty_hole = math.ceil(random.random() * step)
                    grid[center][empty_hole * 2 + center - 1] = False
        else:
            for i in range(0, amount):
                # West
                if i % 4 == 0:
                    empty_hole = math.ceil(random.random() * step)  # Randomisiertes Loch an der Seite
                    grid[center][empty_hole * 2 - 1] = False  # Machen ein Loch
                # North
                if i % 4 == 1:
                    empty_hole = math.ceil(random.random() * step)  # Randomisiertes Loch an der Seite
                    grid[empty_hole * 2 - 1][center] = False  # Machen ein Loch
                # East
                if i % 4 == 2:
                    empty_hole = math.ceil(random.random() * step)  # Randomisiertes Loch an der Seite
                    grid[center][empty_hole * 2 + center - 1] = False  # Machen ein Loch
                # South
                if i % 4 == 3:
                    empty_hole = math.ceil(random.random() * step)  # Randomisiertes Loch an der Seite
                    grid[empty_hole * 2 + center - 1][center] = False  # Machen ein Loch


    # Alle Funktionen in main aufrufen
    n = int(input('n: '))
    grid = grid_creating(n)
    print()
    show_grid(grid)
    remaining_side = choose_direction()
    recursive_descent(centre_calculation(n), centre_calculation(n), 1)
    make_random_holes(int(centre_calculation(n)), amount=2 ** (n - 2), step=2 ** (n - 2))
    show_grid(grid)

    show_maze(grid, n)  # Schlussfolgerung des Labyrinths
