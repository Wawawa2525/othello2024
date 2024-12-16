import math
import random

BLACK = 1
WHITE = 2

def can_place_x_y(board, stone, x, y):
    if board[y][x] != 0:
        return False

    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        found_opponent = False

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            found_opponent = True

        if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            return True

    return False

def get_valid_moves(board, stone):
    valid_moves = []
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone, x, y):
                valid_moves.append((x, y))
    return valid_moves

def make_move(board, stone, x, y):
    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    board[y][x] = stone
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        tiles_to_flip = []

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            tiles_to_flip.append((nx, ny))
            nx += dx
            ny += dy

        if 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            for fx, fy in tiles_to_flip:
                board[fy][fx] = stone

def evaluate_board(board, stone):
    score = 0
    for row in board:
        for cell in row:
            if cell == stone:
                score += 1
            elif cell == 3 - stone:
                score -= 1
    return score

def minimax(board, stone, depth, alpha, beta, maximizing_player):
    if depth == 0 or not get_valid_moves(board, stone):
        return evaluate_board(board, stone)

    if maximizing_player:
        max_eval = -math.inf
        for x, y in get_valid_moves(board, stone):
            new_board = [row[:] for row in board]
            make_move(new_board, stone, x, y)
            eval = minimax(new_board, 3 - stone, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for x, y in get_valid_moves(board, stone):
            new_board = [row[:] for row in board]
            make_move(new_board, stone, x, y)
            eval = minimax(new_board, 3 - stone, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

class PandaAI:

    def face(self):
        return "🐼"

    def place(self, board, stone):
        best_move = None
        best_value = -math.inf
        
        for x, y in get_valid_moves(board, stone):
            new_board = [row[:] for row in board]
            make_move(new_board, stone, x, y)
            move_value = minimax(new_board, 3 - stone, 3, -math.inf, math.inf, False)

            if move_value > best_value:
                best_value = move_value
                best_move = (x, y)

        return best_move if best_move else random_place(board, stone)

def random_place(board, stone):
    valid_moves = get_valid_moves(board, stone)
    return random.choice(valid_moves) if valid_moves else None
