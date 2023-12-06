## Constants
import numpy as np
import pygame
from os import getcwd
pwdir = getcwd()
# grid dimensions 
WIDTH, HEIGHT = 1200, 800

frame = 0
frame_imp = 0
right = True
right_imp = True
at_reward = False

##Q-Learning Parameters
Q_table = np.zeros((WIDTH, HEIGHT, 4))  
Q_table_imp = np.zeros((WIDTH, HEIGHT, 4))
# Q-table for x, y, and actions (0: left, 1: right, 2: up, 3: down)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

##Sprite of gunner
spritesheet = pygame.image.load('Media/Graphics/white.png')

character = pygame.image.load('Media/Graphics/white.png')
character = pygame.transform.scale(character, (40,40))
standright = character

character = pygame.image.load('Media/Graphics/white.png')
character = pygame.transform.scale(character, (40,40))
blinkright = character

standloopright2 = [standright, blinkright]
standloopleft2 = [pygame.transform.flip(standright, True, False),
				  pygame.transform.flip(blinkright, True, False)]

character = pygame.image.load('Media/Graphics/wr1.png')
character = pygame.transform.scale(character, (40,40))
stepright = character

character = pygame.image.load('Media/Graphics/wr2.png')
character = pygame.transform.scale(character, (40,40))
runright1 = character

character = pygame.image.load('Media/Graphics/wr3.png')
character = pygame.transform.scale(character, (40,40))
runright2 = character

character = pygame.image.load('Media/Graphics/wr4.png')
character = pygame.transform.scale(character, (40,40))
runright3 = character

character = pygame.image.load('Media/Graphics/wr5.png')
character = pygame.transform.scale(character, (40,40))
runright4 = character


walkloopright2 = [
    standright,
	stepright,
	runright1,
	runright2,
	runright3,
	runright4
	]

walkloopleft2 = [
	pygame.transform.flip(walkloopright2[0], True, False),
	pygame.transform.flip(walkloopright2[1], True, False),
	pygame.transform.flip(walkloopright2[2], True, False),
	pygame.transform.flip(walkloopright2[3], True, False),
	pygame.transform.flip(walkloopright2[4], True, False),
    pygame.transform.flip(walkloopright2[5], True, False),
	]


