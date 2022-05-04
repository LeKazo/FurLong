import pygame
from pygame.locals import *
import sys


from Ground import Ground
from player import Player
from enemy import Enemy
from UserInterface import UserInterface


# Begin Pygame
pygame.init()


WIDTH = 800
HEIGHT = 400
FPS = 60
CLOCK = pygame.time.Clock()


display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Furlong")

background = pygame.image.load("Images/Background.png")

ground = Ground(900, 120, -20, 320, "Images/Ground.png")
player = Player(200, 200)
player.load_animations()
E1 = Enemy()
UI = UserInterface()

ground2 = Ground(100, 20, 300, 200, "Images/Ground.png")
ground3 = Ground(120, 20, 100, 150, "Images/Ground.png")
ground4 = Ground(80, 20, 500, 100, "Images/Ground.png")


EnemyGroup = pygame.sprite.Group()
GroundGroup = pygame.sprite.Group()
GroundGroup.add(ground)
GroundGroup.add(ground2)
GroundGroup.add(ground3)
GroundGroup.add(ground4)


while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN:
            pass

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                player.jump()
            if event.key == K_RETURN:
                player.attacking = True
                player.attack()


    # Update Functions
    E1.move()
    E1.collision(GroundGroup)
    E1.player_collision(player)
    player.update(GroundGroup)
    UI.update(CLOCK.get_fps())


    # Render Functions
    display.blit(background, (0, 0))
    player.render(display)
    E1.render(display)
    UI.render(display)

    for grounds in GroundGroup:
        grounds.render(display)

    pygame.display.update()
    CLOCK.tick(FPS)
            















    
    

