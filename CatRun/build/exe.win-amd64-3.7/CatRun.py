#Copyright 2019, Moti Begna

import Level_1_intro
import Level_1

import Level_2_intro
import Level_2
import pygame
import random
from pygame.locals import *

# initialize pygame
pygame.init()

# create the screen object
# here we pass it a size of 800x600
screen = pygame.display.set_mode((800, 600))


 
def text_objects(text, font):
    textSurface = font.render(text, True, (255, 255, 255))
    return textSurface, textSurface.get_rect()



def game_intro(highscore):
    pygame.mixer.music.load('sounds/vaporwave.wav')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
    background_img = pygame.image.load('intro_img.png').convert()

    walking = []
    for i in range(1, 5):
        walking.append(pygame.image.load('cat_imgs/catwalk' + str(i) + '.png'))

    jewel_img = []
    jewel_img.append(pygame.image.load('Jewel1.png'))

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super(Player, self).__init__()
            self.image = walking[0].convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.left = 373
            self.rect.bottom = 533
            self.walk = 0
            self.start = False
            
        def update(self):
            #walking animation
            if self.walk % 70 == 0:
                ind = int(self.walk / 70)
                self.image = walking[ind].convert_alpha()
            if self.walk == 1:
                self.image = walking[0].convert_alpha()
            if self.walk == 279:
                self.walk = 0
            else:
                self.walk += 1

            if self.start == True:
                self.rect.move_ip(1, 0)

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
        def update(self):
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

    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    new_jewel = []
    jewel = []
    x_pos = 180
    for i in range(2):
        new_jewel.append(Jewel(x_pos, 225))
        jewel.append(pygame.sprite.Group())
        all_sprites.add(new_jewel[i])
        jewel[i].add(new_jewel[i])

        x_pos += 420
    new_jewel_length = len(new_jewel)

    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == K_SPACE:
                    player.start = True


        screen.blit(background_img, [0, 0])
        
        player.update()
        for i in range(new_jewel_length):
            new_jewel[i].update()

        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)

        if player.rect.left > 800:
            player.kill()
            intro = False

        
        smallText = pygame.font.SysFont('bebas neue', 50)
        TextSurf3, TextRect3 = text_objects("High Score: " + str(highscore), smallText)
        TextRect3.center = ((800/2), (560))
        screen.blit(TextSurf3, TextRect3)
        
        pygame.display.update()

def game_end(new_score):
    pygame.mixer.music.load('sounds/vaporwave.wav')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
    background_img = pygame.image.load('ending_img.png').convert()

    walking = []
    for i in range(1, 5):
        walking.append(pygame.image.load('cat_imgs/catwalk' + str(i) + '.png'))

    jewel_img = []
    jewel_img.append(pygame.image.load('Jewel1.png'))

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super(Player, self).__init__()
            self.image = walking[0].convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.left = 373
            self.rect.bottom = 533
            self.walk = 0
            self.start = False
            
        def update(self):
            #walking animation
            if self.walk % 70 == 0:
                ind = int(self.walk / 70)
                self.image = walking[ind].convert_alpha()
            if self.walk == 1:
                self.image = walking[0].convert_alpha()
            if self.walk == 279:
                self.walk = 0
            else:
                self.walk += 1


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
        def update(self):
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

    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    new_jewel = []
    jewel = []
    x_pos = 120
    for i in range(2):
        new_jewel.append(Jewel(x_pos, 225))
        jewel.append(pygame.sprite.Group())
        all_sprites.add(new_jewel[i])
        jewel[i].add(new_jewel[i])

        x_pos += 545
    new_jewel_length = len(new_jewel)

    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == K_SPACE:
                    return "Play Again"


        screen.blit(background_img, [0, 0])
        
        player.update()
        for i in range(new_jewel_length):
            new_jewel[i].update()

        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)

        if player.rect.left > 800:
            player.kill()
            intro = False

        smallText = pygame.font.SysFont('bebas neue', 50)
        TextSurf3, TextRect3 = text_objects("Your Score: " + str(new_score), smallText)
        TextRect3.center = ((800/2), (560))
        screen.blit(TextSurf3, TextRect3)
        
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

        TextSurf3, TextRect3 = text_objects("Press Space to Restart Game", smallText)
        TextRect3.center = ((800/2), (325))
        screen.blit(TextSurf3, TextRect3)
        pygame.display.update()


def life_lost():
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

        TextSurf3, TextRect3 = text_objects("Press Space to try again", smallText)
        TextRect3.center = ((800/2), (325))
        screen.blit(TextSurf3, TextRect3)
        pygame.display.update()

def level_complete_screen(level):
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
        TextSurf, TextRect = text_objects("Level " + str(level) + " Complete!", largeText)
        TextRect.center = ((800/2), (200))
        screen.blit(TextSurf, TextRect)

        smallText = pygame.font.SysFont('bebas neue', 50)
        TextSurf2, TextRect2 = text_objects("Press Escape to Quit", smallText)
        TextRect2.center = ((800/2), (275))
        screen.blit(TextSurf2, TextRect2)

        TextSurf3, TextRect3 = text_objects("Press Space to Continue", smallText)
        TextRect3.center = ((800/2), (325))
        screen.blit(TextSurf3, TextRect3)
        pygame.display.update()

def main():
    play = True

    while(play):
        lives = 3
        file = open("Highscore.txt", "r")
        highscore = int(file.readline())
        file.close()
        new_score = 0

        game_intro(highscore)

        
        #LEVEL 1
        redo = True
        temp_lives = lives
        level = 1
        while redo == True:
            Level_1_intro.loop(lives, temp_lives)
            temp_score = new_score
            new_score, condition, lives = Level_1.game_loop(highscore, lives)
            if new_score > highscore:
                file = open("Highscore.txt", "w")
                file.write(str(new_score))
                file.close()
            if condition == "Complete":
                play = level_complete_screen(level)
                lives += 1
                redo = False
            if condition == "Death":
                if lives > 0:
                    play = life_lost()
                    redo = True
                    new_score = temp_score
                else:
                    play = death_screen()
                    redo = False
            
        #LEVEL 2
        if condition == "Complete":
            redo = True
            temp_lives = lives
            level = 2
            while redo == True:
                Level_2_intro.loop(lives, temp_lives)
                temp_score = new_score
                new_score, condition, lives = Level_2.game_loop(new_score, highscore, lives)
                if new_score > highscore:
                    file = open("Highscore.txt", "w")
                    file.write(str(new_score))
                    file.close()
                if condition == "Complete":
                    play = level_complete_screen(level)
                    lives += 1
                    redo = False
                if condition == "Death":
                    if lives > 0:
                        play = life_lost()
                        redo = True
                        new_score = temp_score
                    else:
                        play = death_screen()
                        redo = False

        #END
        if condition == "Complete" or condition == "Death":
            ending = game_end(new_score)
        
if __name__== "__main__":
    main()
