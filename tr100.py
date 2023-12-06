import pygame
# import random
import sys
import time
import numpy as np
from os import getcwd


episodes = 100
##Current Working Directory
presworkdir = getcwd()
# win = []
# Initialize Pygame
pygame.init()


## Constants
WIDTH, HEIGHT = 1200, 800
PLAYER_SPEED = 10
IMPOSTER_SPEED = 15

##Game Over Flag 
game_over = False

##Starting frames
frame = 0
frame_imp = 0
right = True
right_imp = True
at_reward = False

##Q-Learning Parameters
Q_table = np.zeros((WIDTH, HEIGHT, 4))  
Q_table_imp = np.zeros((WIDTH, HEIGHT, 4))
# Q-table for x, y, and actions (0: left, 1: right, 2: up, 3: down)
epsilon = 0.1
learning_rate = 0.9
discount_factor = 0.95

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


##Player Class
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

def draw_reward():
    pygame.draw.circle(screen, (255,0,0), (100,700), 20 )
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Among Us")

timesByimposter = []
timesbyplayer = []
time_taken_list = []
count_win = 0 
wins = []
winrate = []
lossrate = []
ep_rewards_p = []
ep_rewards_i = []
for i in range(1,episodes+1):
    time_init = time.time() #start timestamping
    
    print(i)
    
    player_image_path = f'{presworkdir}/Media//Graphics/white.png'
    player = Player(WIDTH//2, HEIGHT//2, player_image_path,Q_table)
    imposter = Player(1000,700, player_image_path,Q_table_imp)
    # Fonts
    font = pygame.font.Font(None, 36)

    target = player
    prev_action = 0
    prev_action_imp = 0
    start_time = time.time()
    game_over = False
    ep_reward = {'player':0,'imposter':0}
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()



        player_action = player.choose_action()
        prev_x = player.x
        prev_y = player.y
        prev_reward = player.Q[player.x, player.y, prev_action]

        if player.dead:
            player.image = pygame.transform.scale(pygame.image.load(f'{presworkdir}/Media//Graphics/gone.png'), (40,40))
        else:
            if player_action == 0 and player.x - PLAYER_SPEED > 0:
                player.x -= PLAYER_SPEED
                # player.image = walkloopleft2[frame]
                # right = False
            elif player_action == 1 and player.x + PLAYER_SPEED < WIDTH:
                player.x += PLAYER_SPEED
                # player.image = walkloopright2[frame]
                # right= True
            elif player_action == 2 and player.y - PLAYER_SPEED > 0:
                player.y -= PLAYER_SPEED
                # if right:
                #     player.image = walkloopright2[frame]
                # else:
                #     player.image = walkloopleft2[frame]
                
            elif player_action == 3 and player.y + PLAYER_SPEED < HEIGHT:
                player.y += PLAYER_SPEED
                # if right:
                #     player.image = walkloopright2[frame]
                # else:
                #     player.image = walkloopleft2[frame]
        # frame = (frame+1)%6
        # frame_imp = (frame_imp+1)%6
        distance_reward = abs(100-player.x) + abs(700-player.y)
        distance_prev_reward = abs(100 - prev_x) + abs(700 - prev_y)
        prev_action = player_action
        if distance_reward < distance_prev_reward:
            prize = prev_reward + 10
        else:
            prize = prev_reward - 20

        player.update_q_table(player_action, prize, player.x, player.y)
        if (((player.x - 100)**2)+((player.y-700)**2))**0.5 <= 20:
            imposter.dead = True
            wins.append(1)
            game_over = True
            Q_table = player.Q
            timesbyplayer.append(time.time() - start_time)
        # else:
        #      nd(0)
        imposter_action = imposter.choose_action()
        prev_x_imp = imposter.x
        prev_y_imp = imposter.y
        prev_reward_imp = imposter.Q[imposter.x, imposter.y, prev_action_imp]

        if imposter.dead:
            imposter.image = pygame.transform.scale(pygame.image.load(f'{presworkdir}/Media//Graphics/gone.png'), (40,40))
        else:
            if imposter_action == 0 and imposter.x - IMPOSTER_SPEED > 0:
                imposter.x -= IMPOSTER_SPEED
                # imposter.image = walkloopleft2[frame_imp]
                # right_imp = False
            elif imposter_action == 1 and imposter.x + IMPOSTER_SPEED < WIDTH:
                imposter.x += IMPOSTER_SPEED
                # imposter.image = walkloopright2[frame_imp]
                # right_imp= True
            elif imposter_action == 2 and imposter.y - IMPOSTER_SPEED > 0:
                imposter.y -= IMPOSTER_SPEED
                # if right_imp:
                #     imposter.image = walkloopright2[frame_imp]
                # else:
                #     imposter.image = walkloopleft2[frame_imp]
            elif imposter_action == 3 and imposter.y + IMPOSTER_SPEED <HEIGHT:
                imposter.y += IMPOSTER_SPEED
                # if right_imp:
                #     imposter.image = walkloopright2[frame_imp]
                # else:
                #     imposter.image = walkloopleft2[frame_imp]
            

        distance_reward_imp = abs(imposter.x-player.x) + abs(imposter.y-player.y)
        distance_prev_reward_imp = abs(prev_y - prev_x_imp) + abs(prev_x - prev_y_imp)
        prev_action = imposter_action
        if distance_reward_imp < distance_prev_reward_imp:
            prize_imp = prev_reward_imp + 10
        else:
            prize_imp = prev_reward_imp - 20

        imposter.update_q_table(imposter_action, prize_imp, imposter.x, imposter.y)
        if (((player.x - imposter.x)**2)+((player.y-imposter.y)**2))**0.5 <= 20:
            wins.append(0)
            player.dead = True
            game_over = True
            Q_table_imp = imposter.Q
            timesByimposter.append(time.time() - start_time)

        ep_reward['player']+=distance_reward_imp
        ep_reward['imposter']+=distance_prev_reward_imp

        #-------------------------------------------------------------------------------------------------------------------- Draw background


        # background_image_path = "background_image.png"  # replace with the actual path
        # background = pygame.image.load(background_image_path)
        # background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        # screen.blit(background, (0, 0))

        # player.draw()
        # imposter.draw()
        # draw_reward()
        pygame.display.update()
        # pygame.time.delay(5)

    time_end = time.time()
    time_taken = time_end - time_init
    time_taken_list.append(time_taken)

    # print(time_taken)
    
    ep_rewards_p.append(ep_reward['player'])
    ep_rewards_i.append(ep_reward['imposter'])


import matplotlib.pyplot as plt


# a = list(range(1,(episodes)+1))
a = list(range(1,episodes+1))
num_0 = 0
sm = 0
for i in range(1, episodes+1):
    sm += wins[i-1]
    if wins[i-1] == 0:
        num_0+=1
    winrate.append(sm/i)
    lossrate.append(num_0/i)

# print(wins)
print(winrate[-1])
print(lossrate[-1])
# Create a plot
# plt.plot(timesByimposter,a)

# # Add labels and title
# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
# plt.title('Imposter')

# # Show the plot
# plt.show()

# # Create a plot
# plt.plot(timesbyplayer,a)

# # Add labels and title
# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
# plt.title('Player')

# # Show the plot
# plt.show()

np.save('player100.npy', Q_table)
np.save('imposter100.npy', Q_table_imp)

plt.plot(a,winrate)

# Add labels and title
plt.xlabel('episodes')
plt.ylabel('player win rate')
plt.title('player')

# Show the plot
plt.savefig(f"{presworkdir}/figures100/player.png")
plt.show()

# Create a plot)
plt.plot(a,lossrate)

# Add labels and title
plt.xlabel('episodes')
plt.ylabel('imposter win rate')
plt.title('Imposter')

# Show the plot
plt.savefig(f"{presworkdir}/figures100/Imposter.png")
plt.show()

plt.plot(a,time_taken_list)

# Add labels and title
plt.xlabel('episodes')
plt.ylabel('time')
plt.title('time-taken')

# Show the plot
plt.savefig(f"{presworkdir}/figures100/time-taken.png")
plt.show()

plt.plot(list(range(len(ep_rewards_p))),ep_rewards_p)

# Add labels and title
plt.xlabel('episodes')
plt.ylabel('reward')
plt.title('player-reward')

# Show the plot
plt.savefig(f"{presworkdir}/figures100/player-reward.png")
plt.show()


plt.plot(list(range(len(ep_rewards_i))),ep_rewards_i)

# Add labels and title

plt.xlabel('episodes')
plt.ylabel('reward')
plt.title('imposter-reward')

# Show the plot
plt.savefig(f"{presworkdir}/figures100/imposter_reward.png")
plt.show()

