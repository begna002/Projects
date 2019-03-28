#Copyright 2019, Moti Begna

import pygame
import random
from pygame.locals import *
import turtle

# initialize pygame
pygame.init()

# create the screen object
# here we pass it a size of 800x600
screen = pygame.display.set_mode((600, 600))

background = pygame.Surface(screen.get_size())
background.fill((0, 0, 0))
 
def text_objects(text, font):
    textSurface = font.render(text, True, (255, 255, 255))
    return textSurface, textSurface.get_rect()

def Start(scores, names):
    pause = True
    clock = pygame.time.Clock()
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')

    input_box1 = pygame.Rect(250, 150, 100, 50)
    color1 = color_inactive
    active1 = False

    input_box2 = pygame.Rect(225, 225, 150, 50)
    color2 = color_inactive
    active2 = False

    input_box3 = pygame.Rect(200, 300, 200, 50)
    color3 = color_inactive
    active3 = False

    while pause:
        for event in pygame.event.get():
            if input_box1.collidepoint(pygame.mouse.get_pos()):
                # Toggle the active variable.
                active1 = True
            else:
                active1 = False
            if input_box2.collidepoint(pygame.mouse.get_pos()):
                # Toggle the active variable.
                active2 = True
            else:
                active2 = False
            if input_box3.collidepoint(pygame.mouse.get_pos()):
                # Toggle the active variable.
                active3 = True
            else:
                active3 = False
            # Change the current color of the input box.
            color1 = color_active if active1 else color_inactive
            color2 = color_active if active2 else color_inactive
            color3 = color_active if active3 else color_inactive

            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box1.collidepoint(event.pos):
                    return 75
                if input_box2.collidepoint(event.pos):
                    return 50
                if input_box3.collidepoint(event.pos):
                    return 25

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pause = False
                    pygame.quit()
                    quit()

        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, color1, input_box1)
        pygame.draw.rect(screen, color2, input_box2)
        pygame.draw.rect(screen, color3, input_box3)


        largeText = pygame.font.SysFont('bebas neue', 115)
        TextSurf, TextRect = text_objects("SNAKE", largeText)
        TextRect.center = ((600/2), (100))
        screen.blit(TextSurf, TextRect)

        smallText = pygame.font.SysFont('bebas neue', 50)
        TextSurf2, TextRect2 = text_objects("Slow", smallText)
        TextRect2.center = ((600/2), (175))
        screen.blit(TextSurf2, TextRect2)

        TextSurf3, TextRect3 = text_objects("Average", smallText)
        TextRect3.center = ((600/2), (250))
        screen.blit(TextSurf3, TextRect3)

        TextSurf4, TextRect4 = text_objects("Ludicrous", smallText)
        TextRect4.center = ((600/2), (325))
        screen.blit(TextSurf4, TextRect4)

        
        TextSurf5, TextRect5 = text_objects("High Scores", smallText)
        TextRect5.center = ((600/2), (425))
        screen.blit(TextSurf5, TextRect5)
        
        smallText = pygame.font.SysFont('bebas neue', 25)
        TextSurf5, TextRect5 = text_objects("Slow:", smallText)
        TextRect5.center = ((100), (475))
        screen.blit(TextSurf5, TextRect5)

        TextSurf5, TextRect5 = text_objects(str(names[0])[0:3], smallText)
        TextRect5.center = ((50), (525))
        screen.blit(TextSurf5, TextRect5)

        TextSurf5, TextRect5 = text_objects(str(scores[0]), smallText)
        TextRect5.center = ((150), (525))
        screen.blit(TextSurf5, TextRect5)

        TextSurf5, TextRect5 = text_objects("Average: ", smallText)
        TextRect5.center = ((600/2), (475))
        screen.blit(TextSurf5, TextRect5)

        TextSurf5, TextRect5 = text_objects(str(names[1])[0:3], smallText)
        TextRect5.center = ((250), (525))
        screen.blit(TextSurf5, TextRect5)

        TextSurf5, TextRect5 = text_objects(str(scores[1]), smallText)
        TextRect5.center = ((350), (525))
        screen.blit(TextSurf5, TextRect5)
        
        TextSurf5, TextRect5 = text_objects("Ludicrous: ", smallText)
        TextRect5.center = ((500), (475))
        screen.blit(TextSurf5, TextRect5)

        TextSurf5, TextRect5 = text_objects(str(names[2])[0:3], smallText)
        TextRect5.center = ((450), (525))
        screen.blit(TextSurf5, TextRect5)

        TextSurf5, TextRect5 = text_objects(str(scores[2]), smallText)
        TextRect5.center = ((550), (525))
        screen.blit(TextSurf5, TextRect5)
        
        pygame.display.update()

def End(score):
    pause = True

    while pause:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pause = False
                    pygame.quit()
                    quit()
                if event.key == K_SPACE:
                    return True, score

        largeText = pygame.font.SysFont('bebas neue', 115)
        TextSurf, TextRect = text_objects("You Lost!", largeText)
        TextRect.center = ((600/2), (200))
        screen.blit(TextSurf, TextRect)

        smallText = pygame.font.SysFont('bebas neue', 50)
        TextSurf2, TextRect2 = text_objects("Score: " + str(score), smallText)
        TextRect2.center = ((600/2), (275))
        screen.blit(TextSurf2, TextRect2)

        TextSurf3, TextRect3 = text_objects("Press Space to Play Agian", smallText)
        TextRect3.center = ((600/2), (325))
        screen.blit(TextSurf3, TextRect3)
        pygame.display.update()

def new_HighScore():
    font = pygame.font.Font(None, 75)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(225, 250, 700, 60)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == KEYDOWN:
                if active:
                    if event.key == K_RETURN:
                        return text
                        text = ''
                    elif event.key == K_BACKSPACE:
                        text = text[:-1]
                    else:
                        if len(text) <= 2:
                            text += event.unicode

        screen.fill((0, 0, 0))

        largeText = pygame.font.SysFont('bebas neue', 75)
        TextSurf, TextRect = text_objects("Write You Initials!", largeText)
        TextRect.center = ((600/2), (200))
        screen.blit(TextSurf, TextRect)

        largeText = pygame.font.SysFont('bebas neue', 75)
        TextSurf, TextRect = text_objects("Enter When Done", largeText)
        TextRect.center = ((600/2), (360))
        screen.blit(TextSurf, TextRect)
        
        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        input_box.w = 130
        # Blit the text.
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)
                  

def loop(speed):
    snake_img = pygame.image.load('snake.png')
    food_img = []
    food_img.append(pygame.image.load('food1.png'))
    food_img.append(pygame.image.load('food2.png'))


    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super(Player, self).__init__()
            self.image = snake_img.convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.left = 0
            self.rect.bottom = 600
            self.direction = "right"
            self.prev_direction = ""
            self.prev_left = 0
            self.prev_bottom = 0
            self.movement = 0
            
        def update(self, pressed_keys):
            if pressed_keys[K_RIGHT] and self.direction != "left":
                self.prev_direction = self.direction
                self.direction = "right"
            if pressed_keys[K_LEFT]and self.direction != "right":
                self.prev_direction = self.direction
                self.direction = "left"
            if pressed_keys[K_UP]and self.direction != "down":
                self.prev_direction = self.direction
                self.direction = "up"
            if pressed_keys[K_DOWN]and self.direction != "up":
                self.prev_direction = self.direction
                self.direction = "down"

            if self.direction == "right" and self.movement == speed:
                self.prev_left = self.rect.left
                self.prev_bottom = self.rect.bottom
                self.rect.move_ip(30, 0)
                self.movement = 0
            if self.direction == "left" and self.movement == speed:
                self.prev_left = self.rect.left
                self.prev_bottom = self.rect.bottom
                self.rect.move_ip(-30, 0)
                self.movement = 0
            if self.direction == "up" and self.movement == speed:
                self.prev_left = self.rect.left
                self.prev_bottom = self.rect.bottom
                self.rect.move_ip(0, -30)
                self.movement = 0
            if self.direction == "down" and self.movement == speed:
                self.prev_left = self.rect.left
                self.prev_bottom = self.rect.bottom
                self.rect.move_ip(0, 30)
                self.movement = 0
            self.movement += 1

    class Addition(pygame.sprite.Sprite):
        def __init__(self, left, bottom, movement):
            super(Addition, self).__init__()
            self.image = snake_img.convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.left = left
            self.rect.bottom = bottom
            self.prev_left = 0
            self.prev_bottom = 0
            self.movement = movement
            self.prev_direction = ""
            
        def update(self, previous):
 
            if self.movement == speed:
                self.prev_direction = previous.prev_direction
                self.prev_left = self.rect.left
                self.prev_bottom = self.rect.bottom

                self.rect.left = previous.prev_left
                self.rect.bottom = previous.prev_bottom
                self.movement = 0
            self.movement += 1
            

        
    class Food(pygame.sprite.Sprite):
        def __init__(self, left, bottom):
            super(Food, self).__init__()
            self.image = food_img[0].convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.left = left
            self.rect.bottom = bottom
            self.move = 0

        def update(self):
            #movement animation
            if self.move % 50 == 0:
                ind = int(self.move / 50)
                self.image = food_img[ind].convert_alpha()
            if self.move == 1:
                self.image = food_img[0].convert_alpha()
            if self.move == 99:
                self.move = 0
            else:
                self.move += 1
                
            if self.rect.bottom >= 600:
                self.kill()

    def Scoreboard(score):
        font = pygame.font.SysFont('bebas neue', 25)
        text = font.render("Score: " + str(score), True, (255, 255, 255))
        screen.blit(text, (25, 25))
            


    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    new_addition = []
    addition = []
    new_additon_length = len(new_addition)
    has_added = False

    new_food = []
    food = []
    x_pos = random.randrange(0, 570, 30)
    y_pos = random.randrange(30, 570, 30)

    new_food.append(Food(x_pos, y_pos))
    food.append(pygame.sprite.Group())
    all_sprites.add(new_food[0])
    food[0].add(new_food[0])
    new_food_length = len(new_food)
    

    score = 0
    intro = True
    while intro:
        new_addition_length = len(new_addition)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()

        for i in range(new_food_length):
            if pygame.sprite.spritecollideany(player, food[i]):
                has_added = True

                new_food[i].rect.bottom = 1000

                x_pos = random.randrange(0, 570, 30)
                y_pos = random.randrange(30, 570, 30)

                for j in range(new_addition_length):
                    if x_pos == new_addition[j].rect.left and y_pos == new_addition[j].rect.bottom:
                        x_pos = random.randrange(0, 570, 30)
                        y_pos = random.randrange(30, 570, 30)

                new_food.append(Food(x_pos, y_pos))
                food.append(pygame.sprite.Group())
                all_sprites.add(new_food[i + 1])
                food[i + 1].add(new_food[i + 1])
                
                new_food_length = len(new_food)
                score += 50
                
                if new_addition_length == 0:
                    if player.direction == "right":
                        new_addition.append(Addition(player.rect.left - 30, player.rect.bottom, player.movement))
                        addition.append(pygame.sprite.Group())
                        all_sprites.add(new_addition[new_additon_length])
                        addition[new_addition_length].add(new_addition[new_addition_length])
                        
                    if player.direction == "left":
                        new_addition.append(Addition(player.rect.left + 30, player.rect.bottom, player.movement))
                        addition.append(pygame.sprite.Group())
                        all_sprites.add(new_addition[new_addition_length])
                        addition[new_addition_length].add(new_addition[new_addition_length])
                        
                    if player.direction == "up":
                        new_addition.append(Addition(player.rect.left, player.rect.bottom + 30, player.movement))
                        addition.append(pygame.sprite.Group())
                        all_sprites.add(new_addition[new_addition_length])
                        addition[new_addition_length].add(new_addition[new_addition_length])
                        
                    if player.direction == "down":
                        new_addition.append(Addition(player.rect.left, player.rect.bottom - 30, player.movement))
                        addition.append(pygame.sprite.Group())
                        all_sprites.add(new_addition[new_addition_length])
                        addition[new_addition_length].add(new_addition[new_addition_length])
                else:
                    i = new_addition_length - 1
                    if new_addition[i].prev_direction == "right":
                        new_addition.append(Addition(new_addition[i].rect.left - 30, new_addition[i].rect.bottom, new_addition[i].movement))
                        addition.append(pygame.sprite.Group())
                        all_sprites.add(new_addition[i + 1])
                        addition[i + 1].add(new_addition[i + 1])
                        
                    if new_addition[i].prev_direction == "left":
                        new_addition.append(Addition(new_addition[i].rect.left + 30, new_addition[i].rect.bottom, new_addition[i].movement))
                        addition.append(pygame.sprite.Group())
                        all_sprites.add(new_addition[i + 1])
                        addition[i + 1].add(new_addition[i + 1])
                        
                    if new_addition[i].prev_direction == "up":
                        new_addition.append(Addition(new_addition[i].rect.left, new_addition[i].rect.bottom + 30, new_addition[i].movement))
                        addition.append(pygame.sprite.Group())
                        all_sprites.add(new_addition[i + 1])
                        addition[i + 1].add(new_addition[i + 1])
                        
                    if new_addition[i].prev_direction == "down":
                        new_addition.append(Addition(new_addition[i].rect.left, new_addition[i].rect.bottom - 30, new_addition[i].movement))
                        addition.append(pygame.sprite.Group())
                        all_sprites.add(new_addition[i + 1])
                        addition[i + 1].add(new_addition[i + 1])

                new_addition_length = len(new_addition)
                


        for i in range(len(new_addition)):
            if pygame.sprite.spritecollideany(player, addition[i]):
                restart = End(score)
                return restart
                

        pressed_keys = pygame.key.get_pressed()
        screen.blit(background, (0, 0))

        player.update(pressed_keys)

        for i in range(new_food_length):
            food[i].update()

        if has_added == True:
            addition[0].update(player)
            for i in range(1, new_addition_length):
                addition[i].update(new_addition[i - 1])

        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)

        if player.rect.right > 600 or player.rect.bottom > 600 or player.rect.left < 0 or player.rect.top < 0:
            restart = End(score)
            return restart

        Scoreboard(score)

        pygame.display.update()


play = True
while play:
    file = open("highscore.txt", "r")
    scores = []
    names = []
    for i in range(3):
        names.append(str(file.readline()))
        scores.append(int(file.readline()))
    file.close()
    speed = Start(scores, names)
    play, new_score = loop(speed)

    if speed == 75:
        if scores[0] < new_score:
            name = new_HighScore()
            file = open("highscore.txt", "w")
            file.write(str(name) + '\n')
            file.write(str(new_score) + '\n')
            file.write(str(names[1]))
            file.write(str(scores[1]) + '\n')
            file.write(str(names[2]))
            file.write(str(scores[2]) + '\n')
            file.close()
    if speed == 50:
        if scores[1] < new_score:
            name = new_HighScore()
            file = open("highscore.txt", "w")
            file.write(str(names[0]))
            file.write(str(scores[0]) + '\n')
            file.write(str(name) + '\n')
            file.write(str(new_score) + '\n')
            file.write(str(names[2]))
            file.write(str(scores[2]) + '\n')
            file.close()
    if speed == 25:
        if scores[2] < new_score:
            name = new_HighScore()
            file = open("highscore.txt", "w")
            file.write(str(names[0]))
            file.write(str(scores[0]) + '\n')
            file.write(str(names[1]))
            file.write(str(scores[1]) + '\n')
            file.write(str(name) + '\n')
            file.write(str(new_score) + '\n')
            file.close()


        
    
