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
background.fill((135, 150, 250))
 
def game_loop(highscore, lives):
    pygame.mixer.music.load('sounds/vaporwave2.wav')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
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

    snail_img = []
    snail_img.append(pygame.image.load('snail_imgs/snail1.png'))
    snail_img.append(pygame.image.load('snail_imgs/snail2.png'))

    snail_imgR = []
    snail_imgR.append(pygame.image.load('snail_imgs/snail1R.png'))
    snail_imgR.append(pygame.image.load('snail_imgs/snail2R.png'))

    snail_img_hurt = []
    snail_img_hurt.append(pygame.image.load('snail_imgs/snail1_hurt.png'))
    snail_img_hurt.append(pygame.image.load('snail_imgs/snail2_hurt.png'))

    snail_imgR_hurt = []
    snail_imgR_hurt.append(pygame.image.load('snail_imgs/snail1R_hurt.png'))
    snail_imgR_hurt.append(pygame.image.load('snail_imgs/snail2R_hurt.png'))

    health_img = []
    health_img.append(pygame.image.load('healthfull.png'))
    health_img.append(pygame.image.load('healthempty.png'))

    jewel_img = []
    jewel_img.append(pygame.image.load('Jewel1.png'))

    end_img = []
    end_img.append(pygame.image.load('end1.png'))
    end_img.append(pygame.image.load('end2.png'))

    platform_img = []
    for i in range(1, 6):
        platform_img.append(pygame.image.load('platform_imgs/Platform' + str(i) + '.png'))

    wall = pygame.image.load('wall.png')
    hole = pygame.image.load('hole.png')
    moon = pygame.image.load('moon.png')
    ground_img = pygame.image.load('ground.png')
    
    cloud_imgs = []
    for i in range(1, 6):
        cloud_imgs.append(pygame.image.load('cloud' + str(i) + '.png'))

    veg_imgs = []
    for i in range(1, 4):
        veg_imgs.append(pygame.image.load('vegetation_imgs/vegetation' + str(i) + '.png'))

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
            
        def update(self, pressed_keys, fireball_delay, fireball2_delay):
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
                    self.rect.move_ip(0, 3)
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
                        self.rect.move_ip(-2, 0)
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
                        self.rect.move_ip(0, -4)
                        if self.walkingRight == True:
                            self.image = jumping[0].convert_alpha()
                        else:
                            self.image = jumping[1].convert_alpha()
                    else:
                        self.isFalling = True
                        self.isJumping = False
                        self.jump = 0
                #Falling Mechanism
                if self.isFalling == True:
                    self.rect.move_ip(0, 3)
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

                #Firing Animation
                if self.isFiring == True:
                    if self.walkingRight == True and fireball_delay < 10:
                        self.image = fire[0].convert_alpha()
                    if self.walkingLeft == True and fireball2_delay < 10:
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
            self.image = hole.convert()
            self.rect = self.image.get_rect()
            self.rect.left = x_pos
            self.rect.bottom = 599
        def update(self, pressed_keys):
            if player.round_over == False:
                if pressed_keys[K_RIGHT] and player.rect.left >= 200:
                    self.rect.move_ip(-3, 0)
                if pressed_keys[K_LEFT] and player.rect.left <= 100:
                    self.rect.move_ip(3, 0)
        

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
        def __init__(self, x_pos, y_pos):
            super(Jewel, self).__init__()
            self.image = jewel_img[0].convert_alpha()
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

    class Snail(pygame.sprite.Sprite):
        def __init__(self, player, x, y, movement, movement_max, left, right):
            super(Snail, self).__init__()
            self.image = snail_img[0].convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.left = x
            self.rect.bottom = y
            self.movement_max = movement_max
            self.movement = movement
            self.moving_aniL = 0
            self.moving_aniR = 0
            self.moving_left = left
            self.moving_right = right
            self.movement_delay = 0
            self.health = 2
            self.hurt = False

        def update(self, pressed_keys):
            if player.round_over == False:

                #movement update
                if pressed_keys[K_RIGHT] and player.rect.left >= 200:
                    self.rect.move_ip(-3, 0)
                if pressed_keys[K_LEFT] and player.rect.left <= 100:
                        self.rect.move_ip(3, 0)
                if self.moving_left == True and self.movement < self.movement_max and self.movement_delay == 7:
                    self.rect.move_ip(-2, 0)
                    self.movement += 1
                    self.movement_delay = 0
                if self.moving_left == True and self.movement == self.movement_max:
                    self.movement = 0
                    self.moving_left = False
                    self.moving_right = True
                if self.moving_right == True and self.movement < self.movement_max and self.movement_delay == 7:
                    self.rect.move_ip(2, 0)
                    self.movement += 1
                    self.movement_delay = 0
                if self.moving_right == True and self.movement == self.movement_max:
                    self.movement = 0
                    self.moving_right = False
                    self.moving_left = True
                self.movement_delay += 1

                #movement animation
                if self.moving_left == True and self.hurt == False:
                    self.moving_aniR = 0
                    if self.moving_aniL % 50 == 0:
                        ind = int(self.moving_aniL / 50)
                        self.image = snail_img[ind].convert_alpha()
                    if self.moving_aniL == 99:
                        self.moving_aniL = 0
                    else:
                        self.moving_aniL += 1
                if self.moving_left == True and self.hurt == True:
                    self.moving_aniR = 0
                    if self.moving_aniL % 50 == 0:
                        ind = int(self.moving_aniL / 50)
                        self.image = snail_img_hurt[ind].convert_alpha()
                    if self.moving_aniL == 99:
                        self.moving_aniL = 0
                    else:
                        self.moving_aniL += 1
                        
                if self.moving_right == True and self.hurt == False:
                    self.moving_aniL = 0
                    if self.moving_aniR % 50 == 0:
                        ind = int(self.moving_aniR / 50)
                        self.image = snail_imgR[ind].convert_alpha()
                    if self.moving_aniR == 99:
                        self.moving_aniR = 0
                    else:
                        self.moving_aniR += 1
                if self.moving_right == True and self.hurt == True:
                    self.moving_aniL = 0
                    if self.moving_aniR % 50 == 0:
                        ind = int(self.moving_aniR / 50)
                        self.image = snail_imgR_hurt[ind].convert_alpha()
                    if self.moving_aniR == 99:
                        self.moving_aniR = 0
                    else:
                        self.moving_aniR += 1
                    
                if self.rect.bottom > 600:
                    self.kill()
                    
    class Platform(pygame.sprite.Sprite):
        def __init__(self, player, x, y):
            super(Platform, self).__init__()
            self.image = platform_img[0].convert_alpha()
            self.image.set_colorkey((0, 0, 0), RLEACCEL)
            self.rect = self.image.get_rect()
            self.rect.left = x
            self.rect.bottom = y

        def update(self, pressed_keys):
            if player.round_over == False:
                if pressed_keys[K_RIGHT] and player.rect.left >= 200:
                    self.rect.move_ip(-3, 0)
                if pressed_keys[K_LEFT] and player.rect.left <= 100:
                        self.rect.move_ip(3, 0)
                if self.rect.bottom > 600:
                    self.kill()

    class Platform2(pygame.sprite.Sprite):
        def __init__(self, player, x, y, can_break, ver):
            super(Platform2, self).__init__()
            self.image = platform_img[ver].convert_alpha()
            self.image.set_colorkey((0, 0, 0), RLEACCEL)
            self.rect = self.image.get_rect()
            self.rect.left = x
            self.rect.bottom = y
            self.can_break = can_break

        def update(self, pressed_keys):
            if player.round_over == False:
                if pressed_keys[K_RIGHT] and player.rect.left >= 200:
                    self.rect.move_ip(-3, 0)
                if pressed_keys[K_LEFT] and player.rect.left <= 100:
                        self.rect.move_ip(3, 0)
                if self.rect.bottom > 1000:
                    self.kill()

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


    class Vegetation(pygame.sprite.Sprite):
        def __init__(self, player, x, y, ind):
            super(Vegetation, self).__init__()
            self.image = veg_imgs[ind].convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.left = x
            self.rect.bottom = y

        def update(self, pressed_keys):
            if player.round_over == False:
                if pressed_keys[K_RIGHT] and player.rect.left >= 200:
                    self.rect.move_ip(-3, 0)
                if pressed_keys[K_LEFT] and player.rect.left <= 100:
                    self.rect.move_ip(3, 0)
                if self.rect.right < 0:
                    self.kill()

    class Moon(pygame.sprite.Sprite):
        def __init__(self, player, x, y):
            super(Moon, self).__init__()
            self.image = moon.convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.left = x
            self.rect.bottom = y
            self.delay = 0
            self.delay_max = 50

        def update(self, pressed_keys):
            if player.round_over == False:
                if pressed_keys[K_RIGHT] and player.rect.left >= 200 and self.delay >= self.delay_max:
                    self.rect.move_ip(-2, 0)
                    self.delay = 0
                if pressed_keys[K_LEFT] and player.rect.left <= 100 and self.delay >= self.delay_max:
                    self.rect.move_ip(2, 0)
                    self.delay = 0
                self.delay += 1
                if self.rect.right < 0:
                    self.kill()

                
##    class Cloud(pygame.sprite.Sprite):
##        def __init__(self, delay_max):
##            super(Cloud, self).__init__()
##            ind = random.randint(0, 4)
##            self.image = cloud_imgs[ind].convert_alpha()
##            self.image.set_colorkey((0, 0, 0), RLEACCEL)
##            self.rect = self.image.get_rect(center=(
##                random.randint(820, 900), random.randint(-50, 100))
##            )
##            self.delay = 0
##            self.delay_max = delay_max
##
##        def update(self):
##            if self.delay == self.delay_max:
##                self.rect.move_ip(-1, 0)
##                self.delay = 0
##            self.delay += 1
##            if self.rect.right < 0:
##                self.kill()
                
    #player inititalization
    player = Player()
    all_sprites = pygame.sprite.Group()

    ##enemies = pygame.sprite.Group()


    #Moon initialization
    new_moon = Moon(player, 700, 200)
    all_sprites.add(new_moon)

    #vegetation initialization
    x_pos = 100
    ind = 0
    new_veg = []
    for i in range(20):
        new_veg.append(Vegetation(player, x_pos, 533, ind))
        all_sprites.add(new_veg[i])
        
        x_pos += 300 + random.randint(0, 1000)
        # No vegetation over holes, need to find a better way to do this later
        if x_pos > 3400 and x_pos < 3800:
            x_pos = 3800
        if x_pos > 4400 and x_pos < 5100:
            x_pos = 5100
        if x_pos > 7750 and x_pos < 9050:
            x_pos = 10000
        ind = random.randint(0, 2)
    new_veg_length = len(new_veg)
    
##    #cloud initialization
##    speed = random.randint(3, 7)
##    cloud_count = 0
##    new_cloud = []
##    new_cloud.append(Cloud(speed))
##    all_sprites.add(new_cloud[cloud_count])
##
##
##    ADDCLOUD = pygame.USEREVENT + 2
##    pygame.time.set_timer(ADDCLOUD, 2000)

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
    new_end = End(player, 9200, 533)
    end = pygame.sprite.Group()
    all_sprites.add(new_end)
    end.add(new_end)


    #platfrom initializations
    platform_pos = [(400, 400), (900, 400), (2600, 300),
                    (3900, 400), (4400, 300), (4800, 300), (5350, 20),
                    (7900, 500), (8300, 400), (8700, 300)]
    new_platform = []
    platform = []
    for i in range(len(platform_pos)):
        new_platform.append(Platform(player, platform_pos[i][0], platform_pos[i][1]))
        platform.append(pygame.sprite.Group())
        all_sprites.add(new_platform[i])
        platform[i].add(new_platform[i])
        
    
    new_platform_length = len(new_platform)

    platform_pos2 = [(250, 533, True, 1), (1025, 225, True, 2), (1400, 533, False, 1), (1700, 649, False, 4),
                     (2090, 591, False, 4), (2929, 533, False, 1), (2500, 200, False, 1), (3000, 591, False, 4),(4300, 533, False, 1),
                     (4450, 120, True, 2),(4525, 120, False, 1), (4600, 120, True, 2), (4850, 120, False, 1), (4925, 120, False, 1),
                     (5000, 120, True, 2),(5200, 400, True, 2), (5700, 400, False, 1), (5775, 400, True, 2), (6100, 533, False, 1),
                     (6300, 400, True, 2),(6500, 400, True, 2),(6500, 200, True, 2), (6700, 400, True, 2), (6900, 707, False, 4),
                     (6971, 649, False, 4),(7042, 591, False, 4), (7113, 533, False, 4), (7413, 533, False, 4), (7484, 591, False, 4),
                     (7555, 649, False, 4),(7626, 707, False, 4)]
    new_platform2 = []
    platform2 = []
    for i in range(len(platform_pos2)):
        new_platform2.append(Platform2(player, platform_pos2[i][0], platform_pos2[i][1], platform_pos2[i][2], platform_pos2[i][3]))
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
    hole_pos = [3500, 4400, 4600, 4800, 7750, 7950, 8150, 8350, 8550, 8750]
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
    new_health2.append(Health2(2513, 90))
    health2.append(pygame.sprite.Group())
    all_sprites.add(new_health2[0])
    health2[0].add(new_health2[0])

    #Jewel Initialization
    new_jewel = []
    jewel = []
    new_jewel.append(Jewel(525, 290))
    jewel.append(pygame.sprite.Group())
    all_sprites.add(new_jewel[0])
    jewel[0].add(new_jewel[0])
    x_pos = 5400
    for i in range(1, 5):
        new_jewel.append(Jewel(x_pos, -90))
        jewel.append(pygame.sprite.Group())
        all_sprites.add(new_jewel[i])
        jewel[i].add(new_jewel[i])

        x_pos += 50
        
    new_jewel.append(Jewel(8030, 390))
    jewel.append(pygame.sprite.Group())
    all_sprites.add(new_jewel[5])
    jewel[5].add(new_jewel[5])

    x_pos = 8750
    for i in range(6, 10):
        new_jewel.append(Jewel(x_pos, 190))
        jewel.append(pygame.sprite.Group())
        all_sprites.add(new_jewel[i])
        jewel[i].add(new_jewel[i])

        x_pos += 50
        
    #snail initialization
    snail_pos = [(400, 533, 30, 200), (1000, 342, 50, 100), (1900, 533, 25, 200),
                 (2200, 533, 170, 200), (2500, 533, 12, 200), (4000, 533, 100, 200),
                 (4500, 242, 50, 100), (4900, 242, 50, 100), (5300, 533, 32, 200),
                  (5600, 533, 190, 200), (8400, 342, 50, 100), (8800, 242, 50, 100)]
    new_snail = []
    for i in range(len(snail_pos)):
        direction = random.randint(0, 1)
        if direction == 0:
            left = True
            right = False
        else:
            left = False
            right = True
        new_snail.append(Snail(player, snail_pos[i][0], snail_pos[i][1], snail_pos[i][2], snail_pos[i][3], left, right))
        all_sprites.add(new_snail[i])
    
    new_snail_length = len(new_snail)
        
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
    playerhit = pygame.mixer.Sound('sounds/playerhit.wav')
    up_1 = pygame.mixer.Sound('sounds/1-up.wav')
    jewel_pick = pygame.mixer.Sound('sounds/jewel.wav')
    brick_break = pygame.mixer.Sound('sounds/brick_break.wav')
    fireball_delay = 150
    fireball2_delay = 150
    score = 0
    new_lives = lives
    running = True
    condition = "Death"
    cheat = []

    #Player/Platform Collision Handling
    def Player_Platform(player, new_platfrom, pressed_keys, i):

        #Payer hits bottom of platform
        if player.rect.top <= new_platform[i].rect.bottom and player.rect.bottom > new_platform[i].rect.bottom:
            player.isJumping = False
            player.isFalling = True

        #Player hits top of platfrom
        if player.rect.bottom - 3 <= new_platform[i].rect.top and player.rect.right > new_platform[i].rect.left and player.rect.left < new_platform[i].rect.right:
            if pressed_keys[K_UP]:
                player.isJumping = True
                player.playjump = True
                player.isFalling = False
            player.rect.bottom = new_platform[i].rect.top
            player.jumpheight = new_platform[i].rect.bottom - 350

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
                
                jewel_chance = random.randint(1, 3)

                if jewel_chance == 1:
                    new_jewel.append(Jewel(new_platform2[i].rect.centerx - 20, new_platform2[i].rect.bottom - 50))
                    jewel.append(pygame.sprite.Group())
                    ind = len(new_jewel) - 1
                    all_sprites.add(new_jewel[ind])
                    jewel[ind].add(new_jewel[ind])

                new_platform2[i].rect.bottom += 1000
                player.rect.top = new_platform2[i].rect.bottom - 990

        #Player hits top of platfrom
        if player.rect.bottom - 3 <= new_platform2[i].rect.top and player.rect.right + 10 > new_platform2[i].rect.left and broken == False:
            can_Jump = True
            if pressed_keys[K_UP]:
                player.isJumping = True
                player.playjump = True
                player.isFalling = False
            player.rect.bottom = new_platform2[i].rect.top
            player.jumpheight = new_platform2[i].rect.top - 300

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
        text = font.render("Score: " + str(score), True, (0, 0, 0))
        screen.blit(text, (225, 25))

    def HighScore(highscore):
        font = pygame.font.SysFont('bebas neue', 25)
        text = font.render("High Score: " + str(highscore), True, (0, 0, 0))
        screen.blit(text, (330, 25))

    def display_lives(new_lives):
        font = pygame.font.SysFont('bebas neue', 25)
        text = font.render("Lives: " + str(new_lives), True, (0, 0, 0))
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
                if event.key == K_UP:
                    cheat.append(1)
                if event.key == K_DOWN:
                    cheat.append(2)
                if event.key == K_LEFT:
                    cheat.append(3)
                if event.key == K_RIGHT:
                    cheat.append(4)
                #fireball right event
                if event.key == K_SPACE and fireball_delay > 150 and player.walkingRight == True:
                    fireball_count += 1
                    new_fireball.append(Player.Fireball(player))
                    fireball.append(pygame.sprite.Group())
                    all_sprites.add(new_fireball[fireball_count])
                    fireball[fireball_count].add(new_fireball[fireball_count])
                    pygame.mixer.Sound.play(fireblast)
                    fireball_delay = 0
                    cheat = []

                #fireball left event
                if event.key == K_SPACE and fireball2_delay > 150 and player.walkingLeft == True:
                    fireball_count2 += 1
                    new_fireball2.append(Player.Fireball2(player))
                    fireball2.append(pygame.sprite.Group())
                    all_sprites.add(new_fireball2[fireball_count2])
                    fireball2[fireball_count2].add(new_fireball2[fireball_count2])
                    pygame.mixer.Sound.play(fireblast)
                    fireball2_delay = 0
                    cheat = []
                
##            elif event.type == ADDCLOUD:
##                speed = random.randint(3, 7)
##                cloud_count += 1
##                new_cloud.append(Cloud(speed))
##                all_sprites.add(new_cloud[cloud_count])


##        new_cloud_length = len(new_cloud)
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
                Player_Platform2(player, new_platform2, pressed_keys, i)

        new_jewel_length = len(new_jewel)

        #player/initial wall collision
        if pygame.sprite.spritecollideany(player, wall):
            player.rect.left = new_wall.rect.right

##        #wall/clouds collison (need to edit for clouds to go behind wall)
##        for i in range(new_cloud_length):
##            if pygame.sprite.spritecollideany(new_cloud[i], wall):
##                new_cloud[i].kill()

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

        #Right Fireball/Snail collision
        for i in range(new_fireball_length):
            for j in range(new_snail_length):
                if pygame.sprite.spritecollideany(new_snail[j], fireball[i]):
                    pygame.mixer.Sound.play(playerhit)
                    new_fireball[i].kill()
                    new_snail[j].health -= 1
                    new_snail[j].hurt = True
                    
                    if new_snail[j].health == 0:            
                        score += 100

                        #HEALTHDROP CHANCE
                        health_chance = random.randint(1, 5)

                        if health_chance == 1 and player.health < 2:
                            new_health2.append(Health2(new_snail[j].rect.left, new_snail[j].rect.bottom - 50))
                            health2.append(pygame.sprite.Group())
                            ind = len(new_health2) - 1
                            all_sprites.add(new_health2[ind])
                            health2[ind].add(new_health2[ind])
                        new_snail[j].rect.bottom = 1000

        #Left Fireball/Snail collision          
        for i in range(new_fireball_length2):
            for j in range(new_snail_length):
                if pygame.sprite.spritecollideany(new_snail[j], fireball2[i]):
                    pygame.mixer.Sound.play(playerhit)
                    new_fireball2[i].kill()
                    new_snail[j].health -= 1
                    new_snail[j].hurt = True

                    if new_snail[j].health == 0:
                        score += 100

                        #HEALTHDROPCHANCE
                        health_chance = random.randint(1, 5)

                        if health_chance == 1 and player.health < 2:
                            new_health2.append(Health2(new_snail[j].rect.left, new_snail[j].rect.bottom - 50))
                            health2.append(pygame.sprite.Group())
                            ind = len(new_health2) - 1
                            all_sprites.add(new_health2[ind])
                            health2[ind].add(new_health2[ind])
                        new_snail[j].rect.bottom = 1000
                        
        new_health_length2 = len(new_health2)

        #Snail/platform2 collision
        for i in range(new_snail_length):
            for j in range(new_platform_length2):
                if pygame.sprite.spritecollideany(new_snail[i], platform2[j]):
                    if new_snail[i].moving_left == True:
                        new_snail[i].moving_left = False
                        new_snail[i].moving_right = True
                        new_snail[i].rect.left += 1
                    else:
                        new_snail[i].moving_right = False
                        new_snail[i].moving_left = True
                        new_snail[i].rect.left -= 1
                    new_snail[i].movement = 0

        #Snail/hole collision
        for i in range(new_snail_length):
            for j in range(new_hole_length):
                if pygame.sprite.spritecollideany(new_snail[i], holes[j]):
                    if new_snail[i].moving_left == True:
                        new_snail[i].moving_left = False
                        new_snail[i].moving_right = True
                        new_snail[i].rect.left += 1
                    else:
                        new_snail[i].moving_right = False
                        new_snail[i].moving_left = True
                        new_snail[i].rect.left -= 1
                    new_snail[i].movement = 0
                    
        #Player/Snail collision
        if pygame.sprite.spritecollideany(player, new_snail):
            score -= 50
            if player.health == 0:
                player.kill()
                new_health[player.health].image = health_img[1].convert_alpha()
                player.health -= 1
            if player.health > 0:
                pygame.mixer.Sound.play(playerhit)
                player.rect.right -= 50
                player.rect.bottom -= 300
                player.isFalling = True
                new_health[player.health].image = health_img[1].convert_alpha()
                player.health -= 1
        
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
                score += 200

        #Player/hole collison
        for i in range(new_hole_length):
            if pygame.sprite.spritecollideany(player, holes[i]):
                if player.rect.left >= new_hole[i].rect.left and player.rect.right < new_hole[i].rect.right:
                    player.isFalling = True
                    player.inHole = True
                if player.rect.right > new_hole[i].rect.right and player.rect.bottom - 5> new_hole[i].rect.top:
                    player.rect.right = new_hole[i].rect.right
                if player.rect.left < new_hole[i].rect.left and player.rect.bottom - 5> new_hole[i].rect.top:
                    player.rect.left = new_hole[i].rect.left

        #Player/End Flag collision
        if pygame.sprite.spritecollideany(player, end):
            player.max_movement = 1000
            player.round_over = True
            

        

        ##Fixed Updates
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys, fireball_delay, fireball2_delay)
        new_moon.update(pressed_keys)
        new_end.update(pressed_keys)

        for i in range(new_snail_length):
            new_snail[i].update(pressed_keys)
            
        for i in range(new_platform_length):  
            platform[i].update(pressed_keys)

        for i in range(new_platform_length2):  
            platform2[i].update(pressed_keys)
            
        for i in range(new_veg_length):
            new_veg[i].update(pressed_keys)

        for i in range(new_ground_length):
            new_ground[i].update(pressed_keys)

        for i in range(new_hole_length):
            new_hole[i].update(pressed_keys)

        ##Dynamic Udates
##        for i in range(new_cloud_length):
##            new_cloud[i].update()

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
            condition = "Death"
            new_lives -= 1
            running = False

        if player.rect.right > 999:
            condition = "Complete"
            running = False


        #no negative score
        if score < 0:
            score = 0

        #CHEATS
        if len(cheat) == 8:
            #PLUS 100 SCORE
            if cheat == [1, 2, 1, 2, 3, 4, 3, 4]:
                score += 100
                pygame.mixer.Sound.play(jewel_pick)
                cheat = []
            #PLUS 1 LIFE
            elif cheat == [3, 1, 4, 2, 3, 1, 4, 2]:
                new_lives += 1
                cheat = []
            #NO SNAILS
            elif cheat == [2, 2, 1, 1, 2, 2, 1, 1]:
                for i in range(new_snail_length):
                    new_snail[i].rect.bottom = 3000
            else:
                cheat = []
        Scoreboard(score)
        HighScore(highscore)
        display_lives(new_lives)

        pygame.display.update()
    return score, condition, new_lives
