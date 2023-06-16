import random

board_size = 3
# Setting empty board as a 2D array: size 3x3
num_row = board_size
num_col = board_size

# Setting number of simulations
num_sim = 5000

board = [
    ['*', '*', '*'],
    ['*', '*', '*'],
    ['*', '*', '*']
]

# ----- Human User Code Starts Here -----

#Randomly deciding first player
def first_Player():
    # Picks 0 or 1 at random
    AI_or_Human = random.randint(0,1)
   
    if(AI_or_Human):
        # X = AI MOVE
        return 'X'
    elif(not AI_or_Human):
        # O = HUMAN MOVE
        return 'O'

# Current move value set at random
first_Move = first_Player()
curr_Move = first_Move

def next_Player(curr_Move):
    if curr_Move == 'X':
        return 'O'
    elif curr_Move == 'O':
        return 'X'

# Printing the Board after any move
def board_Print(board):
    # Printing board with index points to make user inputs easier
    print("    0    1    2")
    for i in range(num_row):
        print(str(i) + " "+ str(board[i]))

# Checking if Board has any empty points left on it
def is_Board_Full(board):
    for row in range(num_row):
        for col in range(num_col):
            if board[row][col] == '*':
                # Board has atleast one empty space
                return False
    # Board is full
    return True

# Getting input when Human Player
def input_Human_Player(board, curr_Move):
    valid_Input = False

    while valid_Input == False:
        row_Human = int(input("row of next move: "))
        col_Human = int(input("col of next move: "))

        # Star implies point on board is empty
        if board[row_Human][col_Human] == '*':
            valid_Input == True
            board[row_Human][col_Human] = curr_Move
            return board

# Checking if Game has been won
def game_Over_Test(board, curr_Move):

    # Making a win set for comparision: Aka 3 'O' or 'X' in a row
    win_Condition_Human = ['O','O','O']
    win_Condition_AI = ['X','X','X']

    # Checking win in rows
    for row in board:
        if row == win_Condition_Human or row == win_Condition_AI:
            # Game over with win
            return True
        
    # Checking win in cols
    curr_col = []
    for col in range(board_size):
        curr_col = [board[row][col] for row in range(board_size)]

        if curr_col == win_Condition_Human or curr_col == win_Condition_AI:
            return True

    # Checking win in diagonals
    diagonal_LtoR = []
    diagonal_RtoL = []

    '''
    We can find these values inside of the previous for loop,
    but since the time complexity is already an O(N^2) for this function,
    doing so would have no impact on the actual time complexity of the system.
    '''
    for equal_coord in range(board_size):
        # gets Diagonal at <(0,0), (1,1), (2,2)>
        diagonal_LtoR.append(board[equal_coord][equal_coord]) 

        # gets Diagonal at <(0,2), (1,1), (2,0)> | The - 1 in the calculation is to avoid out of bound errors
        diagonal_RtoL.append(board[equal_coord][board_size - equal_coord - 1])

    if diagonal_LtoR == win_Condition_Human or diagonal_LtoR == win_Condition_AI:
        return True
    elif diagonal_RtoL == win_Condition_Human or diagonal_RtoL == win_Condition_AI:
        return True
    
    return False
        

# ----- AI SIMULATION CODE STARTS HERE -----

# Board recreation for Sim:
def simulation_board_copy(board):
    sim_board = []
    for row in board:
        # copying board using append
        sim_board.append(row.copy())
    return sim_board

# Getting all possible moves on the current board
def possible_move(board, currMove):
    move_Set = []
    '''
    If there is any empty space on the board
    we go ahead and replace it with current player
    this basically allows us to expand the tree
    by 1 iteration and add it to the list of possible
    moves.
    '''
    for row in range(num_row):
        for col in range(num_col):
            if board[row][col] == "*":
                # Making a copy of the board so we dont impact the main board
                sim_board = simulation_board_copy(board)
                sim_board[row][col] = curr_Move
                # Storing all board combinations for currently open spaces on the board
                move_Set.append(sim_board)
    
    return move_Set

# Picking the best move from Possible Moveset
def Simulation_Best_Move(board, curr_Move):
    # Lists for storing moves and the score for those moves
    results_move = [] * (num_sim)
    results_score = [0] * (num_sim)

    '''
    This for loop dictates how many test games the AI simulates.
    The more game it generates, the better the chance that it 
    find the best possible move set.
    '''

    for sim in range(num_sim):
        # Setting variables for simulation
        player = curr_Move
        sim_board = simulation_board_copy(board)
        score = 10 #Starting every move at a base score of 10

        # Making possible move set:
        valid_Moves = possible_move(sim_board, player)

        # Stores all sim moves:
        sim_move = []

        '''
        The while loop allows a full run through of a game after each move,
        it simulates the game from start to finish at each point. Currently this 
        is set to check 500 different, random games and pick the best one.
        '''

        while valid_Moves != []:
            # creating uncertainity using rand
            size_valid_moves = len(valid_Moves)
            random_Move = int(random.randint(1, size_valid_moves))
            random_Move -= 1

            # Picking random move
            sim_board = valid_Moves[random_Move]

            # Adding the random move to sim_move
            sim_move.append(sim_board)

            if game_Over_Test(sim_board, player) == True:
                break
            
            # Reducing score by 1 if the sim doesnt win
            score -= 1 
            
            # Switching player
            player = next_Player(player)

            # Giving valid moves after the simulation
            valid_Moves = possible_move(sim_board, player)
        
        first_Move = sim_move[0]
        last_Move = sim_move[-1]

        # O is a human player, X is an AI player
        if player == 'O' and game_Over_Test(sim_board, player):
            # Setting score to super low value if the human player wins
            score = -100000
        
        if first_Move in results_move:
            # Adding to the score if its in our results
            index_val = results_move.index(first_Move)
            results_score[index_val] += score
        else:
            # setting general score value if never checked before
            results_move.append(first_Move)
            index_val = results_move.index(first_Move)
            results_score[index_val] = score
    
    final_choice = results_move[0]
    best_score = 0
    '''
        We need check if this is the first input being made
        otherwise the code can run into a out of index error
        for result_score[0]
    '''
    is_First_Result = True

    for index_score in range(len(results_move)):
        if(is_First_Result or results_score[index_score] > best_score):
            best_score = score
            final_choice = results_move[index_score]
            is_First_Result = False

    return final_choice

#Main()
print("*** Starting Board: ***")
board_Print(board)
print("------------------\n")

while not is_Board_Full(board):
    # Get / Generate inputs
    if curr_Move == 'O':
        print("*** Human MOVE: ***")
        board = input_Human_Player(board, curr_Move)
    else:
        print("*** AI MOVE: ***")
        board = Simulation_Best_Move(board, curr_Move)    
    # Print board after move
    board_Print(board)
    print("------------------\n")

    # Checking win conditions
    if game_Over_Test(board, curr_Move):
        if curr_Move == 'X':
            print("GAME WON: Congrats AI")
            break
        if curr_Move == 'O':
            print("GAME WON: Congrats Human")
            break

    curr_Move = next_Player(curr_Move)

print("It was sadly a tie, Good Game!")