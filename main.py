from game import Game

if __name__ == '__main__':
    game = Game()
    # game.show_custom_state()
    # game.draw_board()
    # game.make_move()

    while not game.is_game_over():
        game.draw_board()
        game.make_move()

    print("Igra je gotova.")
    if game.player1_stacks > game.player2_stacks:
        print("Pobednik je igrac X.")
    else:
        print("Pobednik je igrac O.")

    # Trazenje mogucih stanja
    # game.show_custom_state()
    # game.draw_board()
    # game.find_all_moves_for_player('X')
    # game.find_all_moves()




