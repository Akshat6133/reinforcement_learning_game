import pygame
from gameData.config import *
from gameData.gameData import *

class Player:
    def __init__(self, x, y,image, Q_table):
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load(image)  , (40,40))
        self.rect = self.image.get_rect()
        self.rect.width = 40
        self.rect.height = 40
        self.Q = Q_table
        self.dead = False
    def draw(self):
        screen.blit(self.image, (self.x - self.rect.width // 2, self.y - self.rect.height // 2))
    def choose_action(self):
       
        if np.random.rand() < epsilon:
            
            return  np.random.choice([0,1,2,3])
        else:
            # Exploitation: choose the action with the highest Q-value
            return np.argmax(self.Q[self.x, self.y, :])
            
    
    def update_q_table(self, action, prize, next_x, next_y):
        # Q-learning update rule
        current_q_value = self.Q[self.x, self.y, action]
        max_next_q_value = np.max(self.Q[next_x, next_y, :])
        new_q_value = current_q_value + learning_rate * (prize + discount_factor * max_next_q_value - current_q_value)
        self.Q[self.x, self.y, action] = new_q_value
