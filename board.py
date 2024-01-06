from constants import SIZE, POSSIBLE_MOVES, letters, numbers


class Board:
    def __init__(self):
        self.board = []
        self.create_board()

    def create_board(self):
        for row in range(SIZE):
            self.board.append([])
            for col in range(SIZE):
                if (col + 1) % 2 == ((row + 1) % 2):
                    stack = []
                    if 0 < row < SIZE - 1 and row % 2 == 1:
                        stack.append('X')
                        self.board[row].append(stack)

                    elif SIZE - 1 > row > 0 == row % 2:
                        stack.append('O')
                        self.board[row].append(stack)
                    elif row == SIZE - 1:
                        self.board[row].append(stack)
                    elif row == 0:
                        self.board[row].append(stack)
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw_board(self, board):
        black = "."
        white = " "

        print_str = "   " + " ".join(f" {i + 1} " for i in range(SIZE))
        print(print_str)

        for i in range(SIZE):
            # row = self.board[i]
            row = board[i]
            if i % 2 == 0:
                for j in range(3):

                    if j == 1:
                        print(f' {chr(65 + i)} ', end='')
                    else:
                        print("   ", end='')

                    for k in range(SIZE // 2):
                        col = row[k * 2]
                        print_str = ''
                        if col != 0 and len(col) > 0:
                            col = ''.join(col)
                            if j == 2:
                                if len(col) > 3:
                                    print_str += col[:3]
                                else:
                                    print_str += col[:len(col)] + black * (3 - len(col))
                            elif j == 1:
                                if len(col) < 4:
                                    print_str += black * 3
                                elif 3 < len(col) < 6:
                                    print_str += col[3:len(col)] + black * (3 - (len(col) - 3))
                                else:
                                    print_str += col[3:6]
                            elif j == 0:
                                if len(col) > 6:
                                    print_str += col[6: len(col)] + black * (3 - (len(col) - 6))
                                else:
                                    print_str += black * 3
                        else:
                            print_str += black * 3
                        print_str += white * 5
                        print(print_str, end='')
                    print()
            else:
                for j in range(3):
                    if j == 1:
                        print(f' {chr(65 + (i + 1) * j - 1)} ', end='')
                    else:
                        print("   ", end='')
                    for k in range(SIZE // 2):
                        col = row[k * 2 + 1]
                        print_str = white * 4
                        if col != 0 and len(col) > 0:
                            col = ''.join(col)
                            if j == 2:
                                if len(col) > 3:
                                    print_str += col[:3]
                                else:
                                    print_str += col[:len(col)] + black * (3 - len(col))
                            elif j == 1:
                                if len(col) <= 3:
                                    print_str += black * 3
                                elif 3 < len(col) < 6:
                                    print_str += col[3:len(col)] + black * (3 - (len(col) - 3))
                                else:
                                    print_str += col[3:6]
                            elif j == 0:
                                if len(col) > 6:
                                    print_str += col[6: len(col)] + black * (3 - (len(col) - 6))
                                else:
                                    print_str += black * 3
                        else:
                            print_str += black * 3
                        print_str += white
                        print(print_str, end='')
                    print()

    def is_valid_move(self, move_input, board, player_on_turn, game):
        field, stack_pos, move = move_input
        field = field.upper()
        stack_pos = int(stack_pos)
        move = move.upper()

        if len(field) != 2 or field[0] not in letters or field[1] not in numbers:
            print("Pogresan unos polja")
            return False

        # Provera da li postoje figure na zadatom polju
        row = letters.index(field[0])
        col = numbers.index(field[1])

        if board[row][col] == 0 or (not board[row][col]):
            print("Na zadatom polju ne postoje figure")
            return False

        # Provera da li postoje figure na zadatom mestu na steku na zadatom polju
        if stack_pos < 0 or stack_pos > 7:
            print("Pogresan unos pozicije na steku")
            return False
        stack = board[row][col]
        if stack:
            if stack_pos >= len(stack):
                print("Na zadatom mestu na steku ne postoje figure na zadatom polju")
                return False

        # Provera da li je smer jedan od cetiri moguca
        if move.upper() not in POSSIBLE_MOVES:
            print("Pogresan unos poteza")
            return False
        dx, dy = POSSIBLE_MOVES[move.upper()]
        if row + dx < 0 or row + dx > 7 or col + dy < 0 or col + dy > 7:
            print("Ne moze se odigrati potez na ovom polju na tabli (van table)")
            return False

        # Provera velicine novog steka
        figures_to_move = stack[stack_pos:]
        dest_stack = board[row + dx][col + dy]
        if len(figures_to_move) + len(dest_stack) > 8:
            print("Velicina steka ne moze biti veca od 8")
            return False

        if self.check_move(board, row, col, stack_pos, move, player_on_turn):
            self.move_stack(stack, stack_pos, figures_to_move, dest_stack, game)
            return True

        return False

    def check_move(self, board, row, col, stack_pos, move, player_on_turn):
        dx, dy = POSSIBLE_MOVES[move.upper()]

        if self.check_neighbour_fields(board, row, col):
            # ima suseda
            if not board[row + dx][col + dy]:
                print("Imate susedno polje na kom postoje figure.")
                return False
            return self.check_stack_restrictions(board, row, col, stack_pos, dx, dy, player_on_turn)    # mozda da bude pre check_neighbour
        else:
            move_field = (row + dx, col + dy)
            start_node = (row, col)
            nearest_stacks = self.find_nearest_stacks(board, start_node)
            if not nearest_stacks:
                print("Nema dostupnih stekova.")
                return False

            paths = []

            for stack in nearest_stacks:
                start_node = (row, col)
                paths += self.generate_paths(start_node, stack)

            if paths:
                for path in paths:
                    if move_field in path:
                        return self.check_stack_restrictions(board, row, col, stack_pos, dx, dy, player_on_turn)

                print("Morate izabrati potez koji se najkracim putem priblizava do polja koje nije zauzeto.")
                return False
            else:
                print("Nije moguce pronaci put A* algoritmom.")
                return False

    def generate_paths(self, start_node, stack):
        paths = []
        # po dijagonali
        if start_node[0] - start_node[1] == stack[0] - stack[1] or \
                start_node[0] + start_node[1] == stack[0] + stack[1]:
            path = self.a_star_search(start_node, stack)
            paths.append(path)
        else:
            if start_node[1] < stack[1] and start_node[0] + start_node[1] < stack[0] + stack[1]:  # nadesno
                start_node = (start_node[0] + 1, start_node[1] + 1)
                path1 = self.a_star_search(start_node, stack)
                start_node = (start_node[0] - 2, start_node[1])
                path2 = self.a_star_search(start_node, stack)
                paths.append(path1)
                paths.append(path2)
            elif start_node[1] > stack[1] and start_node[0] + start_node[1] > stack[0] + stack[1]:  # nalevo
                # (dodatni uslov jer u situaciji (1,1) -> (4,0) generise poteze nalevo, umesto nadole)
                start_node = (start_node[0] + 1, start_node[1] - 1)
                path1 = self.a_star_search(start_node, stack)
                start_node = (start_node[0] - 2, start_node[1])
                path2 = self.a_star_search(start_node, stack)
                paths.append(path1)
                paths.append(path2)
            elif start_node[0] > stack[0]:  # nagore
                start_node = (start_node[0] - 1, start_node[1] + 1)
                path1 = self.a_star_search(start_node, stack)
                start_node = (start_node[0], start_node[1] - 2)
                path2 = self.a_star_search(start_node, stack)
                paths.append(path1)
                paths.append(path2)
            elif start_node[0] < stack[0]:  # nadole
                start_node = (start_node[0] + 1, start_node[1] + 1)
                path1 = self.a_star_search(start_node, stack)
                start_node = (start_node[0], start_node[1] - 2)
                path2 = self.a_star_search(start_node, stack)
                paths.append(path1)
                paths.append(path2)
        return paths

    def check_neighbour_fields(self, board, row, col):
        has_neighbour = False
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if 0 <= row + i < SIZE and 0 <= col + j < SIZE:
                    if board[row + i][col + j]:
                        has_neighbour = True

        return has_neighbour

    def a_star_search(self, start, end):
        found_end = False
        open_set = set()
        closed_set = set()
        g = {}
        prev_nodes = {}
        g[start] = 0
        prev_nodes[start] = None
        open_set.add(start)

        while len(open_set) > 0 and (not found_end):
            node = None
            for next_node in open_set:
                if node is None or g[next_node] + self.h_function(next_node, end) < g[node] + self.h_function(node,
                                                                                                              end):
                    node = next_node

            if node == end:
                found_end = True
                break

            for neighbor in self.get_neighbors(node):
                if neighbor not in open_set and neighbor not in closed_set:
                    open_set.add(neighbor)
                    prev_nodes[neighbor] = node
                    g[neighbor] = g[node] + 1
                else:
                    if g[neighbor] > g[node] + 1:
                        g[neighbor] = g[node] + 1
                        prev_nodes[neighbor] = node
                        if neighbor in closed_set:
                            closed_set.remove(neighbor)
                            open_set.add(neighbor)
            open_set.remove(node)
            closed_set.add(node)

        path = []
        if found_end:
            while prev_nodes[node] is not None:
                path.append(node)
                node = prev_nodes[node]
            path.append(node)
            path.reverse()

        return path

    def h_function(self, node1, node2):
        return self.calculate_distance(node1, node2)

    def calculate_distance(self, start, end):
        start_row, start_col = start
        end_row, end_col = end

        distance = 0
        current_row, current_col = start_row, start_col

        while current_row != end_row or current_col != end_col:
            horizontal_direction = 1 if end_col > current_col else -1
            vertical_direction = 1 if end_row > current_row else -1

            current_row += vertical_direction
            current_col += horizontal_direction

            if (current_row + current_col) % 2 == 0:
                distance += 1

        return distance

    def get_neighbors(self, node):
        neighbors = [(node[0] - 1, node[1] - 1), (node[0] - 1, node[1] + 1),
                     (node[0] + 1, node[1] - 1), (node[0] + 1, node[1] + 1)]

        return list(x for x in neighbors)

    def find_nearest_stacks(self, board, start):
        min_distance = float('inf')
        nearest_stacks = []

        for row in range(SIZE):
            for col in range(SIZE):
                stack = board[row][col]
                if stack:
                    stack_top = (row, col)
                    distance = self.calculate_distance(start, stack_top)
                    if distance != 0 and distance < min_distance:
                        min_distance = distance
                        nearest_stacks = [stack_top]
                    elif distance != 0 and distance == min_distance:
                        nearest_stacks.append(stack_top)

        return nearest_stacks

    def check_stack_restrictions(self, board, row, col, stack_pos, dx, dy, player_on_turn):
        start_stack = board[row][col]
        goal_stack = board[row + dx][col + dy]

        if player_on_turn not in start_stack:
            print("Ne postoji vasa figura u steku.")
            return False

        # index = start_stack.index(player_on_turn)
        if start_stack[stack_pos] != player_on_turn:
            print("Morate izabrati svoju figuru.")
            return False

        stack_to_move = start_stack[stack_pos:]
        if stack_pos != 0 and (len(goal_stack) == 0 or len(goal_stack) <= stack_pos):
            print("Figura mora da se pomera na visini koja je veca od trenutne visine.")
            return False

        if len(goal_stack) + len(stack_to_move) > 8:
            print("Nova visina steka ne sme biti veca od 8 figura.")
            return False

        return True

    def move_stack(self, start_stack, stack_pos, stack_to_move, goal_stack, game):
        goal_stack += stack_to_move
        del start_stack[stack_pos:]

        if len(goal_stack) == 8:
            last_figure = goal_stack[7]
            del goal_stack[:]

            if last_figure == 'X':
                game.player1_stacks += 1
            else:
                game.player2_stacks += 1
