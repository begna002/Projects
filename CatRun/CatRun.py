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

def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()

def game_intro():
    pygame.mixer.music.load('vaporwave.wav')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
    
    
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    intro = False
        largeText = pygame.font.SysFont('bebas neue', 115)
        screen.fill((135, 150, 250))
        TextSurf, TextRect = text_objects("Cat Run", largeText)
        TextRect.center = ((800/2), (200))
        screen.blit(TextSurf, TextRect)

        smallText = pygame.font.SysFont('bebas neue', 50)
        TextSurf2, TextRect2 = text_objects("Press Space to Play", smallText)
        TextRect2.center = ((800/2), (300))
        screen.blit(TextSurf2, TextRect2)
        pygame.display.update()

def death_screen():
    death = True

    while death:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    death = False
                    pygame.quit()
                    quit()
                if event.key == K_SPACE:
                    return True
        largeText = pygame.font.SysFont('bebas neue', 115)
        TextSurf, TextRect = text_objects("You Died!", largeText)
        TextRect.center = ((800/2), (200))
        screen.blit(TextSurf, TextRect)

        smallText = pygame.font.SysFont('bebas neue', 50)
        TextSurf2, TextRect2 = text_objects("Press Escape to Quit", smallText)
        TextRect2.center = ((800/2), (275))
        screen.blit(TextSurf2, TextRect2)

        TextSurf3, TextRect3 = text_objects("Press Space to Play Again", smallText)
        TextRect3.center = ((800/2), (325))
        screen.blit(TextSurf3, TextRect3)
        pygame.display.update()


                
def game_loop():
    walking = []
    for i in range(1, 5):
        walking.append(pygame.image.load('catwalk' + str(i) + '.png'))
    walkingL = []
    for i in range(1, 5):
        walkingL.append(pygame.image.load('catwalkL' + str(i) + '.png'))
    jumping = []
    jumping.append(pygame.image.load('catjump1.png'))
    jumping.append(pygame.image.load('catjump2.png'))

    fire = []
    fire.append(pygame.image.load('catfight1.png'))
    fire.append(pygame.image.load('catfight2.png'))

    stationary = []
    stationary.append(pygame.image.load('catstationary1.png'))
    stationary.append(pygame.image.load('catstationary2.png'))

    stationaryL = []
    stationaryL.append(pygame.image.load('catstationaryL1.png'))
    stationaryL.append(pygame.image.load('catstationaryL2.png'))

    snail_img = []
    snail_img.append(pygame.image.load('snail1.png'))
    snail_img.append(pygame.image.load('snail2.png'))

    snail_imgR = []
    snail_imgR.append(pygame.image.load('snail1R.png'))
    snail_imgR.append(pygame.image.load('snail2R.png'))

    health_img = []
    health_img.append(pygame.image.load('healthfull.png'))
    health_img.append(pygame.image.load('healthempty.png'))



    wall = pygame.image.load('wall.png')
    moon = pygame.image.load('moon.png')
    
    cloud_imgs = []
    for i in range(1, 6):
        cloud_imgs.append(pygame.image.load('cloud' + str(i) + '.png'))

    veg_imgs = []
    for i in range(1, 4):
        veg_imgs.append(pygame.image.load('vegetation' + str(i) + '.png'))

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super(Player, self).__init__()
            self.image = walking[0].convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.left = 50
            self.rect.bottom = 533
            self.isJumping = False
            self.isFalling = False
            self.isFiring = False
            self.jumpheight = 200
            self.playjump = False
            self.walk = 0
            self.walkL = 0
            self.stationary = 0
            self.stationaryL = 0
            self.walkingRight = True
            self.walkingLeft = False
            self.isStationary = True
        def update(self, pressed_keys):
            self.isStationary = True
            self.isFiring = False

            if pressed_keys[K_UP] and self.isJumping == False and self.isFalling == False:
                self.isStationary = False
                self.isJumping = True
                self.playjump = True
                self.isFiring = False
            if pressed_keys[K_DOWN] and self.isJumping == False and self.isFalling == False:
                self.isStationary = False
                self.rect.move_ip(0, 1)
            if pressed_keys[K_LEFT]:
                self.isStationary = False
                self.walkingLeft = True
                self.walkingRight = False
                self.isFiring = False
                self.walk = 0
                if self.walkL == 199:
                    self.walkL = 0
                else:
                    self.walkL += 1
                if self.rect.left > 100:
                    self.rect.move_ip(-1, 0)
            if pressed_keys[K_RIGHT]:
                self.isStationary = False
                self.walkingRight = True
                self.walkingLeft = False
                self.isFiring = False
                self.walkL = 0
                if self.walk == 199:
                    self.walk = 0
                else:
                    self.walk += 1
                if self.rect.left < 200:
                    self.rect.move_ip(1, 0)
            if pressed_keys[K_SPACE]:
                self.isFiring = True
                self.walk = 0
                self.walkL = 0
            
            #walking animation
            if self.walk % 50 == 0 and self.walkingRight == True and self.isStationary == False:
                ind = int(self.walk / 50)
                self.image = walking[ind].convert_alpha()
            if self.walk == 1 and self.isStationary == False:
                self.image = walking[0].convert_alpha()
            if self.walkL % 50 == 0 and self.walkingLeft == True and self.isStationary == False:
                ind2 = int(self.walkL / 50)
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
                    self.rect.move_ip(0, -2)
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
                self.rect.move_ip(0, 1)
                if self.rect.bottom == 533 or self.rect.bottom == 342:
                    self.walk = 0
                    self.walkL = 0

            #stationary animation
            if self.isStationary == True and self.walkingRight == True:
                self.stationaryL = 0
                if self.stationary % 100 == 0:
                    ind = int(self.stationary / 100)
                    self.image = stationary[ind].convert_alpha()
                if self.stationary == 199:
                    self.stationary = 0
                else:
                    self.stationary += 1
            if self.isStationary == True and self.walkingLeft == True:
                self.stationary = 0
                if self.stationaryL % 100 == 0:
                    ind = int(self.stationaryL / 100)
                    self.image = stationaryL[ind].convert_alpha()
                if self.stationaryL == 199:
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
            elif self.rect.right > 795:
                self.rect.right = 800
            elif self.rect.bottom >= 533:
                self.rect.bottom = 533
                self.isFalling = False
                self.jumpheight = 200
        class Fireball(pygame.sprite.Sprite):
            def __init__(self, player):
                super(Player.Fireball, self).__init__()
                self.image = pygame.image.load('fireball1.png').convert_alpha()
                self.rect = self.image.get_rect()
                self.rect.left = player.rect.right
                self.rect.bottom = player.rect.bottom - 20
            def update(self):
                self.rect.move_ip(1, 0)
                if self.rect.left > 800:
                    self.kill()
        class Fireball2(pygame.sprite.Sprite):
            def __init__(self, player):
                super(Player.Fireball2, self).__init__()
                self.image = pygame.image.load('fireball2.png').convert_alpha()
                self.rect = self.image.get_rect()
                self.rect.right = player.rect.left
                self.rect.bottom = player.rect.bottom - 20
            def update(self):
                self.rect.move_ip(-1, 0)
                if self.rect.right < 0:
                    self.kill()
        
    class Ground(pygame.sprite.Sprite):
        def __init__(self, player, x_pos):
            super(Ground, self).__init__()
            self.image = pygame.image.load('ground.png').convert()
            self.rect = self.image.get_rect()
            self.rect.left = x_pos
            self.rect.bottom = 600
        def update(self, pressed_keys):
            if pressed_keys[K_RIGHT] and player.rect.left >= 200:
                self.rect.move_ip(-1, 0)
            if pressed_keys[K_LEFT] and player.rect.left <= 100:
                self.rect.move_ip(1, 0)
        

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
            if pressed_keys[K_RIGHT] and player.rect.left >= 200:
                self.rect.move_ip(-1, 0)
            if pressed_keys[K_LEFT] and player.rect.left <= 100:
                    self.rect.move_ip(1, 0)
            if self.moving_down == True and self.movement < self.movement_max and self.movement_delay == 7:
                self.rect.move_ip(0, 1)
                self.movement += 1
                self.movement_delay = 0
            if self.moving_down == True and self.movement == self.movement_max:
                self.movement = 0
                self.moving_down = False
                self.moving_up = True
            if self.moving_up == True and self.movement < self.movement_max and self.movement_delay == 7:
                self.rect.move_ip(0, -1)
                self.movement += 1
                self.movement_delay = 0
            if self.moving_up == True and self.movement == self.movement_max:
                self.movement = 0
                self.moving_up = False
                self.moving_down = True
            self.movement_delay += 1
            if self.rect.bottom > 600:
                self.kill()
                    
    ##class Enemy(pygame.sprite.Sprite):
    ##    def __init__(self):
    ##        super(Enemy, self).__init__()
    ##        self.image = pygame.image.load('missile.png').convert()
    ##        self.image.set_colorkey((255, 255, 255), RLEACCEL)
    ##        self.rect = self.image.get_rect(
    ##            center=(random.randint(820, 900), random.randint(300, 500)))
    ##        self.speed = random.randint(1, 2)
    ##
    ##    def update(self):
    ##        self.rect.move_ip(-self.speed, 0)
    ##        if self.rect.right < 0:
    ##            self.kill()

    class Snail(pygame.sprite.Sprite):
        def __init__(self, player, x, y, movement, left, right):
            super(Snail, self).__init__()
            self.image = snail_img[0].convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.left = x
            self.rect.bottom = y
            self.movement_max = 200
            self.movement = movement
            self.moving_aniL = 0
            self.moving_aniR = 0
            self.moving_left = left
            self.moving_right = right
            self.movement_delay = 0

        def update(self, pressed_keys):

            #movement update
            if pressed_keys[K_RIGHT] and player.rect.left >= 200:
                self.rect.move_ip(-1, 0)
            if pressed_keys[K_LEFT] and player.rect.left <= 100:
                    self.rect.move_ip(1, 0)
            if self.moving_left == True and self.movement < self.movement_max and self.movement_delay == 7:
                self.rect.move_ip(-1, 0)
                self.movement += 1
                self.movement_delay = 0
            if self.moving_left == True and self.movement == self.movement_max:
                self.movement = 0
                self.moving_left = False
                self.moving_right = True
            if self.moving_right == True and self.movement < self.movement_max and self.movement_delay == 7:
                self.rect.move_ip(1, 0)
                self.movement += 1
                self.movement_delay = 0
            if self.moving_right == True and self.movement == self.movement_max:
                self.movement = 0
                self.moving_right = False
                self.moving_left = True
            self.movement_delay += 1

            #movement animation
            if self.moving_left == True:
                self.moving_aniR = 0
                if self.moving_aniL % 100 == 0:
                    ind = int(self.moving_aniL / 100)
                    self.image = snail_img[ind].convert_alpha()
                if self.moving_aniL == 199:
                    self.moving_aniL = 0
                else:
                    self.moving_aniL += 1
            if self.moving_right == True:
                self.moving_aniL = 0
                if self.moving_aniR % 100 == 0:
                    ind = int(self.moving_aniR / 100)
                    self.image = snail_imgR[ind].convert_alpha()
                if self.moving_aniR == 199:
                    self.moving_aniR = 0
                else:
                    self.moving_aniR += 1
                
            if self.rect.bottom > 600:
                self.kill()
                    
    class Platform(pygame.sprite.Sprite):
        def __init__(self, player, x, y):
            super(Platform, self).__init__()
            self.image = pygame.image.load('Platform1.png').convert_alpha()
            self.image.set_colorkey((0, 0, 0), RLEACCEL)
            self.rect = self.image.get_rect()
            self.rect.left = x
            self.rect.bottom = y

        def update(self, pressed_keys):
            if pressed_keys[K_RIGHT] and player.rect.left >= 200:
                self.rect.move_ip(-1, 0)
            if pressed_keys[K_LEFT] and player.rect.left <= 100:
                    self.rect.move_ip(1, 0)

    class Platform2(pygame.sprite.Sprite):
        def __init__(self, player, x, y):
            super(Platform2, self).__init__()
            self.image = pygame.image.load('Platform2.png').convert_alpha()
            self.image.set_colorkey((0, 0, 0), RLEACCEL)
            self.rect = self.image.get_rect()
            self.rect.left = x
            self.rect.bottom = y

        def update(self, pressed_keys):
            if pressed_keys[K_RIGHT] and player.rect.left >= 200:
                self.rect.move_ip(-1, 0)
            if pressed_keys[K_LEFT] and player.rect.left <= 100:
                    self.rect.move_ip(1, 0)

    class Wall(pygame.sprite.Sprite):
        def __init__(self, player):
            super(Wall, self).__init__()
            self.image = wall.convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.right = 42
            self.rect.bottom = 533

        def update(self, pressed_keys):
            if pressed_keys[K_RIGHT] and player.rect.left >= 200:
                self.rect.move_ip(-1, 0)
            if pressed_keys[K_LEFT] and player.rect.left <= 100:
                    self.rect.move_ip(1, 0)


    class Vegetation(pygame.sprite.Sprite):
        def __init__(self, player, x, y, ind):
            super(Vegetation, self).__init__()
            self.image = veg_imgs[ind].convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.left = x
            self.rect.bottom = y

        def update(self, pressed_keys):
            if pressed_keys[K_RIGHT] and player.rect.left >= 200:
                self.rect.move_ip(-1, 0)
            if pressed_keys[K_LEFT] and player.rect.left <= 100:
                self.rect.move_ip(1, 0)
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
            if pressed_keys[K_RIGHT] and player.rect.left >= 200 and self.delay >= self.delay_max:
                self.rect.move_ip(-1, 0)
                self.delay = 0
            if pressed_keys[K_LEFT] and player.rect.left <= 100 and self.delay >= self.delay_max:
                self.rect.move_ip(1, 0)
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
    
##    #cloud initialization
##    speed = random.randint(3, 7)
##    cloud_count = 0
##    new_cloud = []
##    new_cloud.append(Cloud(speed))
##    all_sprites.add(new_cloud[cloud_count])
##
##
##    # Create a custom event for adding a new enemy.
##    ##ADDENEMY = pygame.USEREVENT + 1
##    ##pygame.time.set_timer(ADDENEMY, 1000)
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
    fireball2[fireball_count2].add(new_fireball[fireball_count])

    #Ground initialization
    x_pos = -100
    new_ground = []
    for i in range(50):
        new_ground.append(Ground(player, x_pos))
        all_sprites.add(new_ground[i])
        x_pos += 800
    new_ground_length = len(new_ground)

    #platfrom initializations
    x_pos = 400
    new_platform = []
    platform = []
    for i in range(40):
        new_platform.append(Platform(player, x_pos, 400))
        platform.append(pygame.sprite.Group())
        all_sprites.add(new_platform[i])
        platform[i].add(new_platform[i])
        
        x_pos += 400 + random.randint(0, 800)
    new_platform_length = len(new_platform)

    x_pos = 800
    new_platform2 = []
    platform2 = []
    for i in range(40):
        new_platform2.append(Platform2(player, x_pos, 250))
        platform2.append(pygame.sprite.Group())
        all_sprites.add(new_platform2[i])
        platform2[i].add(new_platform2[i])
        
        x_pos += 400 + random.randint(0, 800)
    new_platform_length2 = len(new_platform2)

    #initial wall
    new_wall = Wall(player)
    wall = pygame.sprite.Group()
    all_sprites.add(new_wall)
    wall.add(new_wall)

    #Health initialization
    x_pos = 50
    new_health = []
    for i in range(3):
        new_health.append(Health(x_pos, 50))
        all_sprites.add(new_health[i])
        x_pos += 50
    new_health_length = len(new_health)

    new_health2 = []
    health2 = []
    new_health2.append(Health2(1000, 1000))
    health2.append(pygame.sprite.Group)
    all_sprites.add(new_health2[0])
    health2[0].add(new_health[0])
        
    #vegetation initialization
    x_pos = 100
    ind = 0
    new_veg = []
    for i in range(50):
        new_veg.append(Vegetation(player, x_pos, 533, ind))
        all_sprites.add(new_veg[i])
        
        x_pos += 20 + random.randint(0, 1000)
        ind = random.randint(0, 2)
    new_veg_length = len(new_veg)

    #snail initialization
    x_pos = 400
    new_snail = []
    for i in range(25):
        movement = random.randint(0, 199)
        direction = random.randint(0, 1)
        if direction == 0:
            left = True
            right = False
        else:
            left = False
            right = True
        new_snail.append(Snail(player, x_pos, 533, movement, left, right))
        all_sprites.add(new_snail[i])

        x_pos += 300 + random.randint(0, 1000)
    new_snail_length = len(new_snail)
        
    #adding player last to be infront of objects
    all_sprites.add(player)

    running = True

    fireblast = pygame.mixer.Sound('blast.wav')
    jump = pygame.mixer.Sound('jump.wav')
    playerhit = pygame.mixer.Sound('playerhit.wav')
    up_1 = pygame.mixer.Sound('1-up.wav')
    fireball_delay = 300
    fireball2_delay = 300
    current_health = 2
    score = 0
    running = True

    #Player/Platform Collision Handling
    def Player_Platform(player, new_platfrom, pressed_keys, i):

        #Payer hits bottom of platform
        if player.rect.top <= new_platform[i].rect.bottom and player.rect.bottom > new_platform[i].rect.bottom:
            player.isJumping = False
            player.isFalling = True

        #Player hits top of platfrom
        if player.rect.bottom - 2 <= new_platform[i].rect.top:
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

        #Payer hits bottom of platform
        if player.rect.top <= new_platform2[i].rect.bottom and player.rect.bottom > new_platform2[i].rect.bottom:
            player.isJumping = False
            player.isFalling = True

        #Player hits top of platfrom
        if player.rect.bottom - 2 <= new_platform2[i].rect.top:
            if pressed_keys[K_UP]:
                player.isJumping = True
                player.playjump = True
                player.isFalling = False
            player.rect.bottom = new_platform2[i].rect.top
            player.jumpheight = new_platform2[i].rect.bottom - 300

        #Player hits left of platform
        if player.rect.right >= new_platform2[i].rect.left and player.rect.left + 40 < new_platform2[i].rect.left and player.rect.bottom > new_platfrom2[i].rect.top:
            player.rect.right = new_platform2[i].rect.left

        #Player hits right of platform
        if player.rect.left <= new_platform2[i].rect.right and player.rect.right - 40 > new_platform2[i].rect.right and player.rect.bottom > new_platfrom2[i].rect.top:
            player.rect.left = new_platform2[i].rect.right

    def Scoreboard(score):
        font = pygame.font.SysFont('bebas neue', 25)
        text = font.render("Score: " + str(score), True, (0, 0, 0))
        screen.blit(text, (225, 25))

    while running:
        new_fireball[0].kill()
        new_fireball2[0].kill()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                #fireball right event
                if event.key == K_SPACE and fireball_delay > 300 and player.walkingRight == True:
                    fireball_count += 1
                    new_fireball.append(Player.Fireball(player))
                    fireball.append(pygame.sprite.Group())
                    all_sprites.add(new_fireball[fireball_count])
                    fireball[fireball_count].add(new_fireball[fireball_count])
                    pygame.mixer.Sound.play(fireblast)
                    fireball_delay = 0

                #fireball left event
                if event.key == K_SPACE and fireball2_delay > 300 and player.walkingLeft == True:
                    fireball_count2 += 1
                    new_fireball2.append(Player.Fireball2(player))
                    fireball2.append(pygame.sprite.Group())
                    all_sprites.add(new_fireball2[fireball_count2])
                    fireball2[fireball_count2].add(new_fireball2[fireball_count2])
                    pygame.mixer.Sound.play(fireblast)
                    fireball2_delay = 0
                
            elif event.type == QUIT:
                pygame.quit()
    ##        elif event.type == ADDENEMY:
    ##            new_enemy = Enemy()
    ##            enemies.add(new_enemy)
    ##            all_sprites.add(new_enemy)
                
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
                    score += 100

                    #HEALTHDROP CHANCE
                    health_chance = random.randint(1, 5)

                    if health_chance == 1 and current_health < 2:
                        new_health2.append(Health2(new_snail[j].rect.left, new_snail[j].rect.bottom - 25))
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
                    score += 100

                    #HEALTHDROPCHANCE
                    health_chance = random.randint(1, 5)

                    if health_chance == 1 and current_health < 2:
                        new_health2.append(Health2(new_snail[j].rect.left, new_snail[j].rect.bottom - 25))
                        health2.append(pygame.sprite.Group())
                        ind = len(new_health2) - 1
                        all_sprites.add(new_health2[ind])
                        health2[ind].add(new_health2[ind])
                    new_snail[j].rect.bottom = 1000
        new_health_length2 = len(new_health2)

        #Player/Snail collision
        if pygame.sprite.spritecollideany(player, new_snail):
            score -= 50
            if current_health == 0:
                player.kill()
                new_health[current_health].image = health_img[1].convert_alpha()
                running = False
            else:
                pygame.mixer.Sound.play(playerhit)
                player.rect.right -= 50
                player.rect.bottom -= 300
                player.isFalling = True
                new_health[current_health].image = health_img[1].convert_alpha()
                current_health -= 1

        #Groundhealth/player collision
        for i in range(1, len(new_health2)):
            if pygame.sprite.spritecollideany(player, health2[i]) and current_health < 2:
                pygame.mixer.Sound.play(up_1)
                new_health2[i].rect.bottom = 2000
                current_health += 1
                new_health[current_health].image = health_img[0].convert_alpha()
            

        

        ##Fixed Updates
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        new_moon.update(pressed_keys)

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

        ##Dynamic Udates
##        for i in range(new_cloud_length):
##            new_cloud[i].update()

        for i in range(new_fireball_length):
            new_fireball[i].update()

        for i in range(new_fireball_length2):
            new_fireball2[i].update()

        for i in range(new_health_length2):
            new_health2[i].update(pressed_keys)

        wall.update(pressed_keys)

        #Fireball delay incrementation
        if player.walkingRight:
            fireball_delay += 1
        if player.walkingLeft:
            fireball2_delay += 1
        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)


    ##    if isEnemy:
    ##        if pygame.sprite.spritecollideany(new_enemy, fireball):
    ##            new_enemy.kill()

        #no negative score
        if score < 0:
            score = 0
        Scoreboard(score)

        pygame.display.update()

play = True

game_intro()
while(play):
    game_loop() 
    play = death_screen()
