import pygame
import random

Width = 700
Height = 600
FPS = 60

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((Width,Height))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

White = (255,255,255)
Black = (0,0,0)
Red = (255,0,0)
Green = (0,255,0)
Blue = (0,0,255)

running = True
while running:
	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	screen.fill(Green)
	pygame.display.flip()
