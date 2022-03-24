from tokenize import group
from matplotlib import animation
import pygame
from pygame.locals import *

vec = pygame.math.Vector2

animation_right = [pygame.image.load("Images/RunIdleRight.png"),   
                   pygame.image.load("Images/run1right.png"),
                   pygame.image.load("Images/run2right.png"),
                   pygame.image.load("Images/run3right.png"),
                   pygame.image.load("Images/run4right.png"),
                   pygame.image.load("Images/run5right.png"),
                   pygame.image.load("Images/RunIdleRight.png")]


animation_left = [pygame.image.load("Images/RunIdleLeft.png"),
                  pygame.image.load("Images/run1left.png"),
                  pygame.image.load("Images/run2left.png"),
                  pygame.image.load("Images/run3left.png"),
                  pygame.image.load("Images/run4left.png"),
                  pygame.image.load("Images/run5left.png"),
                  pygame.image.load("Images/RunIdleLeft.png")]


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load("Images/RunIdleRight.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        #player info
        self.pos = vec(x, y)
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)

        #player constants
        self.ACC = 0.4
        self.FRIC = -0.1

        #player movement
        self.jumping = False
        self.running = False
        self.direction = "RIGHT"
        self.move_frame = 0
        


    def move(self):

        self.acc = vec(0, 0.5)

        keys = pygame.key.get_pressed()

        if keys[K_LEFT]:
            self.acc.x = -self.ACC
        if keys[K_RIGHT]:
            self.acc.x = self.ACC

        self.acc.x += self.vel.x * self.FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.topleft = self.pos


    def walking(self):
        if self.move_frame > 6:
            self.move_frame = 0
            return
        if self.jump == False:
            if self.vel.x > 0:
                self.image = animation_right[self.move_frame]
                self.direction = "RIGHT"
            elif self.vel.x < 0:
                self.image =  animation_left[self.move_frame]
                self.direction = "LEFT"
            self.move += 1

    def update(self, group):
        self.walking()
        self.move()
        self.collision(group)

    def collision(self, group): 
        hits = pygame.sprite.spritecollide(self, group, False)

        if self.vel.y > 0:
            if hits:
                lowest = hits[0]

                if self.rect.bottom >= lowest.rect.top:
                   self.pos.y = lowest.rect.top - self.rect.height 
                   self.rect.y = lowest.rect.top - self.rect.height
                   self.vel.y = 0 

    def jump(self):
        self.vel.y = -15

    def render(self, display):
        display.blit(self.image, self.pos)

