import pygame, sys
from pygame.locals import *

pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional

HEIGHT = 450
WIDTH = 800
FPS = 60

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")


class Player(pygame.sprite.Sprite):
 def __init__(self):
  super().__init__()
  self.image = pygame.image.load('mr egg.png')
  self.pos = vec((340,240))

 def move(self):
  pressed_keys = pygame.key.get_pressed()
  if pressed_keys[K_DOWN]:
   self.pos.x = 440

class Box(pygame.sprite.Sprite):
 def __init__(self):
  super().__init__()
  self.image = pygame.image.load('box.png')
  self.pos = vec((315, 175))

class red_lever(pygame.sprite.Sprite):
 def __init__(self):
  super().__init__()
  self.image = pygame.image.load('red_lever.png')
  self.pos = vec((322, 187))

 def move(self):
  pressed_keys = pygame.key.get_pressed()
  if pressed_keys[K_DOWN]:
   self.pos.y = 237

class blue_lever(pygame.sprite.Sprite):
 def __init__(self):
  super().__init__()
  self.image = pygame.image.load('blue_lever.png')
  self.pos = vec((342, 172))

 def move(self):
  pressed_keys = pygame.key.get_pressed()
  if pressed_keys[K_RIGHT]:
   self.pos.x = 390


class rock(pygame.sprite.Sprite):
 def __init__(self):
  super().__init__()
  self.image = pygame.image.load('rock.png')
  self.pos = vec((392, 208))

 def move(self):
  pressed_keys = pygame.key.get_pressed()
  if pressed_keys[K_RIGHT]:
   self.pos.y = 254

class win(pygame.sprite.Sprite):
 def __init__(self):
  super().__init__()
  self.image = pygame.image.load('win.png')
  self.pos = vec((0,1000))

 def move(self):
  pressed_keys = pygame.key.get_pressed()
  if pressed_keys[K_DOWN]:
   self.pos.x = 350
   self.pos.y = 150

class lose(pygame.sprite.Sprite):
 def __init__(self):
  super().__init__()
  self.image = pygame.image.load('lose.png')
  self.pos = vec((0,1000))

 def move(self):
  pressed_keys = pygame.key.get_pressed()
  if pressed_keys[K_RIGHT]:
   self.pos.x = 350
   self.pos.y = 150


PT1 = Box()
P1 = Player()
R_L = red_lever()
B_L = blue_lever()
ROCK = rock()
WIN = win()
LOSE = lose()

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)
all_sprites.add(R_L)
all_sprites.add(B_L)
all_sprites.add(ROCK)
all_sprites.add(WIN)
all_sprites.add(LOSE)


while True:
 for event in pygame.event.get():
  if event.type == QUIT:
   pygame.quit()
   sys.exit()

 displaysurface.fill((0, 0, 0))

 B_L.move()
 R_L.move()
 ROCK.move()
 P1.move()
 WIN.move()
 LOSE.move()

 for entity in all_sprites:
  displaysurface.blit(entity.image, entity.pos)

 pygame.display.update()
 FramePerSec.tick(FPS)

