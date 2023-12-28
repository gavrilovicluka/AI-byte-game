import copy

from board import Board
from constants import FIRST_MOVE, NUMBER_OF_FIGURES, POSSIBLE_MOVES, SIZE, OPPONENT


class Game:
    def __init__(self):
        self.board = Board()
        self.turn = FIRST_MOVE
        self.player1_stacks = 0
        self.player2_stacks = 0
        self.opponent = OPPONENT

    def draw_board(self):
        self.board.draw_board(self.board.board)
        self.show_result()

    def is_game_over(self):
        return self.is_board_empty() or self.has_majority_stack()

    def is_board_empty(self):
        for row in self.board.board:
            if isinstance(row, list):
                for element in row:
                    if isinstance(element, list):
                        # Provera za stekove
                        if any(subelement != 0 for subelement in element):
                            return False
                    else:
                        # Provera za bela polja
                        if element != 0:
                            return False
        return True

    def has_majority_stack(self):
        number_of_stacks = (NUMBER_OF_FIGURES // 8)
        return self.player1_stacks >= (number_of_stacks // 2) + 1 or self.player2_stacks >= (number_of_stacks / 2) + 1

    def show_custom_state(self):
        self.board.board = [
                                [[], 0, [], 0, [], 0, [], 0],
                                [0, [], 0, [], 0, [], 0, []],
                                [['O', 'X', 'X', 'O'], 0, [], 0, [], 0, [], 0],
                                [0, ['X', 'O', 'O', 'X'], 0, [], 0, [], 0, ['X', 'O', 'O', 'X', 'X', 'O', 'X']],
                                [[], 0, [], 0, [], 0, [], 0],
                                [0, [], 0, [], 0, [], 0, []],
                                [[], 0, [], 0, ['O', 'X', 'X'], 0, [], 0],
                                [0, [], 0, [], 0, [], 0, []]
        ]

    def show_result(self):
        print(f'X: {self.player1_stacks}\t O: {self.player2_stacks}')

    def make_move(self):
        is_valid = False

        while not is_valid:
            print(f'\nNa potezu igrac: {self.turn}')
            move_input = str.split(input("Unesite potez u obliku \"POLJE BROJ_PLOCICE POTEZ\": "))
            is_valid = self.board.is_valid_move(move_input, self.board.board, self.turn, self)

        self.change_turn()

    def change_turn(self):
        if self.turn == 'X':
            self.turn = 'O'
        else:
            self.turn = 'X'

    def find_all_moves_for_player(self, player_on_turn):
        current_board = copy.deepcopy(self.board.board)
        all_moves = []

        letters = []
        numbers = []
        for i in range(SIZE):
            letters.append(chr(65 + i))
            numbers.append(str(i + 1))
        count = 0
        for row in range(SIZE):
            for col in range(SIZE):
                if current_board[row][col] != 0 and len(current_board[row][col]) != 0:
                    print(current_board[row][col])
                    if player_on_turn in current_board[row][col]:    # Ako postoji figura igraca na potezu u steku
                        stack_positions = [index for index, element in enumerate(current_board[row][col]) if element == player_on_turn]

                        field = '' + letters[row] + numbers[col]
                        move_inputs = []

                        for pos in stack_positions:
                            for move in POSSIBLE_MOVES:
                                move_input = []
                                move_input.append(field)
                                move_input.append(pos)
                                move_input.append(move)
                                move_inputs.append(move_input)

                        for move in move_inputs:
                            # print(move)

                            is_valid = self.board.is_valid_move(move, current_board, player_on_turn, self)
                            if is_valid:
                                # board_copy = copy.deepcopy(current_board)
                                count += 1
                                # print("*********************************************************")
                                # self.board.draw_board(current_board)
                                # print("*********************************************************")
                                all_moves.append(current_board)
                                current_board = copy.deepcopy(self.board.board)
                                # self.board = current_board
                                # print(board_copy)

        print(f'Ukupno ima {count} mogucih stanja za igraca {player_on_turn}')
        return all_moves

    def find_all_moves(self):
        all_moves = []
        player_X_moves = self.find_all_moves_for_player('X')
        player_O_moves = self.find_all_moves_for_player('O')

        all_moves += player_X_moves + player_O_moves

        for move in all_moves:
            print("*********************************************************")
            self.board.draw_board(move)
            print("*********************************************************")

        print(f'Ukupno ima {len(all_moves)} mogucih stanja')
        return all_moves
