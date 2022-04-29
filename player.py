import pygame
from pygame.locals import *

vec = pygame.math.Vector2


animation_right = [pygame.image.load("Images/Player_Sprite_R.png"),
                   pygame.image.load("Images/Player_Sprite2_R.png"),
                   pygame.image.load("Images/Player_Sprite3_R.png"),
                   pygame.image.load("Images/Player_Sprite4_R.png"),
                   pygame.image.load("Images/Player_Sprite5_R.png"),
                   pygame.image.load("Images/Player_Sprite6_R.png"),
                   pygame.image.load("Images/Player_Sprite_R.png")]

animation_left = [pygame.image.load("Images/Player_Sprite_L.png"),
                  pygame.image.load("Images/Player_Sprite2_L.png"),
                  pygame.image.load("Images/Player_Sprite3_L.png"),
                  pygame.image.load("Images/Player_Sprite4_L.png"),
                  pygame.image.load("Images/Player_Sprite5_L.png"),
                  pygame.image.load("Images/Player_Sprite6_L.png"),
                  pygame.image.load("Images/Player_Sprite_L.png")]

attack_animation_right = [pygame.image.load("Images/Player_Sprite_R.png"),
                          pygame.image.load("Images/Player_Attack1_R.png"),
                          pygame.image.load("Images/Player_Attack2_R.png"),
                          pygame.image.load("Images/Player_Attack3_R.png"),
                          pygame.image.load("Images/Player_Attack4_R.png"),
                          pygame.image.load("Images/Player_Attack5_R.png"),
                          pygame.image.load("Images/Player_Sprite_R.png")]

attack_animation_left = [pygame.image.load("Images/Player_Sprite_L.png"),
                          pygame.image.load("Images/Player_Attack1_L.png"),
                          pygame.image.load("Images/Player_Attack2_L.png"),
                          pygame.image.load("Images/Player_Attack3_L.png"),
                          pygame.image.load("Images/Player_Attack4_L.png"),
                          pygame.image.load("Images/Player_Attack5_L.png"),
                          pygame.image.load("Images/Player_Sprite_L.png")]


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Images/Player_Sprite_R.png")
        self.rect = pygame.Rect(x, y, 35, 50)

        # Player Info
        self.pos = vec(x, y)
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)

        # Player Constants
        self.ACC = 0.4
        self.FRIC = -0.1

        # Player Movements
        self.jumping = False
        self.running = False
        self.direction = "RIGHT"
        self.move_frame = 0

        # Player Attacking
        self.attacking = False
        self.attack_frame = 0
        self.attack_counter = 0
        self.attack_range = pygame.Rect(0, 0, 0, 0)

        
    def move(self):
        self.acc = vec(0, 0.5)

        if abs(self.vel.x) > 0.3:
            self.running = True
        else:
            self.running = False

        keys = pygame.key.get_pressed()

        if keys[K_LEFT]:
            self.acc.x = -self.ACC
        if keys[K_RIGHT]:
            self.acc.x = self.ACC

        self.acc.x += self.vel.x * self.FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.topleft = self.pos
        self.rect.x += 32


    def walking(self):
        if self.move_frame > 6:
            self.move_frame = 0
            return

        if self.jumping == False and self.running == True:
            if self.vel.x >= 0:
                self.image = animation_right[self.move_frame]
                self.direction = "RIGHT"
            elif self.vel.x < 0:
                self.image = animation_left[self.move_frame]
                self.direction = "LEFT"
            self.move_frame += 1

        if self.running == False and self.move_frame != 0:
            self.move_frame = 0
            if self.direction == "RIGHT":
                self.image = animation_right[self.move_frame]
            elif self.direction == "LEFT":
                self.image = animation_left[self.move_frame]

    def attack(self):
        if self.attacking == True:
            if self.direction == "RIGHT":
                self.attack_range = pygame.Rect(self.rect.x + self.rect.width,self.pos.y, 30, self.rect.height)
            elif self.direction == "LEFT":
                self.attack_range = pygame.Rect(self.pos.x, self.pos.y, 30, self.rect.height)
            
            if self.attack_frame > 6:
                self.attack_frame = 0
                self.attacking = False
                self.attack_range = pygame.Rect(0, 0, 0, 0)
                return

            if self.direction == "RIGHT":
                self.image = attack_animation_right[self.attack_frame]
            elif self.direction == "LEFT":
                self.image = attack_animation_left[self.attack_frame]

            self.attack_counter += 1
            if self.attack_counter >= 2:
                self.attack_frame += 1
                self.attack_counter = 0
        

    def update(self, group):
        self.attack()
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
                    self.jumping = False
                    

    def jump(self):
        if self.jumping == False:
            self.jumping = True
            self.vel.y = -12
        


    def render(self, display):
        pygame.draw.rect(display, (255, 0, 0), self.rect)
        pygame.draw.rect(display, (0, 255, 0), self.attack_range)
        display.blit(self.image, self.pos)
