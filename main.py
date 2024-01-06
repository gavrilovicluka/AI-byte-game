from constants import OPPONENT, FIRST_PLAYER, FIRST_MOVE
from game import Game

if __name__ == '__main__':
    game = Game()

    game.draw_board()
    if FIRST_PLAYER == 'h':
        game.make_move()
        game.draw_board()
    elif FIRST_PLAYER == 'c':
        game.play_ai()
        game.draw_board()

    while not game.is_game_over():
        if OPPONENT == 'c':
            if FIRST_PLAYER == 'c' and game.turn != FIRST_MOVE:
                print("Racunar je odigrao potez. Sada je Vas red.")
                game.make_move()
            elif FIRST_PLAYER == 'c' and game.turn == FIRST_MOVE:
                game.play_ai()
            elif FIRST_PLAYER == 'h' and game.turn != FIRST_MOVE:
                game.play_ai()
            elif FIRST_PLAYER == 'h' and game.turn == FIRST_MOVE:
                print("Racunar je odigrao potez. Sada je Vas red.")
                game.make_move()
        else:
            game.make_move()

        print()
        game.draw_board()

    print("Igra je gotova.")
    if game.player1_stacks > game.player2_stacks:
        print("Pobednik je igrac X.")
    elif game.player1_stacks < game.player2_stacks:
        print("Pobednik je igrac O.")
    else:
        print("Igra je zavrsena nereseno.")
    print()
    game.show_result()

