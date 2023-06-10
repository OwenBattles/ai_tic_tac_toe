import pygame
import math

board = [[(50, 50), (150, 50), (250, 50)],
        [(50, 150), (150, 150), (250, 150)],
        [(50, 250), (150, 250), (250, 250)]]

# Initialize py.game
pygame.init()
screen = pygame.display.set_mode((300, 300))
pygame.time.Clock()

# initialize font and placement for winner message
font = pygame.font.Font(None, 45)

pygame.display.set_caption("Tic Tac Toe")
screen.fill("white")

def main():
    running = True
    draw_board()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            x, y = pygame.mouse.get_pos()
            x, y = center(x, y)
            coords = x, y
            update(coords)

            draw(board, int(x), int(y))
            pygame.display.flip()

            winner = check_for_winner(board)
            update_screen_winner(winner)

            depth = find_depth(board)
            print(depth)

            # depth of 8 takes too long but 7 does not give the accurate best move, therefore first ai move is not accurate
            # this area is buggy, I am going to impliment alpha and beta pruning or find a more efficent solution
            if depth == 8:
                depth = 7

            move = minimax(board, depth)
            update(move)
            i, j = move
            draw(board, i ,j)

            winner = check_for_winner(board)
            update_screen_winner(winner)

            
        pygame.display.flip()
        
    pygame.quit()

def update_screen_winner(winner):
    # displays text of the winner to the board
    ready = False

    if winner == "X" or winner == "O":
        message_text = "{} Wins"
        ready = True
    
    if ready == True:
        message_surface = font.render(message_text.format(winner), True, "black")
        message_x = (300 - message_surface.get_width()) // 2
        message_y = (300 - message_surface.get_height()) // 2             
        screen.blit(message_surface, (message_x, message_y))
        pygame.display.flip()
        pygame.time.delay(2000)
        pygame.quit()

def find_depth(state):
    # finds proper depth for minimax() based on how many open squares there are
    depth = 0

    for x in range(0, 3):
        for y in range(0, 3):
            if state[x][y] == "O" or state[x][y] == "X":
                pass
            else:
                depth += 1
    return depth

def player(state):
    # determines the turn based on how many "X"s or "O"s there are on the board/game_state
    over = True
    x = 0
    o = 0
    for width in range(0, 3):
        for height in range(0, 3):
            if state[width][height] == "X":
                x += 1
            if state[width][height] == "O":
                o += 1
            else:
                over = False
    if over == False:
        if x <= o:
            return "X"
        else:
            return "O"
    else:
        return 0    

def draw_board():
    x = 100
    y = 100
    
    for z in range(0,3):
        pygame.draw.line(screen, "black", (0, y), (300, y), 2)
        pygame.draw.line(screen, "black", (x, 0), (x, 300), 2)
        x = x + 100
        y = y + 100

def draw(state, x, y):
    # draws the "O" or "X" based on whoever's turn it is
    if player(state) == "O":
        pygame.draw.line(screen, "blue", (x - 30, y - 30), (x + 30, y + 30), 5)
        pygame.draw.line(screen, "blue", (x - 30, y + 30), (x + 30, y - 30), 5)
        pygame.time.delay(150)

    else:
        pygame.draw.circle(screen, "red", (x, y), 30, 5)
        pygame.time.delay(150)

def center(x, y):
    x = x / 50
    y = y / 50
    
    # set x and y values to the middle of the square
    test_x = math.floor(x)
    test_y = math.floor(y)

    if test_x % 2 == 0:
        x = math.ceil(x) * 50
    else:
        x = math.floor(x) * 50

    if test_y % 2 == 0:
        y = math.ceil(y) * 50
    else:
        y = math.floor(y) * 50

    return x, y

def update_temp(list, a):
    # updates the temporary "game_state" used in the minimax algorithm
    game_state = [[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]]   
    for x in range(0, 3):
        for y in range(0, 3):
            game_state[x][y] = list[x][y]

    for x in range(0, 3):
        for y in range(0, 3):
            if game_state[x][y] == a:
                if player(list) == "X":
                    game_state[x][y] = "X"
                else:
                    game_state[x][y] = "O"
    return game_state

def update(coords):
    # update the board with the square that has been clicked
    for width in range(0, 3):
        for height in range(0, 3):
            if coords == board[width][height]:
                if player(board) == "X":
                    board[width][height] = "X"
                else:
                    board[width][height] = "O"

def check_for_winner(list):
    win = False
    # Loop through the 2d array board to look for 3 in a row
    for width in range(0, 3):
        
        # check for horizontal win
        if list[width][0] == list[width][1] and list[width][0] == list[width][2]:
            win = True
        
        # check for vertical win
        if list[0][width] == list[1][width] and list[0][width] == list[2][width]:
            win = True
        
    # check for diagonal win
    if (list[0][0] == list[1][1] and list[0][0] == list[2][2]) or (list[0][2] == list[1][1] and list[0][2] == list[2][0]):
        win = True

    if win == True:
        if player(list) == "X":
            return "O"
        else:
            return "X"
    else:
        return 2    


def actions(game_state):
    # makes a list of open squares and returns list with available moves
    moves = []
    for x in range(0, 3):
        for y in range(0, 3):
            if game_state[x][y] == "O" or game_state[x][y] == "X":
                pass
            else:
                moves.append(game_state[x][y])
    return moves

def minimax(game_state, depth):
    # if the game is over, return a value based on the outcome
    if check_for_winner(game_state) == "O":
        return -1
    if check_for_winner(game_state) == "X":
        return 1

    if depth == 0:
        print("tie")
        return 0

    if depth > 0:
        if player(game_state) == "X":
            best_move = None
            value = -math.inf
            # return the move that yields the highest value
            for a in actions(game_state):
                new_value = min_value(update_temp(game_state, a), depth - 1)
                if new_value > value:
                    value = new_value
                    best_move = a
                    print("Max: ", a, new_value)
                    if value == 1:
                        return best_move
            return best_move
            
        else: 
            best_move = None  
            value = math.inf
            # returns the move that yields the lowest value
            for a in actions(game_state):
                new_value = max_value(update_temp(game_state, a), depth - 1)
                print(new_value)
                if new_value < value:
                    value = new_value
                    best_move = a
                    print("Min: ", a, new_value)
                    if value == -1:
                        return best_move
            return best_move
    
    return value
    
def max_value(game_state, depth):
    # finds max value of min value from move played after it and returns the value of that move
    # this provides a scenario in which both players are playing optimally
    if check_for_winner(game_state) == "O":
        # print("O wins")
        return -1
    if check_for_winner(game_state) == "X":
        # print("X wins")
        return 1

    value = -math.inf
    if depth > 0:
        for a in actions(board):
            value = max(value, min_value(update_temp(game_state, a), depth - 1))
        return value
    else:
        return 0
    
def min_value(game_state, depth):
    # finds min value of max value from move played after it and returns the value of that move
    if check_for_winner(game_state) == "O":
        # print("O wins")
        return -1
    if check_for_winner(game_state) == "X":
        # print("X wins")
        return 1
    
    if depth > 0:
        value = math.inf
        for a in actions(board):
            value = min(value, max_value(update_temp(game_state, a), depth - 1))
        return value
    else: 
        return 0

if __name__ == "__main__":
    main()


