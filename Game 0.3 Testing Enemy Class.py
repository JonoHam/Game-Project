import pygame
import random

Width = 700
Height = 600
FPS = 60

pygame.init()
#pygame.mixer.init()
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)

class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((50,30))
		self.image.fill(Black)
		self.rect = self.image.get_rect()
		self.rect.center = (Width/2,Height/2)
		self.rect.bottom = Height - 10

	def update(self):
		keypress = pygame.key.get_pressed()
		if keypress[pygame.K_LEFT]:
			self.rect.x -= 8
		elif keypress[pygame.K_RIGHT]:
			self.rect.x += 8


class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((25,25))
		self.image.fill(Red)
		self.rect = self.image.get_rect()
		self.speed = 2

	def update(self):
		self.rect.x += self.speed
		if self.rect.x >= Width:
			self.rect.y += 25
			self.speed = -2
		elif self.rect.x <= 0:
			self.rect.y += 25
			self.speed = 2

all_sprites = pygame.sprite.Group()
player = Player()
enemy = Enemy()
all_sprites.add(player)
all_sprites.add(enemy)

running = True
while running:
	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	all_sprites.update()
	screen.fill(Green)
	all_sprites.draw(screen)
	pygame.display.flip()
