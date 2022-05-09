import pygame
from pygame.locals import *
from HealthBar import HealthBar

vec = pygame.math.Vector2



class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Images/RunIdleRight.png")
        self.rect = pygame.Rect(x, y, 35, 50)

        # Player Info
        self.pos = vec(x, y)
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)
        self.healthBar = HealthBar(10, 10)

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
        self.hit_cooldown = False

        # Player Events
        self.hit_cooldown_event = pygame.USEREVENT + 1

        
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

        if self.pos.x > 800:
            self.pos.x = 0
        elif self.pos.x < -30:
            self.pos.x = 800

        self.rect.topleft = self.pos
        self.rect.x += 32


    def walking(self):
        if self.move_frame > 6:
            self.move_frame = 0
            return

        if self.jumping == False and self.running == True:
            if self.vel.x >= 0:
                self.image = self.animation_right[self.move_frame]
                self.direction = "RIGHT"
            elif self.vel.x < 0:
                self.image = self.animation_left[self.move_frame]
                self.direction = "LEFT"
            self.move_frame += 1

        if self.running == False and self.move_frame != 0:
            self.move_frame = 0
            if self.direction == "RIGHT":
                self.image = self.animation_right[self.move_frame]
            elif self.direction == "LEFT":
                self.image = self.animation_left[self.move_frame]

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
                self.image = self.attack_animation_right[self.attack_frame]
            elif self.direction == "LEFT":
                self.image = self.attack_animation_left[self.attack_frame]

            self.attack_counter += 1
            if self.attack_counter >= 3:
                self.attack_frame += 1
                self.attack_counter = 0
        

    def update(self, group):
        self.walking()
        self.move()
        self.attack()
        self.collision(group)

    def player_hit(self, damage):
        if self.hit_cooldown == False:
            self.hit_cooldown = True
            self.healthBar.takeDamage(damage)
            pygame.time.set_timer(self.hit_cooldown_event, 1000)


    def collision(self, group):
        hits = pygame.sprite.spritecollide(self, group, False)

        if self.vel.y > 0:
            if hits:
                lowest = hits[0]

                if self.rect.bottom < lowest.rect.bottom:
                    self.pos.y = lowest.rect.top - self.rect.height
                    self.rect.y = lowest.rect.top - self.rect.height 
                    self.vel.y = 0
                    self.jumping = False
                    

    def jump(self):
        if self.jumping == False:
            self.jumping = True
            self.vel.y = -12

    def jump_cancel(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
        
    def render(self, display):
        #pygame.draw.rect(display, (255, 0, 0), self.rect)
        #pygame.draw.rect(display, (0, 255, 0), self.attack_range)
        display.blit(self.image, self.pos)
        self.healthBar.render(display)

    def load_animations(self):
        self.animation_right = [pygame.image.load("Images/RunIdleRight.png").convert_alpha(),
                   pygame.image.load("Images/run1right.png").convert_alpha(),
                   pygame.image.load("Images/run2right.png").convert_alpha(),
                   pygame.image.load("Images/run3right.png").convert_alpha(),
                   pygame.image.load("Images/run4right.png").convert_alpha(),
                   pygame.image.load("Images/run5right.png").convert_alpha(),
                   pygame.image.load("Images/RunIdleRight.png").convert_alpha()]

        self.animation_left = [pygame.image.load("Images/RunIdleLeft.png").convert_alpha(),
                          pygame.image.load("Images/run1left.png").convert_alpha(),
                          pygame.image.load("Images/run2left.png").convert_alpha(),
                          pygame.image.load("Images/run3left.png").convert_alpha(),
                          pygame.image.load("Images/run4left.png").convert_alpha(),
                          pygame.image.load("Images/run5left.png").convert_alpha(),
                          pygame.image.load("Images/RunIdleLeft.png").convert_alpha()]

        self.attack_animation_right = [pygame.image.load("Images/RunIdleRight.png").convert_alpha(),
                                  pygame.image.load("Images/shotgun1R.png").convert_alpha(),
                                  pygame.image.load("Images/shotgun2R.png").convert_alpha(),
                                  pygame.image.load("Images/shotgun3R.png").convert_alpha(),
                                  pygame.image.load("Images/shotgun4R.png").convert_alpha(),
                                  pygame.image.load("Images/shotgun5R.png").convert_alpha(),
                                  pygame.image.load("Images/RunIdleRight.png").convert_alpha()]

        self.attack_animation_left = [pygame.image.load("Images/RunIdleLeft.png").convert_alpha(),
                                  pygame.image.load("Images/shotgun1L.png").convert_alpha(),
                                  pygame.image.load("Images/shotgun2L.png").convert_alpha(),
                                  pygame.image.load("Images/shotgun3L.png").convert_alpha(),
                                  pygame.image.load("Images/shotgun4L.png").convert_alpha(),
                                  pygame.image.load("Images/shotgun5L.png").convert_alpha(),
                                  pygame.image.load("Images/RunIdleLeft.png").convert_alpha()]
