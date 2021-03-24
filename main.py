import pygame
import random
import threading
#import thread
import sys
import time

pygame.init()
screen = pygame.display.set_mode((400, 300))
done = False
is_blue = True
entityList = []
x = 30
y = 30

clock = pygame.time.Clock()
class Entity():

     def __init__(self, x, y):
         self.x = x
         self.y = y

     def getX(self):
         return self.x

     def getY(self):
         return self.y

     def drawStuff(entityList):
     #   pygame.draw.rect(screen, (255, 100, 0), pygame.Rect(55, 45, 10, 10))
         for x in range (0, entityList.__len__()):
             pygame.draw.rect(screen, (255, 100, 0), pygame.Rect(entityList[x].getX(),     entityList[x].getY(), 10, 10))
         pygame.display.flip()
         clock.tick(60)


class EntityManager(threading.Thread):

     def __init__(self):
         threading.Thread.__init__(self)

     def run(self):
         while True:
             entityList = generateEntities()
             drawStuff(entityList)

     def endJob(self):
         #thread.exit()
         time.sleep(2)


def detect_collision(x,y):
    if x > 340:
       x -= 1
    if y > 240:
       y -= 1
    if y < 0:
       y += 1
    if x < 0:
       x += 1
    return x,y

def generateEntities():
    itemlist = []
    for x in range (0,4):
        x = random.randint(1,339)
        y = random.randint(1,239)
        entity = Entity(x,y)
        itemlist.append(entity)
    return itemlist

entityList = generateEntities()
a = EntityManager()
a.setDaemon(True)
a.start()

while not done:

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    done = True
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    is_blue = not is_blue

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:
        y -= 1
        x,y = detect_collision(x, y)
    if pressed[pygame.K_DOWN]:
        y += 1
        x,y = detect_collision(x, y)
    if pressed[pygame.K_LEFT]:
        x -= 1
        x,y = detect_collision(x, y)
    if pressed[pygame.K_RIGHT]:
        x += 1
        x,y = detect_collision(x, y)

    screen.fill((0, 0, 0))
    if is_blue: color = (0, 128, 255)
    else: color = (255, 100, 0)
    pygame.draw.rect(screen, color, pygame.Rect(x, y, 60, 60))
    pygame.display.flip()
    clock.tick(60)