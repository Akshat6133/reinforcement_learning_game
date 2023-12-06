import pygame
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from os import getcwd
# import json
from player import Player
from  gameData.config import *
from gameData.gameData import *
pwdir = getcwd()
pygame.init()

##Game Over Flag 
game_over = False 

def draw_reward():
    pygame.draw.circle(screen, (255,0,0), (100,700), 20 )
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Among Us")


# data collection
timesByimposter = []
timesbyplayer = []
time_taken_list = []
count_win = 0 
wins = []
winrate = []
lossrate = []
ep_rewards_p = []
ep_rewards_i = []


# def gamefxn():
for i in range(1,episodes+1):

    time_init = time.time() #start timestamping
    
    print(i)
    
    player_image_path = f'{pwdir}/Media//Graphics/white.png'
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
            player.image = pygame.transform.scale(pygame.image.load(f'{pwdir}/Media//Graphics/gone.png'), (40,40))
        else:
            if player_action == 0 and player.x - PLAYER_SPEED > 0:
                player.x -= PLAYER_SPEED
                player.image = walkloopleft2[frame]
                right = False
            elif player_action == 1 and player.x + PLAYER_SPEED < WIDTH:
                player.x += PLAYER_SPEED
                player.image = walkloopright2[frame]
                right= True
            elif player_action == 2 and player.y - PLAYER_SPEED > 0:
                player.y -= PLAYER_SPEED
                if right:
                    player.image = walkloopright2[frame]
                else:
                    player.image = walkloopleft2[frame]
                
            elif player_action == 3 and player.y + PLAYER_SPEED < HEIGHT:
                player.y += PLAYER_SPEED
                if right:
                    player.image = walkloopright2[frame]
                else:
                    player.image = walkloopleft2[frame]
        frame = (frame+1)%6
        frame_imp = (frame_imp+1)%6
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
            imposter.image = pygame.transform.scale(pygame.image.load(f'{pwdir}/Media//Graphics/gone.png'), (40,40))
        else:
            if imposter_action == 0 and imposter.x - IMPOSTER_SPEED > 0:
                imposter.x -= IMPOSTER_SPEED
                imposter.image = walkloopleft2[frame_imp]
                right_imp = False
            elif imposter_action == 1 and imposter.x + IMPOSTER_SPEED < WIDTH:
                imposter.x += IMPOSTER_SPEED
                imposter.image = walkloopright2[frame_imp]
                right_imp= True
            elif imposter_action == 2 and imposter.y - IMPOSTER_SPEED > 0:
                imposter.y -= IMPOSTER_SPEED
                if right_imp:
                    imposter.image = walkloopright2[frame_imp]
                else:
                    imposter.image = walkloopleft2[frame_imp]
            elif imposter_action == 3 and imposter.y + IMPOSTER_SPEED <HEIGHT:
                imposter.y += IMPOSTER_SPEED
                if right_imp:
                    imposter.image = walkloopright2[frame_imp]
                else:
                    imposter.image = walkloopleft2[frame_imp]
            

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


        background_image_path = "background_image.png"  # replace with the actual path
        background = pygame.image.load(background_image_path)
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        screen.blit(background, (0, 0))

        player.draw()
        imposter.draw()
        draw_reward()
        pygame.display.update()
        pygame.time.delay(5)

    time_end = time.time()
    time_taken = time_end - time_init
    time_taken_list.append(time_taken)

    # print(time_taken)
    
    ep_rewards_p.append(ep_reward['player'])
    ep_rewards_i.append(ep_reward['imposter'])


# data visualization
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

np.save('player1000.npy', Q_table)
np.save('imposter1000.npy', Q_table_imp)

plt.plot(a,winrate)

# Add labels and title
plt.xlabel('episodes')
plt.ylabel('player win rate')
plt.title('player')

# Show the plot
plt.savefig(f"{pwdir}/figures1000/player.png")
plt.show()

# Create a plot)
plt.plot(a,lossrate)

# Add labels and title
plt.xlabel('episodes')
plt.ylabel('imposter win rate')
plt.title('Imposter')

# Show the plot
plt.savefig(f"{pwdir}/figures1000/Imposter.png")
plt.show()

plt.plot(a,time_taken_list)

# Add labels and title
plt.xlabel('episodes')
plt.ylabel('time')
plt.title('time-taken')

# Show the plot
plt.savefig(f"{pwdir}/figures1000/time-taken.png")
plt.show()

plt.plot(list(range(len(ep_rewards_p))),ep_rewards_p)

# Add labels and title
plt.xlabel('episodes')
plt.ylabel('reward')
plt.title('player-reward')

# Show the plot
plt.savefig(f"{pwdir}/figures1000/player-reward.png")
plt.show()


plt.plot(list(range(len(ep_rewards_i))),ep_rewards_i)

# Add labels and title

plt.xlabel('episodes')
plt.ylabel('reward')
plt.title('imposter-reward')

# Show the plot
plt.savefig(f"{pwdir}/figures1000/imposter_reward.png")
plt.show()

