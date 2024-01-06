import copy

from board import Board
from constants import FIRST_MOVE, NUMBER_OF_FIGURES, POSSIBLE_MOVES, SIZE, OPPONENT, letters, numbers


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
                                # [[], 0, [], 0, [], 0, [], 0],
                                # [0, [], 0, [], 0, [], 0, []],
                                # [['O', 'X', 'X', 'O'], 0, [], 0, [], 0, [], 0],
                                # [0, ['X', 'O', 'O', 'X'], 0, [], 0, [], 0, ['X', 'O', 'O', 'X', 'X', 'O', 'X']],
                                # [[], 0, [], 0, [], 0, [], 0],
                                # [0, [], 0, [], 0, [], 0, []],
                                # [[], 0, [], 0, ['O', 'X', 'X'], 0, [], 0],
                                # [0, [], 0, [], 0, [], 0, []]

                                [[], 0, [], 0, [], 0, [], 0],
                                [0, [], 0, [], 0, ['X'], 0, ['X']],
                                [[], 0, [], 0, [], 0, [], 0],
                                [0, [], 0, [], 0, [], 0, []],
                                [[], 0, [], 0, [], 0, [], 0],
                                [0, [], 0, [], 0, [], 0, []],
                                [[], 0, ['O', 'X', 'O', 'O', 'X', 'O', 'O'], 0, ['O', 'X'], 0, ['O', 'X', 'O', 'X', 'O'], 0],
                                [0, [], 0, [], 0, [], 0, []]
        ]

    def show_result(self):
        print(f'X: {self.player1_stacks}\t O: {self.player2_stacks}')

    def make_move(self):
        is_valid = False
        has_moves = True

        if has_moves:
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
        remove_stack_info = []   # Cuva informaciju da li se stek brise i koja je poslednja figura u tom steku

        count = 0
        for row in range(SIZE):
            for col in range(SIZE):
                if current_board[row][col] != 0 and len(current_board[row][col]) != 0:
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
                            # is_valid = self.board.is_valid_move(move, current_board, player_on_turn, self)
                            is_valid, remove_stack, last_figure = self.check_generated_move(move, current_board, player_on_turn)   # verzija bez komentara
                            if is_valid:
                                all_moves.append(current_board)
                                remove_stack_info.append((remove_stack, last_figure))
                                current_board = copy.deepcopy(self.board.board)

        # print(f'Ukupno ima {count} mogucih stanja za igraca {player_on_turn}')
        return all_moves, remove_stack_info

    def find_all_moves(self):
        all_moves = []
        player_X_moves = self.find_all_moves_for_player('X')
        player_O_moves = self.find_all_moves_for_player('O')

        all_moves += player_X_moves + player_O_moves

        print(f'Ukupno ima {len(all_moves)} mogucih stanja')
        return all_moves

    def check_generated_move(self, move_input, board, player_on_turn):
        field, stack_pos, move = move_input
        field = field.upper()
        stack_pos = int(stack_pos)
        move = move.upper()

        # Zbog rezultata
        remove_stack = False
        last_figure = None

        if len(field) != 2 or field[0] not in letters or field[1] not in numbers:
            # print("Pogresan unos polja")
            return False, remove_stack, last_figure

        # Provera da li postoje figure na zadatom polju
        row = letters.index(field[0])
        col = numbers.index(field[1])

        if board[row][col] == 0 or (not board[row][col]):
            # print("Na zadatom polju ne postoje figure")
            return False, remove_stack, last_figure

        # Provera da li postoje figure na zadatom mestu na steku na zadatom polju
        if stack_pos < 0 or stack_pos > 7:
            # print("Pogresan unos pozicije na steku")
            return False, remove_stack, last_figure
        stack = board[row][col]
        if stack:
            if stack_pos >= len(stack):
                # print("Na zadatom mestu na steku ne postoje figure na zadatom polju")
                return False, remove_stack, last_figure

        # Provera da li je smer jedan od cetiri moguca
        if move.upper() not in POSSIBLE_MOVES:
            # print("Pogresan unos poteza")
            return False, remove_stack, last_figure
        dx, dy = POSSIBLE_MOVES[move.upper()]
        if row + dx < 0 or row + dx > 7 or col + dy < 0 or col + dy > 7:
            # print("Ne moze se odigrati potez na ovom polju na tabli (van table)")
            return False, remove_stack, last_figure

        # Provera velicine novog steka
        figures_to_move = stack[stack_pos:]
        dest_stack = board[row + dx][col + dy]
        if len(figures_to_move) + len(dest_stack) > 8:
            # print("Velicina steka ne moze biti veca od 8")
            return False, remove_stack, last_figure

        if player_on_turn not in stack:
            # print("Ne postoji vasa figura u steku.")
            return False, remove_stack, last_figure

        # index = start_stack.index(player_on_turn)
        if stack[stack_pos] != player_on_turn:
            # print("Morate izabrati svoju figuru.")
            return False, remove_stack, last_figure

        if stack_pos != 0 and (len(dest_stack) == 0 or len(dest_stack) <= stack_pos):
            # print("Figura mora da se pomera na visini koja je veca od trenutne visine.")
            return False, remove_stack, last_figure

        if self.board.check_neighbour_fields(board, row, col):
            if not board[row + dx][col + dy]:
                # print("Imate susedno polje na kom postoje figure.")
                return False, remove_stack, last_figure

        move_field = (row + dx, col + dy)
        start_node = (row, col)
        nearest_stacks = self.board.find_nearest_stacks(board, start_node)

        paths = []
        for stack in nearest_stacks:
            start_node = (row, col)
            paths = self.board.generate_paths(start_node, stack)

        if paths:
            for path in paths:
                if move_field in path:
                    start_stack = board[row][col]
                    dest_stack += figures_to_move
                    del start_stack[stack_pos:]

                    if len(dest_stack) == 8:
                        remove_stack = True
                        last_figure = dest_stack[7]
                        del dest_stack[:]

                    return True, remove_stack, last_figure

        return False, remove_stack, last_figure

    def min_max_alpha_beta(self, state, depth, maximizing_player, alpha, beta):
        if depth == 0 or self.is_game_over():   # ako je igra gotova nema potrebe da se nastavlja evaluacija
            return self.evaluate(state), None, None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            best_move_info = None   # (True, 'X')
            moves, remove_stack_info = self.find_all_moves_for_player(self.turn)
            for move, info in zip(moves, remove_stack_info):
                evaluation, _, _ = self.min_max_alpha_beta(move, depth - 1, False, alpha, beta)
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move
                    best_move_info = info
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break  # Beta cutoff
            return max_eval, best_move, best_move_info
        else:
            min_eval = float('inf')
            best_move = None
            best_move_info = None
            moves, remove_stack_info = self.find_all_moves_for_player(self.opponent)
            for move, info in zip(moves, remove_stack_info):
                evaluation, _, _ = self.min_max_alpha_beta(move, depth - 1, True, alpha, beta)
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move
                    best_move_info = info
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_eval, best_move, best_move_info

    def evaluate(self, state):
        player1_stacks = 0
        player2_stacks = 0
        max_stack_height = 0
        safety = 0

        for row_index, row in enumerate(state):
            for col_index, element in enumerate(row):
                if isinstance(element, list) and len(element) > 0:
                    top_element = element[-1]
                    stack_height = len(element)

                    max_stack_height = max(max_stack_height, stack_height)

                    if top_element == FIRST_MOVE:
                        player1_stacks += 1
                    else:
                        player2_stacks += 1

                    if stack_height < 7:
                        for move in POSSIBLE_MOVES:
                            dx, dy = POSSIBLE_MOVES[move]
                            new_row, new_col = row_index + dx, col_index + dy
                            if 0 <= new_row < 8 and 0 <= new_col < 8:
                                neighbor_stack = self.board.board[new_row][new_col]
                                if isinstance(neighbor_stack, list) and neighbor_stack[-1] == self.turn:
                                    safety += 1

        stack_height_weight = 0.1
        safety_weight = 0.2

        evaluation = ((player1_stacks - player2_stacks)
                      + stack_height_weight * max_stack_height
                      + safety_weight * safety)
        return evaluation

    def play_ai(self, depth=3):
        _, best_move, best_move_info = self.min_max_alpha_beta(self.board.board, depth, True, float('-inf'), float('inf'))
        if best_move:
            self.board.board = best_move
            if best_move_info[0]:
                if best_move_info[1] == 'X':
                    if FIRST_MOVE == 'X':
                        self.player1_stacks += 1
                    else:
                        self.player2_stacks += 1
                else:
                    if FIRST_MOVE == 'O':
                        self.player1_stacks += 1
                    else:
                        self.player2_stacks += 1

            self.change_turn()
        else:
            input("Nema validnih poteza. Vi ste na redu. Pritisnite ENTER za prelazak na potez...")
            self.change_turn()

