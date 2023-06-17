import random

# Global Vars
board_size = 3
num_row = board_size
num_col = board_size

# Setting number of simulations
num_sim = 5000

# Checking if Game has been won
def game_over_test(board_marked):

    # Making a win set for comparision: Aka 3 'O' or 'X' in a row
    win_Condition_Human = [1,1,1]
    win_Condition_AI = [-1,-1,-1]

    # Checking win in rows
    for row in board_marked:
        if row == win_Condition_Human:
            return 1
        if row == win_Condition_AI:
            return -1
        
    # Checking win in cols
    curr_col = []
    for col in range(board_size):
        curr_col = [board_marked[row][col] for row in range(board_size)]

        if curr_col == win_Condition_Human:
            return 1
        if curr_col == win_Condition_AI:
            return -1

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
        diagonal_LtoR.append(board_marked[equal_coord][equal_coord]) 

        # gets Diagonal at <(0,2), (1,1), (2,0)> | The - 1 in the calculation is to avoid out of bound errors
        diagonal_RtoL.append(board_marked[equal_coord][board_size - equal_coord - 1])

    if diagonal_LtoR == win_Condition_Human or diagonal_RtoL == win_Condition_Human:
        return 1
    elif diagonal_LtoR == win_Condition_AI or diagonal_RtoL == win_Condition_AI:
        return -1
    return 0


# MONTE CARLO AI FUNCTIONS: 

def next_Player(curr_Move):
    return(curr_Move*-1)

# Board recreation for Sim:
def simulation_board_copy(board):
    sim_board = []
    for row in board:
        # copying board using append
        sim_board.append(row.copy())
    return sim_board

# Getting all possible moves on the current board
def possible_move(board, curr_Move):
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
            if board[row][col] == 0:
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

            if game_over_test(sim_board) != 0:
                break
            
            # Reducing score by 1 if the sim doesnt win
            score -= 1 
            
            # Switching player
            player = next_Player(player)

            # Giving valid moves after the simulation
            valid_Moves = possible_move(sim_board, player)
        
        first_Move = sim_move[0]
        last_Move = sim_move[-1]

        # 1 is a human player, -1 is an AI player
        if player == 1 and game_over_test(sim_board) == 1:
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
    
    x_AI, Y_AI = -1,-1

    for row in range(3):
        for col in range(3):
            if board[row][col] == final_choice[row][col]:
                continue
            else:
                x_AI = row
                Y_AI = col
                break

    return (x_AI,Y_AI)
