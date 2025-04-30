import pygame
from pathlib import Path
from pygame.examples.cursors import image
from pygame.examples.go_over_there import screen, running, clock
from pygame.examples.grid import Player
from pygame.examples.video import backgrounds


def main():
    pygame.init()

screenHigh=760
screenWidth=1000
playground=[screenWidth, screenHigh]
screen = pygame.display.set_mode((screenWidth,screenHigh))

running = True
fps=120
clock=pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

    pygame.display.update()
    dt=clock.tick(fps)

pygame.quit()


parent_path = Path(__file__).parents[1]
print(parent_path)
image_path = parent_path / 'res'
print(image_path)
icon_path = image_path / 'pngtree-air-force-fighter-cartoon-black-png-image_3979329.png'
print(icon_path)

pygame.display.set_caption("Game")
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(50,50,50)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background,(0,0))
    pygame.display.update()
    dt == clock.tick(fps)
pygame.quit()

fps = 120
movingScale = 600/fps

player = Player(playground=playground,sensitivity=movingScale)

while running:
    screen.blit(background,(0,0))

    player.update()
    screen.blit(player.image,player.xy)
    pygame.display.update()
    dt = clock.tick(fps)