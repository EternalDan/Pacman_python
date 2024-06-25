import random
import stddraw
import time

CANVAS_SIZE = 800


# Funktion zum Zeichnen von Labyrinthrahmen
def show_frames(n):
    s = (2 ** n) + 1  # s = canvas size
    # bottom side
    for i in range(0, s):
        stddraw.square(i / s + (1 / s) / 2, (1 / s) / 2, (1 / s) / 2)
    # left side
    for i in range(0, s):
        stddraw.square((1 / s) / 2, i / s + (1 / s) / 2, (1 / s) / 2)
    # top side
    for i in range(0, s):
        stddraw.square(i / s + (1 / s) / 2, 1 - (1 / s) / 2, (1 / s) / 2)
    # right side
    for i in range(0, s):
        stddraw.square(1 - (1 / s) / 2, i / s + (1 / s) / 2, (1 / s) / 2)


def get_swap_dict(d):
    return {v: k for k, v in d.items()}  # Tauschen keys und value an Orten aus


def choose_direction_for_enemy(maze, x, y, current_direction):
    directions_dict = {'up': False, 'down': False, 'left': False, 'right': False, 'dead': False}  # Wörterbuch der Richtungen

    if current_direction == 'none':  # Der Feind steht still
        if not maze[y + 1][x]:  # Kein Labyrinth
            directions_dict['up'] = True  # Aufwärtsbewegung
        if not maze[y - 1][x]:  # Kein Labyrinth
            directions_dict['down'] = True  # Abwärtsbewegung
        if not maze[y][x - 1]:  # Kein Labyrinth
            directions_dict['left'] = True  # Bewegung nach links
        if not maze[y][x + 1]:  # Kein Labyrinth
            directions_dict['right'] = True  # Bewegung nach rechts
        directions_amount = sum(list(directions_dict.values()))
        if directions_amount == 1:  # Wenn es eine einzige Richtung gibt
            return get_swap_dict(directions_dict)[True]  # Bewegung in diese Richtung

        else:  # Wenn es mehr als eine Richtung gibt
            keys_list = list(directions_dict.keys())  # Nehmen eine separate Liste aus keys des Wörterbuchs
            values_list = list(directions_dict.values())  # Nehmen eine separate Liste aus values des Wörterbuchs
            rest_direction_list = []  # Sammeln die verbleibenden Richtungen an

            for i in range(0, 4):  # Gehen durch alle values
                if values_list[i]:  # Wenn True
                    rest_direction_list.append(keys_list[i])  # Zur Liste hinzufügen
            return random.choice(rest_direction_list)  # Zufällige Richtungsauswahl aus der Liste

    else:  # Der Feind bewegt sich
        if not maze[y + 1][x]:  # Kein Labyrinth
            directions_dict['up'] = True  # Aufwärtsbewegung
        if not maze[y - 1][x]:  # Kein Labyrinth
            directions_dict['down'] = True  # Abwärtsbewegung
        if not maze[y][x - 1]:  # Kein Labyrinth
            directions_dict['left'] = True  # Bewegung nach links
        if not maze[y][x + 1]:  # Kein Labyrinth
            directions_dict['right'] = True  # Bewegung nach rechts

        if directions_dict[current_direction]:  # Wenn unsere Richtung frei ist
            return current_direction  # Aktuelle Richtung zurückgeben
        else:  # Wenn es eine Wand gibt
            return 'none'  # Bleiben vor Ort stehen


def create_enemies(s, n):
    enemies_coordinates = []  # Liste mit Feindkoordinaten
    enemies_directions = []  # Liste mit Feindrichtungen
    if n == 3:
        enemies_coordinates.append([7, 7])  # Die Koordinate des Auftretens des Feindes
        enemies_directions.append('none')  # Der Feind steht still
    elif n > 3:
        enemies_coordinates.append([1, s - 2])
        enemies_coordinates.append([s - 2, s - 2])  # Die Koordinaten des Auftretens von Feinden
        enemies_coordinates.append([s - 2, 1])
        enemies_directions.append('none')
        enemies_directions.append('none')  # Die Feinde stehen still
        enemies_directions.append('none')

    return enemies_coordinates, enemies_directions  # Listen übergeben


def create_points(s, maze):
    points = []  # Liste der Punkte

    for i in range(0, s):  # Gehen durch alle Zeilen
        points.append([])  # Fügen in Array Punkte hinzu
        for j in range(0, s):  # Gehen durch alle Spalten

            if not maze[i][j]:  # Wenn gibt es keine Wand
                points[i].append(True)  # Fügen einen Punkt hinzu
            else:  # Wenn gibt es eine Wand
                points[i].append(False)  # Fügen keinen Punkt hinzu

    return points


def create_power_points(enemies_coordinates, s):
    power_points = []  # Liste mit Punkten des zweiten Typs

    for i in range(0, len(enemies_coordinates)):  # Erstellen Punkte des zweiten Typs gleich der Anzahl der Feinde
        # Erzeugen zufällig die Koordinaten der Punkte des zweiten Typs in einer bestimmten Zone
        pp_x = random.randrange(3, s - 3, 2)
        pp_y = random.randrange(3, s - 3, 2)
        power_points.append([pp_x, pp_y])  # Fügen in Array Punkte des zweiten Typs hinzu

    return power_points


def lose_the_game():
    # Text: GAME OVER
    stddraw.clear(stddraw.BLACK)  # Hintergrundfarbe
    stddraw.setFontSize(90)  # Schriftgröße
    stddraw.setPenColor(stddraw.WHITE)  # Textfarbe
    stddraw.text(0.5, 0.5, "GAME OVER")  # Text und seine Position
    stddraw.show(2000)  # Bildschirmtextzeit (ms)
    # Text: You lose!
    stddraw.clear(stddraw.DARK_RED)  # Hintergrundfarbe
    stddraw.setFontSize(128)  # Schriftgröße
    stddraw.setPenColor(stddraw.WHITE)  # Textfarbe
    stddraw.text(0.5, 0.5, "You lose!")  # Text und seine Position
    stddraw.show(3500)  # Bildschirmtextzeit (ms)


def win_the_game():
    # Text: You win!
    stddraw.clear(stddraw.DARK_GREEN)  # Hintergrundfarbe
    stddraw.setFontSize(128)  # Schriftgröße
    stddraw.setPenColor(stddraw.WHITE)  # Textfarbe
    stddraw.text(0.5, 0.5, "You win!")  # Text und seine Position
    stddraw.show(3500)  # Bildschirmtextzeit (ms)


def draw_points_and_pacman(s, half_sq, maze, points, x, y):
    for i in range(0, s):  # Gehen durch alle Zeilen

        for j in range(0, s):  # Gehen durch alle Spalten
            if maze[i][j]:
                stddraw.square(j / s + half_sq, i / s + half_sq, half_sq) # Wenn es eine Wand gibt, zeichnen ein Quadrat

            else:
                if points[i][j]:  # Wenn es einen Punkt in diesem Feld gibt
                    stddraw.filledCircle(j / s + half_sq, i / s + half_sq, half_sq * 0.15)  # Zeichnen die Punkte
                else:
                    stddraw.setPenColor(stddraw.ORANGE)  # Pacman-Farbe
                    stddraw.filledCircle(x / s + half_sq, y / s + half_sq, half_sq * 0.9)  # Zeichne einen Pacman
                    stddraw.setPenColor(stddraw.BLACK)  # Farbe des Rests


def draw_power_points(power_points, s, half_sq):
    for i in range(0, len(power_points)):  # Gehen durch alle Punkte des zweiten Typs
        stddraw.setPenColor(stddraw.RED)  # Die Farbe des Punktes des zweiten Typs
        stddraw.filledCircle(power_points[i][0] / s + half_sq,  # Zeichnen die Punkte des zweiten Typs
                             power_points[i][1] / s + half_sq, half_sq * 0.4)
        stddraw.setPenColor(stddraw.BLACK)  # Farbe des Rests


def show_maze(maze, n):
    stddraw.setCanvasSize(CANVAS_SIZE, CANVAS_SIZE)  # Leinwandgrößen

    s = len(maze)
    half_sq = (1 / s) / 2  # Formel für ein halbes Quadrat

    x = 1  # Die Koordinaten des Auftretens von Pacman
    y = 1

    enemies_coordinates, enemies_directions = create_enemies(s, n)  # Listen mit Koordinaten und Richtungen von Feinden

    points = create_points(s, maze)  # Liste der Punkte

    power_points = create_power_points(enemies_coordinates, s)  # Liste mit Punkten des zweiten Typs

    power_mode = False  # Unverwundbarkeit Mod
    power_mode_start_time = None  # Dauer der Unverwundbarkeit

    end_of_the_game = False  # Das Spiel beenden
    the_game_is_lost = False  # Verlust

    up = False  # Aufwärtsbewegung
    down = False  # Abwärtsbewegung
    left = False  # Bewegung nach links
    right = False  # Bewegung nach rechts

    while True:
        stddraw.clear()  # Löscht den alten und gibt nach dem Verschieben von Pacman einen neuen Frame aus

        points[y][x] = False  # Der Punkt wurde gegessen

        for i in range(0, len(power_points)):  # Gehen durch alle Punkte des zweiten Typs
            # Wenn auf einen Punkt des zweiten Typs treten
            if x == power_points[i][0] and y == power_points[i][1]:
                power_points[i] = [-1, -1]  # Übertragen eines Punktes des zweiten Typs außerhalb des Feldes
                power_mode = True  # Aktivierung des Unverwundbarkeitsmodes
                power_mode_start_time = time.time()  # Gibt die aktuelle Uhrzeit seit dem Start zurück

        if power_mode:  # Wenn der Unverwundbarkeitsmod funktioniert
            if time.time() - power_mode_start_time > 5:  # Wenn die Verweildauer in Mode > 5 Sekunden ist
                power_mode = False  # Der Mod schaltet sich aus

        for i in range(0, s):  # Gehen durch alle Zeilen

            for j in range(0, s):  # Gehen durch alle Spalten
                if points[i][j]:
                    end_of_the_game = False  # Wenn es mindestens einen Punkt gibt

        for i in range(0, len(enemies_coordinates)):
            # Bedingung für die Übereinstimmung von Feindkoordinaten mit Pacmankoordinaten
            if enemies_coordinates[i][0] == x and enemies_coordinates[i][1] == y:
                if power_mode:  # Wenn ein Punkt des zweiten Typs nicht gültig ist
                    # enemies_coordinates[i] = [25, 25]
                    enemies_directions[i] = 'dead'
                else:
                    if not enemies_directions[i] == 'dead':
                        end_of_the_game = True  # Das Spiel endet
                        the_game_is_lost = True  # Verlust

        if end_of_the_game or the_game_is_lost:  # Änderungen nach Beendigung des Spiels
            # Wenn das Spiel verloren ist
            if the_game_is_lost:
                lose_the_game()
            # Wenn das Spiel gewonnen wird
            else:
                win_the_game()
            exit()  # Beendung des Programms

        end_of_the_game = True  # Spielende

        draw_points_and_pacman(s, half_sq, maze, points, x, y)

        draw_power_points(power_points, s, half_sq)

        for enemy in range(0, len(enemies_coordinates)):  # Gehen durch jeden der Feinde
            if power_mode:  # Wenn ein Punkt des zweiten Typs gültig ist
                stddraw.setPenColor(stddraw.GRAY)  # Änderung der Farbe der Feinde

            if not enemies_directions[enemy] == 'dead':
                stddraw.filledCircle(enemies_coordinates[enemy][0] / s + half_sq,
                                     enemies_coordinates[enemy][1] / s + half_sq, half_sq * 0.9)
            stddraw.setPenColor(stddraw.BLACK)  # Farbe des Rests

            # Änderung der Richtung des Feindes
            if enemies_directions[enemy] == 'up':  # Wenn nach oben gehen
                enemies_coordinates[enemy][1] += 1  # Änderung der y-Koordinate um +1
            if enemies_directions[enemy] == 'down':  # Wenn nach unten gehen
                enemies_coordinates[enemy][1] -= 1  # Änderung der y-Koordinate um -1
            if enemies_directions[enemy] == 'left':  # Wenn nach links gehen
                enemies_coordinates[enemy][0] -= 1  # Änderung der x-Koordinate um -1
            if enemies_directions[enemy] == 'right':  # Wenn nach rechts gehen
                enemies_coordinates[enemy][0] += 1  # Änderung der x-Koordinate um +1
            # Berechnen die Richtung des Feindes im nächsten Zug
            if not enemies_directions[enemy] == 'dead':
                enemies_directions[enemy] = choose_direction_for_enemy(maze, enemies_coordinates[enemy][0],
                                                                   enemies_coordinates[enemy][1],
                                                                   enemies_directions[enemy])



            # Bedingung für die Übereinstimmung von Feindkoordinaten mit Pacmankoordinaten
            if enemies_coordinates[enemy][0] == x and enemies_coordinates[enemy][1] == y:
                if not power_mode and not enemies_directions[enemy] == 'dead':  # Wenn ein Punkt des zweiten Typs nicht gültig ist
                    the_game_is_lost = True  # Das Spiel endet

        if stddraw.hasNextKeyTyped():  # Wenn eine Taste gedrückt wird
            key = stddraw.nextKeyTyped()
            # Movement up
            if key == 'w' or key == 'ц':
                up = True
                down = False
                left = False
                right = False
            # Movement down
            if key == 's' or key == 'ы':
                up = False
                down = True
                left = False
                right = False
            # Movement to the left
            if key == 'a' or key == 'ф':
                up = False
                down = False
                left = True
                right = False
            # Movement to the right
            if key == 'd' or key == 'в':
                up = False
                down = False
                left = False
                right = True

        if up:  # Wenn 'w' gedrückt wird
            if not maze[y + 1][x]:  # Freier Weg
                y += 1  # Gehen nach oben
            else:  # Hindernis
                up = False  # Anhaltung der Bewegung

        elif down:  # Wenn 's' gedrückt wird
            if not maze[y - 1][x]:  # Freier Weg
                y -= 1  # Gehen nach unten
            else:  # Hindernis
                down = False  # Anhaltung der Bewegung

        elif left:  # Wenn 'a' gedrückt wird
            if not maze[y][x - 1]:  # Freier Weg
                x -= 1  # Gehen nach links
            else:  # Hindernis
                left = False  # Anhaltung der Bewegung

        elif right:  # Wenn 'd' gedrückt wird
            if not maze[y][x + 1]:  # Freier Weg
                x += 1  # Gehen nach rechts
            else:  # Hindernis
                right = False  # Anhaltung der Bewegung

        stddraw.show(100.0)  # Ausgabegeschwindigkeit (ms/Frame)
