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
 
def text_objects(text, font):
    textSurface = font.render(text, True, (255, 255, 255))
    return textSurface, textSurface.get_rect()



def loop(lives, temp_lives):
    pygame.mixer.music.stop()
    walking = []
    for i in range(1, 5):
        walking.append(pygame.image.load('cat_imgs/catwalk' + str(i) + '.png'))

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super(Player, self).__init__()
            self.image = walking[0].convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.left = -100
            self.rect.bottom = 533
            self.walk = 0
            self.start = False
            
        def update(self):
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
            self.rect.move_ip(1, 0)

    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    player.start = True


        largeText = pygame.font.SysFont('bebas neue', 115)
        TextSurf, TextRect = text_objects("Level 2", largeText)
        TextRect.center = ((800/2), (200))

        msg = "No Snails, Just Spikey Boys"
        if temp_lives - 1 == lives:
            msg = "Minor set back, try again"
        if temp_lives - 2 == lives:
            msg = "Ok, even bigger set back.."
        if lives == 1:
            msg = "Last life, use it well!"

        smallText = pygame.font.SysFont('bebas neue', 50)
        TextSurf2, TextRect2 = text_objects(msg, smallText)
        TextRect2.center = ((800/2), (275))

        TextSurf3, TextRect3 = text_objects("Lives: " + str(lives), smallText)
        TextRect3.center = ((800/2), (325))

        screen.blit(background, (0, 0))
        screen.blit(TextSurf, TextRect)
        screen.blit(TextSurf2, TextRect2)
        screen.blit(TextSurf3, TextRect3)
        screen.blit(player.image, player.rect)
        player.update()

        if player.rect.left > 800:
            player.kill()
            intro = False
        pygame.display.update()

