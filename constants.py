SIZE = 8
NUMBER_OF_FIGURES = (SIZE ** 2 - SIZE * 2) // 2
FIRST_PLAYER = 'h'  # h - covek, c - racunar
FIRST_MOVE = 'X'    # X - crni, O - beli
OPPONENT = 'h'

POSSIBLE_MOVES = {
    'GL': (-1, -1),
    'GD': (-1, 1),
    'DL': (1, -1),
    'DD': (1, 1)
}

s = int(input("Unesite dimenziju table: "))
number_of_figures = (s ** 2 - 2 * s) // 2
if number_of_figures % 8 != 0:
    print("Broj figura na tabli mora biti deljiv sa 8!")
    print("Tabla postavljena na podrazumevanu vrednost 8x8")
elif s % 2 == 0 and 8 <= s <= 16:
    SIZE = s
    NUMBER_OF_FIGURES = number_of_figures
else:
    print("Pogresan unos dimenzija table!")
    print("Tabla postavljena na podrazumevanu vrednost 8x8")

while True:
    opponent = input("Unesite protiv koga igrate (h - covek, c - racunar): ").lower()
    if opponent not in ["h", "c"]:
        print("Pogresan unos igraca. Molimo unesite ponovo.")
    elif opponent == 'c':
        print("Igrate protiv racunara.")
        OPPONENT = opponent
        break
    else:
        print("Igrate protiv coveka")
        break

if opponent == 'c':
    first_player = input("Unesite ko igra prvi (h - covek, c - racunar): ").lower()
    if first_player not in ["h", "c"]:
        print("Pogresan unos igraca. Prvi igra covek.")
    elif first_player == 'c':
        print("Prvi igra racunar.")
        FIRST_PLAYER = first_player
    else:
        print("Prvi igra covek")


first_move = input("Unesite ko je prvi na potezu (X - crni, O - beli): ").upper()
if first_move not in ["X", "O"]:
    print("Pogresan unos prvog poteza. Prvi potez ima igrac X (crni).")
elif first_move == 'O':
    print("Prvi potez ima igrac O (beli)")
    FIRST_MOVE = first_move
else:
    print("Prvi potez ima igrac X (crni)")


