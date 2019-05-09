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
		self.image = pygame.Surface((50, 30))
		self.image.fill(Black)
		self.rect = self.image.get_rect()
		self.rect.center = (Width / 2,Height / 2)
		self.rect.bottom = Height - 10
		self.speedx = 0
		self.accelx = 0.5
		self.bullet_button_hold = 0

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
		if keypress[pygame.K_k] == 1:
			self.bullet_button_hold += 10
			if len(bullet_sprites) >= bullet_limit:
				pass
			elif (self.bullet_button_hold % 200) == 0:
				bullet = Bullet(self.rect.centerx, self.rect.top)
				all_sprites.add(bullet)
				bullet_sprites.add(bullet)

	def fire(self):
		if len(bullet_sprites) >= bullet_limit:
			pass
		else:
			self.bullet_button_hold = 0
			bullet = Bullet(self.rect.centerx, self.rect.top)
			all_sprites.add(bullet)
			bullet_sprites.add(bullet)

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((5, 20))
		self.image.fill(Blue)
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.bottom = y

	def update(self):
		self.rect.y -= 5
		if self.rect.bottom == 0:
			self.kill()

class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((25, 25))
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

bullet_limit = 3
bullet_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

global enemies_spawned
enemies_spawned = 0
enemy_limit = 100
def enemySpawn():
	global enemies_spawned
	enemies_spawned += 1
	enemy = Enemy()
	if enemies_spawned <= enemy_limit:
		threading.Timer(0.3, enemySpawn).start()
		all_sprites.add(enemy)
		enemy_sprites.add(enemy)
enemySpawn()

running = True
while running:
	shot_hit = pygame.sprite.groupcollide(bullet_sprites, enemy_sprites, True, True)
	clock.tick(FPS)
	all_sprites.update()
	screen.fill(Green)
	all_sprites.draw(screen)
	pygame.display.flip()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_k:
				player.fire()
