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

#PT1 = platform()
P1 = Player()

all_sprites = pygame.sprite.Group()
#all_sprites.add(PT1)
all_sprites.add(P1)

while True:
 for event in pygame.event.get():
  if event.type == QUIT:
   pygame.quit()
   sys.exit()

 displaysurface.fill((0, 0, 0))

 for entity in all_sprites:
  displaysurface.blit(entity.image, )

 pygame.display.update()
 FramePerSec.tick(FPS)

