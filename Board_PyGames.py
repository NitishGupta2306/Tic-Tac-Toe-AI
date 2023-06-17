import pygame
import random
import Tic_Tac_Toe_AI_V2 as func

from sys import exit
pygame.init()

# Making the Empty Game Board
screen = pygame.display.set_mode((300,300))
pygame.display.set_caption("Tic-Tac-Toe")

# Global Var declaration:
Curr_Player = 1

# Setting Board Markers
board_marked = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

def board_creation():
    # Adding Grid to Board
    background_color = (255,218,185)
    grid_color = (0,0,0)
    screen.fill(background_color)

    for pos in range(1,3):
        # Horizontal Line
        pygame.draw.line(screen, grid_color, start_pos = (0,pos*100), end_pos = (300,pos*100), width= 5)
        # Vertical Line
        pygame.draw.line(screen, grid_color, start_pos = (pos*100,0), end_pos = (pos*100,300),width= 5)

def draw_input():
    # Color Vals
    rgb_red = (255, 0, 0)
    rgb_blue = (0, 0, 255)

    # Starting Drawing
    x = 0
    for row in board_marked:
        y = 0
        for val in row:
            if val == 1:
                pygame.draw.line(screen, rgb_red, start_pos = (x*100 + 15, y*100 + 15), end_pos = (x*100 + 85, y*100 + 85), width = 5)
                pygame.draw.line(screen, rgb_red, start_pos = (x*100 + 15, y*100 + 85), end_pos = (x*100 + 85, y*100 + 15), width = 5)
            if val == -1:
                pygame.draw.circle(screen, rgb_blue, center = (x*100 + 50, y*100 + 50), radius = 40, width = 5)
            # Changing point in board currently checked
            y+=1
        x+=1

def draw_win_msg(Winner):
    # Setting Values
    rgb_black = (0,0,0)
    font_style = pygame.font.SysFont(None, 40)
    if (Winner == 1):
        message = "Human Wins!"
    elif (Winner == -1):
        message = "AI Wins!"
    
    to_disp = font_style.render(message, True, rgb_black)
    
    # Drawing message
    rgb_blue = (0, 0, 255)

    pygame.draw.rect(screen, rgb_blue,(50, 100,200,50))
    screen.blit(to_disp, (50, 100))

while True:
    board_creation()
    draw_input()

    for event in pygame.event.get():
        # Allowing game to close
        if(Curr_Player == 1):
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and Is_Winner == 0:
                # Getting use inputs
                position = pygame.mouse.get_pos()
                X = position[0]
                Y = position[1]
                # Converting to Board Values
                true_x = X//100
                true_y = Y//100

                if board_marked[true_x][true_y] == 0:
                    board_marked[true_x][true_y] = Curr_Player
                    Curr_Player *= -1

        elif(Curr_Player == -1):
            # Getting AI_Input
            x_AI, y_AI = func.Simulation_Best_Move(board_marked, Curr_Player)
            if board_marked[x_AI][y_AI] == 0:
                board_marked[x_AI][y_AI] = Curr_Player
                Curr_Player *= -1
        
        Is_Winner = func.game_over_test(board_marked) 
        
    if Is_Winner != 0:
        draw_win_msg(Is_Winner)

    # Updating Gameboard
    pygame.display.update()

pygame.quit()
