#Copyright 2019, Moti Begna

import Level_1
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
    pygame.mixer.music.load('sounds/vaporwave.wav')
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

def level_complete_screen():
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
        TextSurf, TextRect = text_objects("Level Complete!", largeText)
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


play = True

game_intro()
while(play):    
    file = open("Highscore.txt", "r")
    highscore = int(file.readline())
    score, condition = Level_1.game_loop(highscore)
    file.close()
    if score > highscore:
        file = open("Highscore.txt", "w")
        file.write(str(score))
        file.close()
    if condition == "Complete":
        play = level_complete_screen()
    else:
        play = death_screen()
                
