import pygame
import random
import threading

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
		self.speedx = 0
		self.accelx = 0.5

	def update(self):
		keypress = pygame.key.get_pressed()
		if keypress[pygame.K_LEFT]:
			self.speedx -= self.accelx
			self.rect.x += self.speedx
		elif keypress[pygame.K_RIGHT]:
			self.speedx +=	self.accelx
			self.rect.x += self.speedx
		if self.rect.left < 0:
			self.rect.left = 0
			self.speedx = 1
		elif self.rect.right > Width:
			self.rect.right = Width
			self.speedx = -1
		if keypress[pygame.K_LEFT] == 0 and keypress[pygame.K_RIGHT] == 0:
			if self.speedx < 0:
				self.speedx += self.accelx
				self.rect.x += self.speedx
			elif self.speedx > 0:
				self.speedx -= self.accelx
				self.rect.x += self.speedx

class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((25,25))
		self.image.fill(Red)
		self.rect = self.image.get_rect()
		self.rect.bottom = 0
		self.speedx = 0
		self.speedy = 0

	def update(self):
		self.rect.x += self.speedx
		if self.rect.right >= Width - 50:
			self.rect.y += 1
			self.speedx -= 0.1
		elif self.rect.left <= 0 + 50:
			self.rect.y += 1
			self.speedx += 0.1

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

global enemies_spawned
enemies_spawned = 0
enemy_limit = 1000
def enemySpawn():
	global enemies_spawned
	enemies_spawned += 1
	enemy = Enemy()
	if enemies_spawned <= enemy_limit:
		threading.Timer(0.05, enemySpawn).start()
		all_sprites.add(enemy)
enemySpawn()

running = True
while running:
	clock.tick(FPS)
	all_sprites.update()
	screen.fill(Green)
	all_sprites.draw(screen)
	pygame.display.flip()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			running = False
