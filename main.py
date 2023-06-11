import pygame
from sys import exit
from random import randint

def vertical_movement(list, speed, surf):
    global game_state

    if list:
        for rect in list:
            if rect.y < -50 and surf == pocisk_surf:
                list.remove(rect)
            if surf == enemy_surf:
                if rect.y > 800:
                    game_state = 'gameover'
            rect.y += speed
            screen.blit(surf, rect)
        return list
    else:
        return []

def checkListCollision(bullets, enemies):
    global score

    for enemy_rect in enemies:
        for bullet_rect in bullets:
            if enemy_rect.colliderect(bullet_rect):
                enemies.remove(enemy_rect)
                bullets.remove(bullet_rect)
                score += 1

def checkCollision(rect, list):
    global slowboost_start_time, show_time

    for list_rect in list:
        if list_rect.colliderect(rect):
            list.remove(list_rect)
            slowboost_start_time = pygame.time.get_ticks()
            show_time = -3000


pygame.init()
screen = pygame.display.set_mode((400, 800))
pygame.display.set_caption('Space Shooter')
clock = pygame.time.Clock()

#variables
game_state = 'menu'
progress = 0
bullets = 3
enemy_speed = 5
slowboost_show = False
show_time = -3000
slowboost_start_time = -5000
score = 0

enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 2000)

slowBoost_timer = pygame.USEREVENT + 2
pygame.time.set_timer(slowBoost_timer, 4000)

#fonts
bullet_font = pygame.font.Font('font/retro_gaming.ttf', 30)
menu_font = pygame.font.Font('font/retro_gaming.ttf', 50)

title1_surf = menu_font.render("Space", False, '#ffffff')
title1_rect = title1_surf.get_rect(center = (200, 40))

title2_surf = menu_font.render("Shooter", False, '#ffffff')
title2_rect = title2_surf.get_rect(center = (200, 80))

score_surf = menu_font.render(str(score), False, '#ffffff')
score_rect = score_surf.get_rect(center = (200, 40))

bullets_left_surf = bullet_font.render(f"Bullets left: {bullets}", False, '#ffffff')
bullets_left_rect = bullets_left_surf.get_rect(center = (200, 80))

gameover_surf = menu_font.render("GAME OVER", False, '#ffffff')
gameover_rect = gameover_surf.get_rect(center = (200, 75))

pressSpace_surf = bullet_font.render("Press Space to play", False, '#ffffff')
pressSpace_rect = pressSpace_surf.get_rect(center = (200, 120))

pressEnter1_surf = bullet_font.render("Press ENTER to", False, '#ffffff')
pressEnter1_rect = pressEnter1_surf.get_rect(center = (200, 620))

pressEnter2_surf = bullet_font.render("get back to menu", False, '#ffffff')
pressEnter2_rect = pressEnter2_surf.get_rect(center = (200, 660))

#player
player_surf = pygame.image.load('graphics/player.png').convert_alpha()
player_rect = player_surf.get_rect(center = (200, 700))

move_left = False
move_right = False

#pocisk
pocisk_surf = pygame.image.load('graphics/pocisk.png').convert_alpha()
pocisk_rect_list = []

#enemy
enemy_surf = pygame.image.load('graphics/enemy.png').convert_alpha()
enemy_rect_list = []

#slow boost
slowboost_surf = pygame.image.load('graphics/slowboost.png').convert_alpha()
slowboost_rect = slowboost_surf.get_rect()

#menu elementy
player_menu_surf = pygame.transform.scale_by(player_surf, 3)
player_menu_rect = player_menu_surf.get_rect(center = (200,400))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_state == 'game':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_left = True
                    move_right = False
                if event.key == pygame.K_RIGHT:
                    move_right = True
                    move_left = False
                if event.key == pygame.K_SPACE and bullets > 0:
                    pocisk_rect_list.append(pocisk_surf.get_rect(center = player_rect.midtop))
                    bullets -= 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    move_left = False
                if event.key == pygame.K_RIGHT:
                    move_right = False
            if event.type == enemy_timer:
                enemy_rect_list.append(enemy_surf.get_rect(center = (randint(20, 380), 0)))
            if event.type == slowBoost_timer and randint(1, 2) == 1:
                slowboost_show = True
                show_time = pygame.time.get_ticks()
                slowboost_rect.center = (randint(50, 350), randint(100, 550))
        
        if game_state == 'gameover' or game_state == 'menu':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = 'game'
                    progress = 0
                    bullets = 5
                    pocisk_rect_list = []
                    enemy_rect_list = []
                    player_rect.center = (200, 700)
                    move_left = False
                    move_right = False
                if event.key == pygame.K_RETURN:
                    game_state = 'menu'
    
    screen.fill('#000000')

    if game_state == 'game':

        if move_left == True and player_rect.left > 0:
            player_rect.x -= 5
        if move_right == True and player_rect.right < 400:
            player_rect.x += 5
        
        pocisk_rect_list = vertical_movement(pocisk_rect_list, -5, pocisk_surf)
        enemy_rect_list = vertical_movement(enemy_rect_list, enemy_speed, enemy_surf)
        checkListCollision(pocisk_rect_list, enemy_rect_list)

        screen.blit(player_surf,player_rect)

        #progress bar
        if progress < 1:
            progress += 0.009
        else:
            progress = 0
            bullets += 1
        pygame.draw.rect(screen, ('#ffffff'), pygame.Rect(50, 750, 300*progress, 30))
        bullets_left_surf = bullet_font.render(f"Bullets left: {bullets}", False, '#ffffff')
        screen.blit(bullets_left_surf, bullets_left_rect)

        score_surf = menu_font.render(str(score), False, '#ffffff')
        screen.blit(score_surf, score_rect)

        if pygame.time.get_ticks() - show_time < 3000:
            screen.blit(slowboost_surf, slowboost_rect)
            checkCollision(slowboost_rect, pocisk_rect_list)
        if pygame.time.get_ticks() - slowboost_start_time < 5000:
            slowboost_show = False
            enemy_speed = 3
        else:
            enemy_speed = 5

    
    if game_state == 'gameover':
        screen.blit(gameover_surf, gameover_rect)
        screen.blit(pressSpace_surf, pressSpace_rect)
        screen.blit(pressEnter1_surf, pressEnter1_rect)
        screen.blit(pressEnter2_surf, pressEnter2_rect)
        screen.blit(player_menu_surf, player_menu_rect)
    
    if game_state == 'menu':
        screen.blit(title1_surf, title1_rect)
        screen.blit(title2_surf, title2_rect)
        screen.blit(pressSpace_surf, pressSpace_rect)
        screen.blit(player_menu_surf, player_menu_rect)

    print(score)

    pygame.display.update()
    clock.tick(60)
