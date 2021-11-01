import pygame, sys
from pygame.locals import *
vec = pygame.math.Vector2  # 2 for two dimensional


pygame.init()

displaysurface = pygame.display.set_mode((1080, 800))
pygame.display.set_caption("Game")

font = pygame.font.SysFont(None, 20)

class screen(pygame.sprite.Sprite):
 def __init__(self):
  super().__init__()
  self.image = pygame.image.load('screen 1.png')
  self.pos = vec((45,150))

 def move(self):
  pressed_keys = pygame.key.get_pressed()
  if pressed_keys[K_LEFT]:
   self.pos.x = 1100
  if pressed_keys[K_RIGHT]:
   self.pos.x = 1100

class screen1_1(pygame.sprite.Sprite):
 def __init__(self):
  super().__init__()
  self.image = pygame.image.load('screen 1.1.png')
  self.pos = vec((4500,10))

 def move(self):
  pressed_keys = pygame.key.get_pressed()
  if pressed_keys[K_LEFT]:
   self.pos.x = 210

class screen2_1(pygame.sprite.Sprite):
 def __init__(self):
  super().__init__()
  self.image = pygame.image.load('screen 2.1.png')
  self.pos = vec((4500,10))

 def move(self):
  pressed_keys = pygame.key.get_pressed()
  if pressed_keys[K_RIGHT]:
   self.pos.x = 210


P1 = screen()
P2 = screen1_1()
P3 = screen2_1()
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(P2)
all_sprites.add(P3)

#background = pygame.image.load('bird escape.png')
while True:
 for event in pygame.event.get():
  if event.type == QUIT:
   pygame.quit()
   sys.exit()

 displaysurface.fill((0, 0, 0))
 #displaysurface.blit(background, (0, 0))

 P1.move()
 P2.move()
 P3.move()

 for entity in all_sprites:
  displaysurface.blit(entity.image, entity.pos)



 pygame.display.update()
