#Copyright 2019, Moti Begna

import pygame
import random
from pygame.locals import *

# initialize pygame
pygame.init()

# create the screen object
# here we pass it a size of 800x600
screen = pygame.display.set_mode((800, 600))


background = pygame.Surface(screen.get_size())
background.fill((0, 0, 0))

def game_loop(new_score, highscore, lives):
    pygame.mixer.music.load('sounds/vaporwave3.wav')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.3)
    walking = []
    for i in range(1, 5):
        walking.append(pygame.image.load('cat_imgs/catwalk' + str(i) + '.png'))
    walkingL = []
    for i in range(1, 5):
        walkingL.append(pygame.image.load('cat_imgs/catwalkL' + str(i) + '.png'))
    jumping = []
    jumping.append(pygame.image.load('cat_imgs/catjump1.png'))
    jumping.append(pygame.image.load('cat_imgs/catjump2.png'))

    fire = []
    fire.append(pygame.image.load('cat_imgs/catfight1.png'))
    fire.append(pygame.image.load('cat_imgs/catfight2.png'))

    stationary = []
    stationary.append(pygame.image.load('cat_imgs/catstationary1.png'))
    stationary.append(pygame.image.load('cat_imgs/catstationary2.png'))

    stationaryL = []
    stationaryL.append(pygame.image.load('cat_imgs/catstationaryL1.png'))
    stationaryL.append(pygame.image.load('cat_imgs/catstationaryL2.png'))

    fireball1_img = pygame.image.load('fireball1.png')
    fireball2_img = pygame.image.load('fireball2.png')


    health_img = []
    health_img.append(pygame.image.load('healthfull.png'))
    health_img.append(pygame.image.load('healthempty.png'))

    jewel_img = []
    jewel_img.append(pygame.image.load('Jewel1.png'))
    jewel_img.append(pygame.image.load('Jewel2.png'))

    end_img = []
    end_img.append(pygame.image.load('end1.png'))
    end_img.append(pygame.image.load('end2.png'))

    platform_img = []
    for i in range(1, 13):
        platform_img.append(pygame.image.load('platform_imgs/Platform' + str(i) + '.png'))

    wall = pygame.image.load('wall.png')
    hole = []
    for i in range(2, 6):
        hole.append(pygame.image.load('hole' + str(i) + '.png'))
        
    ground_img = pygame.image.load('ground2.png')

    
 
    def text_objects(text, font):
        textSurface = font.render(text, True, (255, 255, 255))
        return textSurface, textSurface.get_rect()

    def pause():
        pause = True

        while pause:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pause = False
                        pygame.quit()
                        quit()
                    if event.key == K_SPACE:
                        pause = False
                        return True
            largeText = pygame.font.SysFont('bebas neue', 115)
            TextSurf, TextRect = text_objects("Paused", largeText)
            TextRect.center = ((800/2), (200))
            screen.blit(TextSurf, TextRect)

            smallText = pygame.font.SysFont('bebas neue', 50)
            TextSurf2, TextRect2 = text_objects("Press Escape to Quit", smallText)
            TextRect2.center = ((800/2), (275))
            screen.blit(TextSurf2, TextRect2)

            TextSurf3, TextRect3 = text_objects("Press Space to Resume", smallText)
            TextRect3.center = ((800/2), (325))
            screen.blit(TextSurf3, TextRect3)
            pygame.display.update()
    
   
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super(Player, self).__init__()
            self.image = walking[0].convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.left = 50
            self.rect.bottom = 533
            self.health = 2
            self.isJumping = False
            self.isFalling = False
            self.isFiring = False
            self.jumpheight = 275
            self.playjump = False
            self.walk = 0
            self.walkL = 0
            self.stationary = 0
            self.stationaryL = 0
            self.walkingRight = True
            self.walkingLeft = False
            self.isStationary = True
            self.inHole = False
            self.min_movement = 100
            self.max_movement = 200
            self.round_over = False
            
        def update(self, pressed_keys):
            if self.round_over == False:
                self.isStationary = True
                self.isFiring = False

                if pressed_keys[K_UP] and self.isJumping == False and self.isFalling == False:
                    self.isStationary = False
                    self.isJumping = True
                    self.playjump = True
                    self.isFiring = False
                if pressed_keys[K_DOWN] and self.isJumping == False and self.isFalling == False:
                    self.isStationary = False
                    self.rect.move_ip(0, 2)
                if pressed_keys[K_LEFT]:
                    self.isStationary = False
                    self.walkingLeft = True
                    self.walkingRight = False
                    self.isFiring = False
                    self.walk = 0
                    if self.walkL == 99:
                        self.walkL = 0
                    else:
                        self.walkL += 1
                    if self.rect.left > self.min_movement:
                        self.rect.move_ip(-3, 0)
                if pressed_keys[K_RIGHT]:
                    self.isStationary = False
                    self.walkingRight = True
                    self.walkingLeft = False
                    self.isFiring = False
                    self.walkL = 0
                    if self.walk == 99:
                        self.walk = 0
                    else:
                        self.walk += 1
                    if self.rect.left < self.max_movement:
                        self.rect.move_ip(2, 0)
                if pressed_keys[K_SPACE]:
                    self.isFiring = True
                    self.walk = 0
                    self.walkL = 0
                
                #walking animation
                if self.walk % 25 == 0 and self.walkingRight == True and self.isStationary == False:
                    ind = int(self.walk / 25)
                    self.image = walking[ind].convert_alpha()
                if self.walk == 1 and self.isStationary == False:
                    self.image = walking[0].convert_alpha()
                if self.walkL % 25 == 0 and self.walkingLeft == True and self.isStationary == False:
                    ind2 = int(self.walkL / 25)
                    self.image = walkingL[ind2].convert_alpha()
                if self.walkL == 1 and self.isStationary == False:
                    self.image = walkingL[0].convert_alpha()

                #Jumping mechanism
                if self.isJumping == True:
                    self.isStationary = False
                    if self.playjump == True:
                        pygame.mixer.Sound.play(jump)
                    self.playjump = False
                    if self.rect.top > self.jumpheight:
                        self.rect.move_ip(0, -3)
                        if self.walkingRight == True:
                            self.image = jumping[0].convert_alpha()
                        else:
                            selfimage = jumping[1].convert_alpha()
                    else:
                        self.isFalling = True
                        self.isJumping = False
                        self.jump = 0
                #Falling Mechanism
                if self.isFalling == True:
                    self.rect.move_ip(0, 2)
                    if self.rect.bottom == 533:
                        self.walk = 0
                        self.walkL = 0

                #stationary animation
                if self.isStationary == True and self.walkingRight == True:
                    self.stationaryL = 0
                    if self.stationary % 50 == 0:
                        ind = int(self.stationary / 50)
                        self.image = stationary[ind].convert_alpha()
                    if self.stationary == 99:
                        self.stationary = 0
                    else:
                        self.stationary += 1
                if self.isStationary == True and self.walkingLeft == True:
                    self.stationary = 0
                    if self.stationaryL % 50 == 0:
                        ind = int(self.stationaryL / 50)
                        self.image = stationaryL[ind].convert_alpha()
                    if self.stationaryL == 99:
                        self.stationaryL = 0
                    else:
                        self.stationaryL += 1

                if self.isFiring == True:
                    if self.walkingRight == True:
                        self.image = fire[0].convert_alpha()
                    if self.walkingLeft == True:
                        self.image = fire[1].convert_alpha()
                        
                # Keep player on the screen
                if self.rect.left < 0:
                    self.rect.left = 0
                elif self.rect.right > 795 and self.max_movement == 200:
                    self.rect.right = 800
                elif self.rect.bottom >= 533 and self.inHole != True:
                    self.rect.bottom = 533
                    self.isFalling = False
                    self.jumpheight = 275

                if self.inHole == True and self.rect.top >= 600:
                    self.health = -1
            else:
                self.rect.move_ip(3, 0)
                if self.rect.bottom <= 533:
                    self.rect.move_ip(0, 3)

                #walking animation
                if self.walk % 25 == 0:
                    ind = int(self.walk / 25)
                    self.image = walking[ind].convert_alpha()
                if self.walk == 1:
                    self.image = walking[0].convert_alpha()
                if self.walk == 99:
                    self.walk = 0
                else:
                    self.walk += 1

                
        class Fireball(pygame.sprite.Sprite):
            def __init__(self, player):
                super(Player.Fireball, self).__init__()
                self.image = fireball1_img.convert_alpha()
                self.rect = self.image.get_rect()
                self.rect.left = player.rect.centerx
                self.rect.bottom = player.rect.bottom - 20
            def update(self):
                self.rect.move_ip(4, 0)
                if self.rect.left > 800:
                    self.kill()
        class Fireball2(pygame.sprite.Sprite):
            def __init__(self, player):
                super(Player.Fireball2, self).__init__()
                self.image = fireball2_img.convert_alpha()
                self.rect = self.image.get_rect()
                self.rect.right = player.rect.centerx
                self.rect.bottom = player.rect.bottom - 20
            def update(self):
                self.rect.move_ip(-4, 0)
                if self.rect.right < 0:
                    self.kill()
        
    class Ground(pygame.sprite.Sprite):
        def __init__(self, player, x_pos):
            super(Ground, self).__init__()
            self.image = ground_img.convert()
            self.rect = self.image.get_rect()
            self.rect.left = x_pos
            self.rect.bottom = 600
        def update(self, pressed_keys):
            if player.round_over == False:
                if pressed_keys[K_RIGHT] and player.rect.left >= 200:
                    self.rect.move_ip(-3, 0)
                if pressed_keys[K_LEFT] and player.rect.left <= 100:
                    self.rect.move_ip(3, 0)
                
    class Hole(pygame.sprite.Sprite):
        def __init__(self, player, x_pos):
            super(Hole, self).__init__()
            self.image = hole[0].convert()
            self.rect = self.image.get_rect()
            self.rect.left = x_pos
            self.rect.bottom = 599
            self.stationary = 0
        def update(self, pressed_keys):
            if player.round_over == False:
                if pressed_keys[K_RIGHT] and player.rect.left >= 200:
                    self.rect.move_ip(-3, 0)
                if pressed_keys[K_LEFT] and player.rect.left <= 100:
                    self.rect.move_ip(3, 0)
                if self.stationary % 50 == 0:
                        ind = int(self.stationary / 50)
                        self.image = hole[ind].convert_alpha()
                if self.stationary == 199:
                    self.stationary = 0
                else:
                    self.stationary += 1
        

    class Health(pygame.sprite.Sprite):
        def __init__(self, x_pos, y_pos):
            super(Health, self).__init__()
            self.image = health_img[0].convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.left = x_pos
            self.rect.bottom = y_pos

    class Health2(pygame.sprite.Sprite):
        def __init__(self, x_pos, y_pos):
            super(Health2, self).__init__()
            self.image = health_img[0].convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.left = x_pos
            self.rect.bottom = y_pos
            self.movement_max = 25
            self.movement = 0
            self.moving_down = True
            self.moving_up = False
            self.movement_delay = 0
        def update(self, pressed_keys):
            if player.round_over == False:
                if pressed_keys[K_RIGHT] and player.rect.left >= 200:
                    self.rect.move_ip(-3, 0)
                if pressed_keys[K_LEFT] and player.rect.left <= 100:
                        self.rect.move_ip(3, 0)
                if self.moving_down == True and self.movement < self.movement_max and self.movement_delay == 7:
                    self.rect.move_ip(0, 2)
                    self.movement += 1
                    self.movement_delay = 0
                if self.moving_down == True and self.movement == self.movement_max:
                    self.movement = 0
                    self.moving_down = False
                    self.moving_up = True
                if self.moving_up == True and self.movement < self.movement_max and self.movement_delay == 7:
                    self.rect.move_ip(0, -2)
                    self.movement += 1
                    self.movement_delay = 0
                if self.moving_up == True and self.movement == self.movement_max:
                    self.movement = 0
                    self.moving_up = False
                    self.moving_down = True
                self.movement_delay += 1
                if self.rect.bottom > 600:
                    self.kill()

    class Jewel(pygame.sprite.Sprite):
        def __init__(self, x_pos, y_pos, ver):
            super(Jewel, self).__init__()
            self.image = jewel_img[ver].convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.left = x_pos
            self.rect.bottom = y_pos
            self.movement_max = 25
            self.movement = 0
            self.moving_down = True
            self.moving_up = False
            self.movement_delay = 0
            self.ver = ver
        def update(self, pressed_keys):
            if player.round_over == False:
                if pressed_keys[K_RIGHT] and player.rect.left >= 200:
                    self.rect.move_ip(-3, 0)
                if pressed_keys[K_LEFT] and player.rect.left <= 100:
                        self.rect.move_ip(3, 0)
                if self.moving_down == True and self.movement < self.movement_max and self.movement_delay == 7:
                    self.rect.move_ip(0, 2)
                    self.movement += 1
                    self.movement_delay = 0
                if self.moving_down == True and self.movement == self.movement_max:
                    self.movement = 0
                    self.moving_down = False
                    self.moving_up = True
                if self.moving_up == True and self.movement < self.movement_max and self.movement_delay == 7:
                    self.rect.move_ip(0, -2)
                    self.movement += 1
                    self.movement_delay = 0
                if self.moving_up == True and self.movement == self.movement_max:
                    self.movement = 0
                    self.moving_up = False
                    self.moving_down = True
                self.movement_delay += 1
                if self.rect.bottom > 600:
                    self.kill()
                    

    class End(pygame.sprite.Sprite):
        def __init__(self, player, x, y):
            super(End, self).__init__()
            self.image = end_img[0].convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.left = x
            self.rect.bottom = y
            self.stationary = 0


        def update(self, pressed_keys):
            if player.round_over == False:
                #movement update
                if pressed_keys[K_RIGHT] and player.rect.left >= 200:
                    self.rect.move_ip(-3, 0)
                if pressed_keys[K_LEFT] and player.rect.left <= 100:
                        self.rect.move_ip(3, 0)

            #movement animation
            if self.stationary % 50 == 0:
                ind = int(self.stationary / 50)
                self.image = end_img[ind].convert_alpha()
            if self.stationary == 99:
                self.stationary = 0
            else:
                self.stationary += 1

    class Platform(pygame.sprite.Sprite):
        def __init__(self, player, x, y, can_move, movement, movement_max):
            super(Platform, self).__init__()
            self.image = platform_img[0].convert_alpha()
            self.image.set_colorkey((0, 0, 0), RLEACCEL)
            self.rect = self.image.get_rect()
            self.rect.left = x
            self.rect.bottom = y
            self.can_move = can_move
            self.movement = movement
            self.movement_max = movement_max
            self.moving_right = True
            self.moving_left = False
            self.has_moved_left = False
            self.has_moved_right = False
            self.movement_delay = 0

        def update(self, pressed_keys):
            if player.round_over == False:
                if pressed_keys[K_RIGHT] and player.rect.left >= 200:
                    self.rect.move_ip(-3, 0)
                if pressed_keys[K_LEFT] and player.rect.left <= 100:
                        self.rect.move_ip(3, 0)
                if self.rect.bottom > 600:
                    self.kill()

            if self.can_move == True:
                #movement animation
                self.has_moved_left = False
                self.has_moved_right = False
                
                if self.moving_left == True and self.movement < self.movement_max and self.movement_delay == 7:
                    self.has_moved_left = True
                    self.rect.move_ip(-3, 0)
                    self.movement += 1
                    self.movement_delay = 0
                if self.moving_left == True and self.movement == self.movement_max:
                    self.movement = 0
                    self.moving_left = False
                    self.moving_right = True
                if self.moving_right == True and self.movement < self.movement_max and self.movement_delay == 7:
                    self.has_moved_right = True
                    self.rect.move_ip(3, 0)
                    self.movement += 1
                    self.movement_delay = 0
                if self.moving_right == True and self.movement == self.movement_max:
                    self.movement = 0
                    self.moving_right = False
                    self.moving_left = True
                self.movement_delay += 1

    class Platform2(pygame.sprite.Sprite):
        def __init__(self, player, x, y, can_break, can_move, min_height, max_height, ver):
            super(Platform2, self).__init__()
            self.image = platform_img[ver].convert_alpha()
            self.image.set_colorkey((0, 0, 0), RLEACCEL)
            self.rect = self.image.get_rect()
            self.rect.left = x
            self.rect.bottom = y
            self.can_break = can_break
            self.can_move = can_move
            self.movement = 0
            self.moving_down = True
            self.moving_up = False
            self.min_height = min_height
            self.max_height = max_height
            self.ver = ver
            self.movement_delay = 0
            self.has_moved_left = False
            self.has_moved_right = False

        def update(self, pressed_keys):
            if player.round_over == False:
                if pressed_keys[K_RIGHT] and player.rect.left >= 200:
                    self.rect.move_ip(-3, 0)
                if pressed_keys[K_LEFT] and player.rect.left <= 100:
                        self.rect.move_ip(3, 0)
                if self.rect.bottom > 1000:
                    self.kill()

            if self.can_move == True:
                if self.ver != 6 and self.ver != 7 and self.ver != 10 and self.ver != 11:
                    #movement animation
                    if self.moving_down == True and self.rect.top + 30 < self.min_height and self.movement_delay == 7:
                        self.rect.move_ip(0, 3)
                        self.movement += 1
                        self.movement_delay = 0
                    if self.moving_down == True and self.rect.top + 30 >= self.min_height:
                        self.movement = 0
                        self.moving_down = False
                        self.moving_up = True
                    if self.moving_up == True and self.rect.top > self.max_height and self.movement_delay == 7:
                        self.rect.move_ip(0, -3)
                        self.movement += 1
                        self.movement_delay = 0
                    if self.moving_up == True and self.rect.top <= self.max_height:
                        self.movement = 0
                        self.moving_up = False
                        self.moving_down = True
                    self.movement_delay += 1
                if self.ver == 6 or self.ver == 7 or self.ver == 10 or self.ver == 11:
                    self.has_moved_left = False
                    self.has_moved_right = False
                    #movement animation
                    if self.moving_up == True and self.rect.top > self.max_height and self.movement_delay == 7:
                        if self.ver == 6 or self.ver == 10:
                            self.rect.move_ip(2, -3)
                        if self.ver == 7 or self.ver == 11:
                            self.rect.move_ip(-2, -3)
                        self.movement_delay = 0
                        self.has_moved_left = True
                    if self.moving_up == True and self.rect.top <= self.max_height:
                        self.moving_up = False
                        self.moving_down = True
                    if self.moving_down == True and self.rect.top + 30 < self.min_height and self.movement_delay == 7:
                        if self.ver == 6 or self.ver == 10:
                            self.rect.move_ip(-2, 3)
                        if self.ver == 7 or self.ver == 11:
                            self.rect.move_ip(2, 3)
                        self.movement_delay = 0
                        self.has_moved_right = True
                    if self.moving_down == True and self.rect.top + 30 >= self.min_height:
                        self.moving_down = False
                        self.moving_up = True
                    self.movement_delay += 1


    class Wall(pygame.sprite.Sprite):
        def __init__(self, player):
            super(Wall, self).__init__()
            self.image = wall.convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.right = 42
            self.rect.bottom = 533

        def update(self, pressed_keys):
            if player.round_over == False:
                if pressed_keys[K_RIGHT] and player.rect.left >= 200:
                    self.rect.move_ip(-3, 0)
                if pressed_keys[K_LEFT] and player.rect.left <= 100:
                        self.rect.move_ip(3, 0)


  
                
    #player inititalization
    player = Player()
    all_sprites = pygame.sprite.Group()

    ##enemies = pygame.sprite.Group()
   

    #fireball initialization
    fireball_count = 0
    new_fireball = []
    fireball = []
    new_fireball.append(Player.Fireball(player))
    fireball.append(pygame.sprite.Group())
    all_sprites.add(new_fireball[fireball_count])
    fireball[fireball_count].add(new_fireball[fireball_count])

    fireball_count2 = 0
    new_fireball2 = []
    fireball2 = []
    new_fireball2.append(Player.Fireball2(player))
    fireball2.append(pygame.sprite.Group())
    all_sprites.add(new_fireball2[fireball_count2])
    fireball2[fireball_count2].add(new_fireball[fireball_count2])

    #End Flag initialization
    new_end = End(player, 9500, 533)
    end = pygame.sprite.Group()
    all_sprites.add(new_end)
    end.add(new_end)


    #platfrom initializations
    platform_pos = [(900, 300, True, 149, 150), (3100, 300, False, 0, 0)]
    new_platform = []
    platform = []
    for i in range(len(platform_pos)):        
        new_platform.append(Platform(player, platform_pos[i][0], platform_pos[i][1], platform_pos[i][2], platform_pos[i][3], platform_pos[i][4]))
        platform.append(pygame.sprite.Group())
        all_sprites.add(new_platform[i])
        platform[i].add(new_platform[i])
        
    
    new_platform_length = len(new_platform)

    platform_pos2 = [(250, 707, False, True, 533, 310, 4),
                     (350, 600, False, True, 533, 310, 4),
                     (1200, 300, False, True, 500, 200, 1),
                     (1400, 400, False, True, 500, 200, 1),
                     (1600, 500, False, True, 500, 200, 1),
                     (1800, 0, False, True, 0, -200, 5),
                     (2200, 707, False, True, 600, 310, 5),
                     (2300, 400, True, False, 0, 0, 2),
                     (2500, 400, True, False, 0, 0, 2),
                     (2700, 400, True, False, 0, 0, 2),
                     (2900, 800, False, True, 600, 310, 5),
                     (3100, 800, False, True, 600, 310, 5),
                     (3300, 800, False, True, 600, 310, 5),
                     (3500, 800, False, True, 600, 310, 5),
                     (3600, 300, False, True, 500, 200, 1),
                     (4000, 300, False, True, 500, 150, 6),
                     (4190, 300, False, True, 500, 150, 7),
                     (4640, 300, False, True, 500, 150, 6),
                     (4830, 300, False, True, 500, 150, 7),
                     (5430, 300, False, False, 0, 0, 1),
                     (5500, 433, False, False, 0, 0, 4),
                     (5500, 400, False, False, 0, 0, 4),
                     (5500, 50, False, False, 0, 0, 4),
                     (5570, 300, False, False, 0, 0, 1),
                     (5640, 300, False, False, 0, 0, 1),
                     (5750, 533, False, False, 0, 0, 8),
                     (5900, 0, False, True, 0, -300, 5),
                     (6190, 300, False, False, 0, 0, 1),
                     (6260, 300, False, False, 0, 0, 1),
                     (6330, 300, False, False, 0, 0, 1),
                     (6400, 433, False, False, 0, 0, 4),
                     (6400, 300, False, False, 0, 0, 4),
                     (6400, 200, False, False, 0, 0, 4),
                     (6470, 400, False, False, 0, 0, 1),
                     (6600, 533, False, False, 0, 0, 1),
                     (6670, 533, False, False, 0, 0, 4),
                     (6670, 400, False, False, 0, 0, 4),
                     (6740, 239, False, False, 0, 0, 9),
                     (7010, 429, False, False, 0, 0, 9),
                     (6850, 0, False, True, -40, -200, 5),
                     (6970, 239, False, False, 0, 0, 9),
                     (7240, 429, False, False, 0, 0, 9),
                     (7080, -100, False, True, -40, -200, 5),
                     (7200, 239, False, False, 0, 0, 9),
                     (7470, 429, False, False, 0, 0, 9),
                     (7310, -200, False, True, -40, -200, 5),
                     (7430, 239, False, False, 0, 0, 9),
                     (7540, -300, False, True, -40, -200, 5),
                     (7530, 429, False, False, 0, 0, 9),
                     (7762, 429, False, False, 0, 0, 4),
                     (7762, 229, False, False, 0, 0, 4),
                     (7080, 500, False, True, 600, 429, 5),
                     (7310, 600, False, True, 600, 429, 5),
                     (7540, 700, False, True, 600, 429, 5),
                     (8100, 400, False, True, 500, 250, 10),
                     (8200, 499, False, True, 500, 250, 11),
                     (8500, 400, False, True, 500, 250, 10),
                     (8600, 499, False, True, 500, 250, 11),
                     (8900, 400, False, True, 500, 250, 10),
                     (9000, 499, False, True, 500, 250, 11),
                     (8300, 707, False, True, 533, 310, 4),
                     (8700, 707, False, True, 533, 310, 4)]
    
    new_platform2 = []
    platform2 = []
    for i in range(len(platform_pos2)):
        new_platform2.append(Platform2(player, platform_pos2[i][0], platform_pos2[i][1], platform_pos2[i][2], platform_pos2[i][3], platform_pos2[i][4], platform_pos2[i][5], platform_pos2[i][6]))
        platform2.append(pygame.sprite.Group())
        all_sprites.add(new_platform2[i])
        platform2[i].add(new_platform2[i])
        
    new_platform_length2 = len(new_platform2)

    #initial wall
    new_wall = Wall(player)
    wall = pygame.sprite.Group()
    all_sprites.add(new_wall)
    wall.add(new_wall)

    #Ground initialization
    x_pos = -100
    new_ground = []
    for i in range(14):
        new_ground.append(Ground(player, x_pos))
        all_sprites.add(new_ground[i])
        x_pos += 800
    new_ground_length = len(new_ground)

    #Hole initialization
    hole_pos = [500, 784, 1065, 1340, 1570, 1800, 4000, 4280, 4560, 4840]
    new_hole = []
    holes = []
    for i in range(len(hole_pos)):
        new_hole.append(Hole(player, hole_pos[i]))
        holes.append(pygame.sprite.Group())
        all_sprites.add(new_hole[i])
        holes[i].add(new_hole[i])

    new_hole_length = len(new_hole)
    
    #Ground Health initialization

    new_health2 = []
    health2 = []
    new_health2.append(Health2(5440, 185))
    health2.append(pygame.sprite.Group())
    all_sprites.add(new_health2[0])
    health2[0].add(new_health2[0])

    #Jewel Initialization
    new_jewel = []
    jewel = []
    new_jewel.append(Jewel(100, -1000, 0))
    jewel.append(pygame.sprite.Group())
    all_sprites.add(new_jewel[0])
    jewel[0].add(new_jewel[0])
    
    x_pos = 3160
    for i in range(1, 5):
        new_jewel.append(Jewel(x_pos, 185, 1))
        jewel.append(pygame.sprite.Group())
        all_sprites.add(new_jewel[i])
        jewel[i].add(new_jewel[i])
        x_pos += 50
        
    x_pos = 6230
    for i in range(5, 8):
        new_jewel.append(Jewel(x_pos, 185, 0))
        jewel.append(pygame.sprite.Group())
        all_sprites.add(new_jewel[i])
        jewel[i].add(new_jewel[i])
        x_pos += 50
        
    x_pos = 7060
    num = 0
    for i in range(8, 20):
        if num % 2 == 0:
            ver = 0
        else:
            ver = 1
        new_jewel.append(Jewel(x_pos, 307, ver))
        jewel.append(pygame.sprite.Group())
        all_sprites.add(new_jewel[i])
        jewel[i].add(new_jewel[i])
        x_pos += 50
        num += 1

    y_pos = 200
    for i in range(20, 23):
        new_jewel.append(Jewel(8325, y_pos, 0))
        jewel.append(pygame.sprite.Group())
        all_sprites.add(new_jewel[i])
        jewel[i].add(new_jewel[i])
        y_pos -= 50

    y_pos = 200
    for i in range(23, 26):
        new_jewel.append(Jewel(8725, y_pos, 0))
        jewel.append(pygame.sprite.Group())
        all_sprites.add(new_jewel[i])
        jewel[i].add(new_jewel[i])
        y_pos -= 50
        
    #adding player last to be infront of objects, except top health
    all_sprites.add(player)

    #top health initialization
    x_pos = 50
    new_health = []
    for i in range(3):
        new_health.append(Health(x_pos, 50))
        all_sprites.add(new_health[i])
        x_pos += 50
    new_health_length = len(new_health)

    running = True

    fireblast = pygame.mixer.Sound('sounds/blast.wav')
    jump = pygame.mixer.Sound('sounds/jump.wav')
    playerhit = pygame.mixer.Sound('sounds/spike.wav')
    up_1 = pygame.mixer.Sound('sounds/1-up.wav')
    jewel_pick = pygame.mixer.Sound('sounds/jewel.wav')
    brick_break = pygame.mixer.Sound('sounds/brick_break.wav')
    burn = pygame.mixer.Sound('sounds/playerhit.wav')
    fireball_delay = 150
    fireball2_delay = 150
    score = new_score
    new_lives = lives
    running = True
    condition = "Death"

    #Player/Platform Collision Handling
    def Player_Platform(player, new_platfrom, pressed_keys, i):

        #Payer hits bottom of platform
        if player.rect.top <= new_platform[i].rect.bottom and player.rect.bottom > new_platform[i].rect.bottom:
            player.isJumping = False
            player.isFalling = True

        #Player hits top of platfrom
        if player.rect.bottom - 2 <= new_platform[i].rect.top and player.rect.right > new_platform[i].rect.left and player.rect.left < new_platform[i].rect.right:
            if pressed_keys[K_UP]:
                player.isJumping = True
                player.playjump = True
                player.isFalling = False
            player.rect.bottom = new_platform[i].rect.top
            player.jumpheight = new_platform[i].rect.bottom - 350
            if new_platform[i].has_moved_left == True:
                player.rect.move_ip(-3, 0)
            if new_platform[i].has_moved_right == True:
                player.rect.move_ip(3, 0)

        #Player hits left of platform
        if player.rect.right >= new_platform[i].rect.left and player.rect.left + 40 < new_platform[i].rect.left and player.rect.bottom > new_platfrom[i].rect.top:
            player.rect.right = new_platform[i].rect.left

        #Player hits right of platform
        if player.rect.left <= new_platform[i].rect.right and player.rect.right - 40 > new_platform[i].rect.right and player.rect.bottom > new_platfrom[i].rect.top:
            player.rect.left = new_platform[i].rect.right

    
    #Player/Platform2 Collision Handling
    def Player_Platform2(player, new_platfrom2, pressed_keys, i):
        broken = False

        #Payer hits bottom of platform
        if player.rect.top <= new_platform2[i].rect.bottom and player.rect.bottom > new_platform2[i].rect.bottom and player.rect.right - 5 > new_platform2[i].rect.left and player.rect.left + 5 < new_platform2[i].rect.right:
            player.isJumping = False
            player.isFalling = True
            if new_platform2[i].can_break == True:
                broken = True
                pygame.mixer.Sound.play(brick_break)
                
                jewel_chance = random.randint(0, 3)
                jewel_type = random.randint(0, 3)

                if jewel_chance == 0:
                    if jewel_type == 0:
                        jewel_ver = 1
                    else:
                        jewel_ver = 0
                    new_jewel.append(Jewel(new_platform2[i].rect.centerx - 20, new_platform2[i].rect.bottom - 50, jewel_ver))
                    jewel.append(pygame.sprite.Group())
                    ind = len(new_jewel) - 1
                    all_sprites.add(new_jewel[ind])
                    jewel[ind].add(new_jewel[ind])

                new_platform2[i].rect.bottom += 1000
                player.rect.top = new_platform2[i].rect.bottom - 990


        #Player hits top of platfrom
        if player.rect.bottom - 5 <= new_platform2[i].rect.top and player.rect.right + 10 > new_platform2[i].rect.left and broken == False:
            can_Jump = True
            if pressed_keys[K_UP]:
                player.isJumping = True
                player.playjump = True
                player.isFalling = False
            player.rect.bottom = new_platform2[i].rect.top
            player.jumpheight = new_platform2[i].rect.top - 300
            
            #Move player when platform moves
            if new_platform2[i].ver == 6:
                if new_platform2[i].has_moved_left == True:
                    player.rect.move_ip(2, 0)
                if new_platform2[i].moving_down == True and new_platform2[i].movement_delay == 7:
                    player.rect.move_ip(-2, 0)
                    
            if new_platform2[i].ver == 7:
                if new_platform2[i].has_moved_left == True:
                    player.rect.move_ip(-2, 0)
                if new_platform2[i].moving_down == True and new_platform2[i].movement_delay == 7:
                    player.rect.move_ip(2, 0)

            #Jumpad for ver == 8:
            if new_platform2[i].ver == 8:
                player.isJumping = True
                player.playjump = True
                player.isFalling = False
                player.jumpheight = new_platform2[i].rect.top - 400
                

        #Player hits left of platform
        if player.rect.right >= new_platform2[i].rect.left and player.rect.left + 40 < new_platform2[i].rect.left and player.rect.bottom > new_platfrom2[i].rect.top and broken == False:
            player.rect.right = new_platform2[i].rect.left
            player.jumpheight = new_platform2[i].rect.top + 350


        #Player hits right of platform
        if player.rect.left <= new_platform2[i].rect.right and player.rect.right - 40 > new_platform2[i].rect.right and player.rect.bottom > new_platfrom2[i].rect.top and broken == False:
            player.rect.left = new_platform2[i].rect.right
            player.jumpheight = new_platform2[i].rect.bottom + 350

    def Scoreboard(score):
        font = pygame.font.SysFont('bebas neue', 25)
        text = font.render("Score: " + str(score), True, (255, 255, 255))
        screen.blit(text, (225, 25))

    def HighScore(highscore):
        font = pygame.font.SysFont('bebas neue', 25)
        text = font.render("High Score: " + str(highscore), True, (255, 255, 255))
        screen.blit(text, (330, 25))

    def display_lives(new_lives):
        font = pygame.font.SysFont('bebas neue', 25)
        text = font.render("Lives: " + str(new_lives), True, (255, 255, 255))
        screen.blit(text, (500, 25))


    while running:
        new_fireball[0].kill()
        new_fireball2[0].kill()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.mixer.music.pause()
                    running = pause()
                    pygame.mixer.music.unpause()
                    if running == False:
                        condtion = "Quit"
                #fireball right event
                if event.key == K_SPACE and fireball_delay > 150 and player.walkingRight == True:
                    fireball_count += 1
                    new_fireball.append(Player.Fireball(player))
                    fireball.append(pygame.sprite.Group())
                    all_sprites.add(new_fireball[fireball_count])
                    fireball[fireball_count].add(new_fireball[fireball_count])
                    pygame.mixer.Sound.play(fireblast)
                    fireball_delay = 0

                #fireball left event
                if event.key == K_SPACE and fireball2_delay > 150 and player.walkingLeft == True:
                    fireball_count2 += 1
                    new_fireball2.append(Player.Fireball2(player))
                    fireball2.append(pygame.sprite.Group())
                    all_sprites.add(new_fireball2[fireball_count2])
                    fireball2[fireball_count2].add(new_fireball2[fireball_count2])
                    pygame.mixer.Sound.play(fireblast)
                    fireball2_delay = 0


        new_fireball_length = len(new_fireball)    
        new_fireball_length2 = len(new_fireball2)

        screen.blit(background, (0, 0))

        #player/platform collison
        for i in range(new_platform_length):
            if pygame.sprite.spritecollideany(player, platform[i]):
                Player_Platform(player, new_platform, pressed_keys, i)

        #player/platform2 collison
        for i in range(new_platform_length2):
            if pygame.sprite.spritecollideany(player, platform2[i]):
                if new_platform2[i].ver == 5 or new_platform2[i].ver == 10or new_platform2[i].ver == 11:
                    #Only hit if on screen
                    if new_platform2[i].rect.bottom > 0:
                        pygame.mixer.Sound.play(playerhit)
                        new_health[player.health].image = health_img[1].convert_alpha()
                        player.health -= 1
                        if player.rect.left < new_platform2[i].rect.left:
                            player.rect.right -= 50
                        if player.rect.right > new_platform2[i].rect.right:
                            player.rect.right += 50
                else:
                    Player_Platform2(player, new_platform2, pressed_keys, i)
                    

        new_jewel_length = len(new_jewel)

        #player/initial wall collision
        if pygame.sprite.spritecollideany(player, wall):
            player.rect.left = new_wall.rect.right

        #Right Fireball/platform collision
        for i in range(new_fireball_length):
            for j in range(new_platform_length):
                if pygame.sprite.spritecollideany(new_fireball[i], platform[j]):
                    new_fireball[i].kill()

        #Left Fireball/platform collision
        for i in range(new_fireball_length2):
            for j in range(new_platform_length):
                if pygame.sprite.spritecollideany(new_fireball2[i], platform[j]):
                    new_fireball2[i].kill()

        #Right Fireball/platform2 collision
        for i in range(new_fireball_length):
            for j in range(new_platform_length2):
                if pygame.sprite.spritecollideany(new_fireball[i], platform2[j]):
                    new_fireball[i].kill()

        #Left Fireball/platform2 collision
        for i in range(new_fireball_length2):
            for j in range(new_platform_length2):
                if pygame.sprite.spritecollideany(new_fireball2[i], platform2[j]):
                    new_fireball2[i].kill()

        #Fireball/initial wall collision
        for i in range(new_fireball_length2):
            if pygame.sprite.spritecollideany(new_fireball2[i], wall):
                new_fireball2[i].kill()

                                
        new_health_length2 = len(new_health2)

        
        #Groundhealth/player collision
        for i in range(new_health_length2):
            if pygame.sprite.spritecollideany(player, health2[i]) and player.health < 2:
                pygame.mixer.Sound.play(up_1)
                new_health2[i].rect.bottom = 2000
                player.health += 1
                new_health[player.health].image = health_img[0].convert_alpha()

        #Jewel/player collision
        for i in range(new_jewel_length):
            if pygame.sprite.spritecollideany(player, jewel[i]):
                pygame.mixer.Sound.play(jewel_pick)
                new_jewel[i].rect.bottom = 2000
                if new_jewel[i].ver == 0:
                    score += 200
                if new_jewel[i].ver == 1:
                    score += 300

        #Player/hole collison
        for i in range(new_hole_length):
            if pygame.sprite.spritecollideany(player, holes[i]):
                if player.rect.left >= new_hole[i].rect.left and player.rect.right < new_hole[i].rect.right:
                    if player.rect.bottom >= 535 and player.rect.bottom <= 537:
                        pygame.mixer.Sound.play(burn)
                    player.isFalling = True
                    player.inHole = True

        #Player/End Flag collision
        if pygame.sprite.spritecollideany(player, end):
            player.max_movement = 1000
            player.round_over = True
            

        

        ##Fixed Updates
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        new_end.update(pressed_keys)

        for i in range(new_platform_length):  
            platform[i].update(pressed_keys)

        for i in range(new_platform_length2):  
            platform2[i].update(pressed_keys)

        for i in range(new_ground_length):
            new_ground[i].update(pressed_keys)

        for i in range(new_hole_length):
            new_hole[i].update(pressed_keys)

        ##Dynamic Udates

        for i in range(new_fireball_length):
            new_fireball[i].update()

        for i in range(new_fireball_length2):
            new_fireball2[i].update()

        for i in range(new_health_length2):
            new_health2[i].update(pressed_keys)

        for i in range(new_jewel_length):
            new_jewel[i].update(pressed_keys)

        wall.update(pressed_keys)

        #Fireball delay incrementation
        if player.walkingRight:
            fireball_delay += 1
        if player.walkingLeft:
            fireball2_delay += 1
        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)


        #END GAME CONDITIONS
        if player.health == -1:
            new_lives -= 1
            condition = "Death"
            running = False

        if player.rect.right > 999:
            condition = "Complete"
            running = False


    ##    if isEnemy:
    ##        if pygame.sprite.spritecollideany(new_enemy, fireball):
    ##            new_enemy.kill()

        #no negative score
        if score < 0:
            score = 0
        Scoreboard(score)
        HighScore(highscore)
        display_lives(new_lives)

        pygame.display.update()
    return score, condition, new_lives

