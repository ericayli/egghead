# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import pygame, sys
from pygame.locals import *
pygame.init()


HEIGHT = 500
WIDTH = 400


#FPS = 5
FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frequency Flasher")

class coloredSquare(pygame.sprite.Sprite):
    def __init__(self, color, width, xloc, yloc):
        super().__init__()
        self.surf = pygame.Surface((width, width))
        self.surf.fill(color)
        self.rect = self.surf.get_rect(center = (xloc, yloc))


class button(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc):
        super().__init__()
        self.surf = pygame.Surface((70, 30))
        self.surf.fill((0, 0, 255))
        self.rect = self.surf.get_rect(center= (xloc, yloc))

def mainScreen():
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)

    displaysurface.blit(text1, (180, 90))
    displaysurface.blit(text2, (180, 190))
    displaysurface.blit(text3, (180, 290))
    displaysurface.blit(text4, (175, 390))
    pygame.display.update()

def xHertz(x):
    displaysurface.blit(g1.surf, g1.rect)
    pygame.display.update()
    FramePerSec.tick(x)
    displaysurface.blit(b1.surf, b1.rect)
    pygame.display.update()
    FramePerSec.tick(x)


"""def doubleFlash(x, y):
    topOn = False
    botOn = False
    tickCounter = 0
    #both on screen
    displaysurface.blit(g2.surf, g2.rect)
    topOn = True
    displaysurface.blit(r1.surf, r1.rect)
    botOn = True
    finished = False
    pygame.display.update()

    while (finished == False):
        FramePerSec.tick(1)
        tickCounter = tickCounter + 1

        if (tickCounterfix this == 0):
            if (topOn == True):
                displaysurface.blit(b2.surf, b2.rect)
                topOn = False
            else:
                displaysurface.blit(g2.surf, g2.rect)
                topOn = True
        if (y%tickCounter == 0):
            if (botOn == True):
                displaysurface.blit(b3.surf, b3.rect)
                botOn = False
            else:
                displaysurface.blit(r1.surf, r1.rect)
                botOn = True
        pygame.display.update()
        if (x%tickCounter == 0 and y%tickCounter == 0):
            finished = True"""


def wipDouble(x):
    displaysurface.blit(g2.surf, g2.rect)
    displaysurface.blit(r1.surf, r1.rect)
    pygame.display.update()
    FramePerSec.tick(x)
    displaysurface.blit(b2.surf, b2.rect)
    pygame.display.update()
    FramePerSec.tick(x)

    displaysurface.blit(g2.surf, g2.rect)
    displaysurface.blit(b3.surf, b3.rect)
    pygame.display.update()
    FramePerSec.tick(x)
    displaysurface.blit(b2.surf, b2.rect)
    pygame.display.update()
    FramePerSec.tick(x)

def sepDouble(x, y):

    for i in range(10):
        displaysurface.blit(g2.surf, g2.rect)
        pygame.display.update()
        FramePerSec.tick(x)
        displaysurface.blit(b2.surf, b2.rect)
        pygame.display.update()
        FramePerSec.tick(x)
    for i in range(10):
        displaysurface.blit(r1.surf, r1.rect)
        pygame.display.update()
        FramePerSec.tick(y)
        displaysurface.blit(b3.surf, b3.rect)
        pygame.display.update()
        FramePerSec.tick(y)
















g1 = coloredSquare(pygame.Color('green'), 100, 200, 250)
b1 = coloredSquare(pygame.Color('black'), 100, 200, 250)
g2 = coloredSquare(pygame.Color('green'), 75, 200, 125)
b2 = coloredSquare(pygame.Color('black'), 75, 200, 125)
r1 = coloredSquare(pygame.Color('red'), 75, 200, 375)
b3 = coloredSquare(pygame.Color('black'), 75, 200, 375)



font = pygame.font.Font('freesansbold.ttf', 20)
button1 = button(200, 100)
button2 = button(200, 200)
button3 = button(200, 300)
button4 = button(200, 400)
text1 = font.render('XHZ', True, (255, 255, 255))
text2 = font.render('DHZ', True, (255, 255, 255))
text3 = font.render('SHZ', True, (255, 255, 255))
text4 = font.render('QUIT', True, (255, 255, 255))



all_sprites = pygame.sprite.Group()
all_sprites.add(button1)
all_sprites.add(button2)
all_sprites.add(button3)
all_sprites.add(button4)



mainScreen()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # if the mouse is clicked on the
            # button the game is terminated
            mouse = pygame.mouse.get_pos()
            if 165 <= mouse[0] <= 235 and 385 <= mouse[1] <= 415:
                pygame.quit()
                sys.exit()
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse = pygame.mouse.get_pos()
        if 165 <= mouse[0] <= 235 and 85 <= mouse[1] <= 115:
            displaysurface.fill((0, 0, 0))
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                xHertz(3)
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse = pygame.mouse.get_pos()
        if 165 <= mouse[0] <= 235 and 185 <= mouse[1] <= 215:
            displaysurface.fill((0, 0, 0))
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                wipDouble(5)
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse = pygame.mouse.get_pos()
        if 165 <= mouse[0] <= 235 and 285 <= mouse[1] <= 315:
            displaysurface.fill((0, 0, 0))
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                sepDouble(5, 1)















