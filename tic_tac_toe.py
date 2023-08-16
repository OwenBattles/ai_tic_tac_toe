import math
import copy

board = [["", "", ""],
        ["", "", ""],
        ["", "", ""]]

def main():
    key = int(input("Do you want to play 1(st) or 2(nd): "))
    if key == 2:
        update((0, 0))
        key += 1
        print_board(board)

    while True:
        if key % 2 != 0:
            x = int(input("X: "))
            y = int(input("Y: "))
            coords = (x, y)
            update(coords)
            print_board(board)
            if end() == True:
                break
            else:
                key += 1
        else:
            update(minimax(board, 0))
            print_board(board)
            if end() == True:
                break
            else:
                key += 1

def print_board(game_state):
    for layer in game_state:
        print(layer)

def end():
    if check_for_winner(board) == "X":
        print("X wins")
        return True
    if check_for_winner(board) == "O":
        print("O wins")
        return True
    if terminal(board) == True:
        print("Tie")
        return True
    return False

def utility(game_state):
    if check_for_winner(game_state) == "X":
        return 10
    elif check_for_winner(game_state) == "O":
        return -10
    else:
        return 0

def terminal(game_state):
    for i in range(3):
        for j in range(3):
            if game_state[i][j] == "":
                return False
    return True       

def actions(game_state):
    moves = []

    for i in range(3):
        for j in range(3):
            if game_state[i][j] == "":
                moves.append((i, j))
    return moves

def check_for_winner(game_state):

    # Check rows, columns, and diagonals for a win
    win_conditions = [
        # Rows
        [game_state[0][0], game_state[0][1], game_state[0][2]],
        [game_state[1][0], game_state[1][1], game_state[1][2]],
        [game_state[2][0], game_state[2][1], game_state[2][2]],
        # Columns
        [game_state[0][0], game_state[1][0], game_state[2][0]],
        [game_state[0][1], game_state[1][1], game_state[2][1]],
        [game_state[0][2], game_state[1][2], game_state[2][2]],
        # Diagonals
        [game_state[0][0], game_state[1][1], game_state[2][2]],
        [game_state[0][2], game_state[1][1], game_state[2][0]]
    ]
    
    for i in range(8):
        if win_conditions[i][0] == "":
            pass
        elif win_conditions[i][0] == win_conditions[i][1] and win_conditions[i][1] == win_conditions[i][2] and win_conditions[i][2] == win_conditions[i][0]:
            if win_conditions[i][0] == "X":
                return "X"
            else:
                return "O"   
    
    return 0

def update_temp(game_state, action):
    temp = copy.deepcopy(game_state)
    
    for i in range(3):
        for j in range(3):
            if i == action[0] and j == action[1] and temp[i][j] == "":
                if player(temp) == "X":
                    temp[i][j] = "X"
                else:
                    temp[i][j] = "O"
    return temp

def update(action):
    for i in range(0, 3):
        for j in range(0, 3):
            if i == action[0] and j == action[1] and board[i][j] == "":
                if player(board) == "X":
                    board[i][j] = "X"
                else:
                    board[i][j] = "O"

def player(board):
    x, o = 0, 0
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == "X":
                x += 1
            if board[i][j] == "O":
                o +=1
    if o >= x:
        return "X"
    else:
        return "O"

def minimax(game_state, depth):
    if player(game_state) == "X":
        best_value = -math.inf
        best_move = None

        for a in actions(game_state):
            value = max(best_value, min_value(update_temp(game_state, a), depth + 1))
            if value > best_value:
                best_value = value
                best_move = a
        return best_move

    else:
        best_value = math.inf
        best_move = None
        
        for a in actions(game_state):
            value = min(best_value, max_value(update_temp(game_state, a), depth + 1))
            if value < best_value:
                best_value = value
                best_move = a
        return best_move

def max_value(game_state, depth):
    if check_for_winner(game_state) == "X" or check_for_winner(game_state) == "O":
        return utility(game_state)
    if terminal(game_state) == True:
        return utility(game_state)
    else:
        best_value = -math.inf
        for a in actions(game_state):
            value = max(best_value, min_value(update_temp(game_state, a), depth + 1))
            best_value = max(value, best_value)
        return best_value - depth

def min_value(game_state, depth):
    if check_for_winner(game_state) == "X" or check_for_winner(game_state) == "O":
        return utility(game_state)
    if terminal(game_state) == True:
        return utility(game_state)
    
    else:
        best_value = math.inf
        for a in actions(game_state):
            value = min(best_value, max_value(update_temp(game_state, a), depth + 1))
            best_value = min(value, best_value)
        return best_value + depth

if __name__ == "__main__":
    main()