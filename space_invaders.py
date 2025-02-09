# space invaders!

from math import floor
import random, os
import pygame, time

os.chdir(r"C:\Users\priya\PycharmProjects\space invaders")

pygame.init()
dis_width = 900
dis_height = 700
#dis = pygame.display.set_mode((dis_width, dis_height), pygame.RESIZABLE)
dis = pygame.display.set_mode((dis_width, dis_height))

pygame.display.update()
pygame.display.set_caption("Space invaders!")

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)

info_height = 50

x_loc = dis_width // 2 - 25
y_loc = dis_height - 50
incr = dis_width // 80
score = 0
health = 3

tickspeed = 20
paused = False

laser_coords = []
laser_width = 8
shoot_interval = 1
shoot_interval_time = 0
shoot_interval_time_start = 0

shoot_time = 0
clear_time = 0
hit_time = time.time()
anim_time = time.time()

anim_frame = True
clock = pygame.time.Clock()
font_style = pygame.font.SysFont("consolas", 30)

level = 1
phase = 1
enemy_lasers = []
moving_aliens = True
move_incr_x = 0
move_incr_y = 0
move_time = 0
move_flip = 1
move_time_threshold = 1

squid_ranks = [[True, False, False, False, False], [True, False, False, False, False], [True, False, False, False, False], [True, False, False, False, False], [True, False, False, False, False], [True, False, False, False, False], [True, False, False, False, False], [True, False, False, False, False]]
squid_coords = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
squid_image = pygame.image.load("Squid.png")
squid_image = pygame.transform.scale(squid_image, (30, 60))

crab_ranks = [[False, True, True, False, False], [False, True, True, False, False], [False, True, True, False, False], [False, True, True, False, False], [False, True, True, False, False], [False, True, True, False, False], [False, True, True, False, False], [False, True, True, False, False]]
crab_coords = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
crab_image = pygame.image.load("Crab.png")
crab_image = pygame.transform.scale(crab_image, (50, 70))

octopus_ranks = [[False, False, False, True, True], [False, False, False, True, True], [False, False, False, True, True], [False, False, False, True, True], [False, False, False, True, True], [False, False, False, True, True], [False, False, False, True, True], [False, False, False, True, True]]
octopus_coords = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
octopus_image = pygame.image.load("Octopus.png")
octopus_image = pygame.transform.scale(octopus_image, (50, 70))


player_image = pygame.image.load("Laser_Cannon.png")
player_image = pygame.transform.scale(player_image, (50, 35))

def message(msg, color, x=dis_width/2-100, y=dis_height/2):
    sendMsg = font_style.render(msg, True, color)
    dis.blit(sendMsg, [x, y])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.VIDEORESIZE:
            old_width = dis_width

            dis_width = event.w
            dis_height = event.h

            y_loc = dis_height - 50
            x_loc = floor(x_loc / old_width * dis_width)
            incr = dis_width // 80
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
            if event.key == pygame.K_c:
                if time.time() - shoot_interval_time > 15:
                    shoot_interval = 0.25
                    shoot_interval_time = time.time()
                    shoot_interval_time_start = time.time()

    if paused:
        message("Paused", white)
        pygame.display.update()
        continue

    if time.time() - shoot_interval_time_start > 3:
        shoot_interval = 1

    keys = pygame.key.get_pressed() # check for repeated keys
    if keys[pygame.K_LEFT]:
        x_loc = max(x_loc - incr, -25)
    if keys[pygame.K_RIGHT]:
        x_loc = min(x_loc + incr, dis_width-25)
    if keys[pygame.K_SPACE]:
        if time.time() - shoot_time > shoot_interval and health > 0:
            laser_coords.append([x_loc+25-(laser_width/2), y_loc])
            shoot_time = time.time()
    if keys[pygame.K_EQUALS]:
        for i in squid_ranks:
            for j in i:
                j = False
        

    dis.fill(black) # background

    for k in range(len(laser_coords)): # draw lasers
        pygame.draw.rect(dis, white, [laser_coords[k][0], laser_coords[k][1], laser_width, 20])
        laser_coords[k][1] -= incr

    for k in laser_coords: # kill player lasers that are off of the screen
        if k[1] < -100:
            laser_coords.remove(k)
    
    for k in enemy_lasers: # draw enemy lasers
        pygame.draw.rect(dis, red, [k[0]+12.5, k[1], laser_width, 20])
        k[1] += incr

    for l in enemy_lasers: # kill enemy lasers that are off of the screen
        if l[1] > dis_height + 100:
            enemy_lasers.remove(l)
    
    pygame.draw.rect(dis, white, (0, 0, dis_width, 40)) # draw infobar

    if shoot_interval == 0.25:
        powerup_status = "active ({} sec)".format(3 - (time.time() - shoot_interval_time_start))
    elif time.time() - shoot_interval_time < 15:
        powerup_status = "cooldown ({} sec)".format(15 - (time.time() - shoot_interval_time))
    elif time.time() - shoot_interval_time > 15:
        powerup_status = "available"

    message(f"Score: {score}   Lives: {health}   Phase: {phase}   Rapid-fire: {powerup_status}", black, 5, 5)
    
    if health > 0:
        dis.blit(player_image, (x_loc, y_loc)) # draw laser cannon
    
    pygame.draw.line(dis, green, (0, dis_height - 60), (dis_width, dis_height - 60))

    if level == 1: # level 1
        if squid_ranks == [[False, False, False, False, False], [False, False, False, False, False], [False, False, False, False, False], [False, False, False, False, False], [False, False, False, False, False], [False, False, False, False, False], [False, False, False, False, False], [False, False, False, False, False]] and crab_ranks == [[False, False, False, False, False], [False, False, False, False, False], [False, False, False, False, False], [False, False, False, False, False], [False, False, False, False, False], [False, False, False, False, False], [False, False, False, False, False], [False, False, False, False, False]] and octopus_ranks == [[False, False, False, False, False], [False, False, False, False, False], [False, False, False, False, False], [False, False, False, False, False], [False, False, False, False, False], [False, False, False, False, False], [False, False, False, False, False], [False, False, False, False, False]]:
            message("Phase cleared!", green)
            if clear_time == 0:
                clear_time = time.time()
            if time.time() - clear_time > 2:
                health += 1
                clear_time = 0
                phase += 1 # TODO idk if i want levels
                move_incr_x = 0
                move_incr_y = 0

                squid_ranks = [[True, False, False, False, False], [True, False, False, False, False], [True, False, False, False, False], [True, False, False, False, False], [True, False, False, False, False], [True, False, False, False, False], [True, False, False, False, False], [True, False, False, False, False]]
                squid_coords = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

                crab_ranks = [[False, True, True, False, False], [False, True, True, False, False], [False, True, True, False, False], [False, True, True, False, False], [False, True, True, False, False], [False, True, True, False, False], [False, True, True, False, False], [False, True, True, False, False]]
                crab_coords = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

                octopus_ranks = [[False, False, False, True, True], [False, False, False, True, True], [False, False, False, True, True], [False, False, False, True, True], [False, False, False, True, True], [False, False, False, True, True], [False, False, False, True, True], [False, False, False, True, True]]
                octopus_coords = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

                move_time_threshold = 0.75

        coords_len = len(squid_coords)
        if squid_coords[0] and health:
            if moving_aliens and time.time()-move_time > move_time_threshold: # move aliens like in original game
                move_time = time.time()
                if squid_coords[7][0]+30 < move_flip * dis_width-35:
                    move_incr_x += 5
                elif squid_coords[0][0] > 35:
                    prev_flip = move_flip
                    move_flip = -1
                    if prev_flip != move_flip:
                        move_incr_y += 30
                        move_time_threshold = max(0.15, move_time_threshold-0.1)
                    else:
                        move_incr_x -= 5
                else:
                    move_flip = 1
                    move_incr_y += 30
                    move_time_threshold = max(0.15, move_time_threshold-0.1)

            for i in range(len(squid_coords)): # check if aliens are past line
                if squid_coords[i][1] > dis_height - 95 and squid_ranks[i%8][i//8]:
                    health = 0
            
            for i in range(len(crab_coords)): # check if aliens are past line
                if crab_coords[i][1] > dis_height - 95 and crab_ranks[i%8][i//8]:
                    health = 0
            
            for i in range(len(octopus_coords)): # check if aliens are past line
                if octopus_coords[i][1] > dis_height - 95 and octopus_ranks[i%8][i//8]:
                    health = 0
        
        squid_coords.clear()
        for i in range(coords_len): # draw squid ships
            j = i%8
            i = i//8
            
            if time.time() - anim_time > move_time_threshold:
                anim_frame = not anim_frame
                anim_time = time.time()
            
            add_coord = [100*j+35 + move_incr_x, 50*(i+1)+100 + move_incr_y]

            if squid_ranks[j][i]:
                if (j%2 == i%2) != anim_frame:
                    dis.blit(squid_image, (add_coord[0], add_coord[1]), (0, 0, 30, 30))
                else:
                    dis.blit(squid_image, (add_coord[0], add_coord[1]), (0, 30, 30, 30))
            
            squid_coords.append(add_coord)
       
        for i_, i in enumerate(squid_coords): # laser collision detection for squids
            for k in laser_coords:
                if (i[0] < k[0]+laser_width/2 < i[0]+30) and (i[1] < k[1]+laser_width/2 < i[1]+30):
                    if squid_ranks[i_%8][i_//8]:
                        squid_ranks[i_%8][i_//8] = False
                        laser_coords.remove(k)
                        score += 40

        for i in enemy_lasers: # laser collision detection for players
            if (x_loc-25 < i[0] < x_loc + 25) and (y_loc < i[1] < y_loc + 35):
                if time.time() - hit_time > 0.5:
                    health -= 1
                    hit_time = time.time()
        
        for i in range(len(squid_coords)): # create squid lasers
            if squid_ranks[i%8][i//8]:
                if random.randint(0, 500) == 19:
                    enemy_lasers.append(squid_coords[i])
        
        ####################################################

        coords_len = len(crab_coords)
        crab_coords.clear()
        for i in range(coords_len): # draw crab ships
            j = i%8
            i = i//8
            
            if time.time() - anim_time > move_time_threshold:
                anim_frame = not anim_frame
                anim_time = time.time()

            add_coord = [100*j+25 + move_incr_x, 50*(i+1)+100 + move_incr_y]

            if crab_ranks[j][i]:
                if (j%2 == 0+i%2) != anim_frame:
                    dis.blit(crab_image, (add_coord[0], add_coord[1]), (0, 0, 50, 35))
                else:
                    dis.blit(crab_image, (add_coord[0], add_coord[1]), (0, 35, 50, 35))
            
            crab_coords.append(add_coord)
        
        for i_, i in enumerate(crab_coords): # laser collision detection for crabs
            for k in laser_coords:
                if (i[0] < k[0]+laser_width/2 < i[0]+50) and (i[1] < k[1]+laser_width/2 < i[1]+30):
                    if crab_ranks[i_%8][i_//8]:
                        crab_ranks[i_%8][i_//8] = False
                        laser_coords.remove(k)
                        score += 20
        
        for i in range(len(crab_coords)): # create crab lasers
            if crab_ranks[i%8][i//8]:
                if random.randint(0, 500) == 19:
                    enemy_lasers.append(crab_coords[i])
        
        ####################################################

        coords_len = len(octopus_coords)
        octopus_coords.clear()
        for i in range(coords_len): # draw octopus ships
            j = i%8
            i = i//8
            
            if time.time() - anim_time > move_time_threshold:
                anim_frame = not anim_frame
                anim_time = time.time()

            add_coord = [100*j+25 + move_incr_x, 50*(i+1)+100 + move_incr_y]

            if octopus_ranks[j][i]:
                if (j%2 == 0+i%2) != anim_frame:
                    dis.blit(octopus_image, (add_coord[0], add_coord[1]), (0, 0, 50, 35))
                else:
                    dis.blit(octopus_image, (add_coord[0], add_coord[1]), (0, 35, 50, 35))
            
            octopus_coords.append(add_coord)
        
        for i_, i in enumerate(octopus_coords): # laser collision detection for octopus
            for k in laser_coords:
                if (i[0] < k[0]+laser_width/2 < i[0]+50) and (i[1] < k[1]+laser_width/2 < i[1]+30):
                    if octopus_ranks[i_%8][i_//8]:
                        octopus_ranks[i_%8][i_//8] = False
                        laser_coords.remove(k)
                        score += 10
        
        for i in range(len(octopus_coords)): # create octopus lasers
            if octopus_ranks[i%8][i//8]:
                if random.randint(0, 500) == 19:
                    enemy_lasers.append(octopus_coords[i])
        
        if not health:
            message("You lose!", red)

    pygame.display.update() # update display
    clock.tick(tickspeed)