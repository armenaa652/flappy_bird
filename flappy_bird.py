import pygame
import random
import sys
from pygame.locals import *

WINDOWWIDTH = 600
WINDOWHEIGHT = 400

WHITE = (255, 255, 255)
GREEN = (80, 210, 90)
BLUE = (102, 153, 255)
BLACK = (0, 0, 0)

#GAP = 200
GAP = 150
PIPEWIDTH = 50

FRAMERATE = 60
GRAVITY = 0.2
THRUST = 0.4
COUNTS = 130
speed = 1

count = COUNTS
toppipes = []
bottompipes = []
score = 0
topScore = 0
counter = 0


def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey(font):
    windowSurface.fill(WHITE)
    drawText('Flappy Bird', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press spacebar to play.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                return

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, BLACK)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

pygame.init()

mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Flappy Bird')


iconImage = pygame.image.load('flappybird.png')
pygame.display.set_icon(iconImage)
birdImage = pygame.image.load('59537.png')
#birdImage = pygame.image.load('flappybird.png')

#birdImage = pygame.transform.scale(birdImage, (95, 58))
birdRect = birdImage.get_rect()
birdEllipse = (50, 140, 57, 57)
birdRect.topleft = (50, 140)

font = pygame.font.SysFont(None, 48)

waitForPlayerToPressKey(font)
while True:
    windowSurface.fill(BLUE)
    removed = True
    if birdRect.bottom < WINDOWHEIGHT + 7:
        speed += GRAVITY
    else:
        score = 0
        speed = 0
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_UP:
                for i in range(27):
                    if speed > -6 and birdRect.top > 0 - 7:
                        speed -= THRUST

    birdRect.top += speed
    if count == COUNTS:
        count = 0
        counter = 0
        randHeigthtTop = random.randint(0, WINDOWHEIGHT - GAP)
        randHeightBottom = randHeigthtTop + GAP
        top = pygame.Rect(WINDOWWIDTH, 0, PIPEWIDTH, randHeigthtTop)
        bottom = pygame.Rect(WINDOWWIDTH, randHeightBottom, PIPEWIDTH, WINDOWHEIGHT - randHeightBottom)
        toppipes.append(top)
        bottompipes.append(bottom)

    count += 1
    windowSurface.blit(birdImage, birdRect)

    while removed:
        for p in toppipes:
            if p.right < 0:
                toppipes.remove(p)
                removed = True
                break
            else:
                p.left -= 2
                pygame.draw.rect(windowSurface, GREEN, p)
                pygame.draw.rect(windowSurface, (0, 80, 0), p, 2)
                if birdRect.colliderect(p):
                    score = 0
                    counter += 1
                removed = False
    removed = True
    while removed:
        for p in bottompipes:
            if p.right < 0:
                bottompipes.remove(p)
                removed = True
                break
            else:
                p.left -= 2
                pygame.draw.rect(windowSurface, GREEN, p)
                pygame.draw.rect(windowSurface, (0,80,0), p,2)
                if birdRect.colliderect(p):
                    score = 0
                    counter += 1
                if birdRect.left > p.right and counter == 0:
                    score += 1
                    counter += 1
                removed = False

    if score > topScore:
        topScore = score

    drawText('Score: %s' % (score), font, windowSurface, 10, 0)
    drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)
    pygame.display.update()
    mainClock.tick(FRAMERATE)