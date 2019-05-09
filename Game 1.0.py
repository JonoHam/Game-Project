#importing libraries
import pygame
import random
import threading

#setting resolution and framerate
Width = 700
Height = 600
FPS = 60

#initialising pygame
pygame.init()
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

#setting colours
White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)
Purple = (139, 0, 139)

#adding player class
class Player(pygame.sprite.Sprite):
	#setting player class attributes
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

	#what the sprite will do *FPS* times per second
	def update(self):
		keypress = pygame.key.get_pressed()
		#if statement to see if "left arrow key" is held down
		if keypress[pygame.K_LEFT]:
			self.speedx -= self.accelx
			self.rect.x += self.speedx
		#if statement to see if "right arrow key" is held down
		elif keypress[pygame.K_RIGHT]:
			self.speedx +=	self.accelx
			self.rect.x += self.speedx
		#if statement to see if player sprite is at the left end of the resolution
		if self.rect.left < 0:
			self.rect.left = 0
			self.speedx = 1
		#if statement to see if player sprite is at the right end of the resolution
		elif self.rect.right > Width:
			self.rect.right = Width
			self.speedx = -1
		#if statement to see if player is not pressing movement keys
		if keypress[pygame.K_LEFT] == 0 and keypress[pygame.K_RIGHT] == 0:
			#if statement to check if player speed is less than 0
			if self.speedx < 0:
				self.speedx += self.accelx
				self.rect.x += self.speedx
			#if statement to check if player speed is more than 0
			elif self.speedx > 0:
				self.speedx -= self.accelx
				self.rect.x += self.speedx
		#if statement to check if key "k" is held down
		if keypress[pygame.K_k] == 1:
			self.bullet_button_hold += 10
			#if statement to see if the amount of bullet sprites exceeds the bullet limit
			if len(bullet_sprites) >= bullet_limit:
				pass
			#if statement to delay time between shots fired if key "k" is currently being held down
			elif (self.bullet_button_hold % 200) == 0:
				bullet = Bullet(self.rect.centerx, self.rect.top)
				all_sprites.add(bullet)
				bullet_sprites.add(bullet)

	#allows the player to shoot when key "k" is pressed
	def fire(self):
		#if statement to see if the amount of bullet sprites exceeds or equals the bullet limit
		if len(bullet_sprites) >= bullet_limit:
			pass
		else:
			#because the key "k" was pressed again instead of being held down the entire time, the button hold timer is reset to 0
			self.bullet_button_hold = 0
			bullet = Bullet(self.rect.centerx, self.rect.top)
			all_sprites.add(bullet)
			bullet_sprites.add(bullet)

#adding bullet class
class Bullet(pygame.sprite.Sprite):
	#setting bullet class attributes
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((5, 20))
		self.image.fill(Blue)
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.bottom = y

	#what the bullet will do *FPS* times per second
	def update(self):
		self.rect.y -= 5
		#if statement to check if the bullet sprite has left the screen
		if self.rect.bottom == 0:
			self.kill()

#adding enemy class
class Enemy(pygame.sprite.Sprite):
	#setting enemy class attributes
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((25, 25))
		self.image.fill(Red)
		self.rect = self.image.get_rect()
		self.rect.bottom = 0
		self.speedx = 0
		self.speedy = 0

	#what the enemy will do *FPS* times per second
	def update(self):
		self.rect.x += self.speedx
		#if statement to check if the right side of the sprite exceeds or equals the right side of the resolution -50
		if self.rect.right >= Width - 50:
			self.rect.y += 1
			self.speedx -= 0.1
		#if statement to check if the right side of the sprite exceeds or equals the left side of the resolution +50
		elif self.rect.left <= 0 + 50:
			self.rect.y += 1
			self.speedx += 0.1
		#if statement to check if the enemy has reached the player sprite's y-axis
		if self.rect.bottom >= Height - 40:
			pygame.quit()

#adding boss class
class Boss_enemy(pygame.sprite.Sprite):
	#setting enemy class attributes
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((100, 100))
		self.image.fill(Purple)
		self.rect = self.image.get_rect()
		self.rect.center = (Width / 2,Height / 2)
		self.rect.top = 10
		self.speedx = 0
		self.boss_move = False
		#these variables are reset / altered for the enemies that spawn from the boss
		global enemies_spawned
		global enemy_limit
		global enemies_killed
		enemies_spawned = 0
		enemy_limit = 15
		enemies_killed = 0
		enemySpawn()
	#what the Boss will do *FPS* times per second
	def update(self):
		self.rect.x += self.speedx
		if enemies_killed == enemy_limit and self.boss_move == False:
			self.boss_move = True
			self.speedx = 5
		#if statement to check if the right side of the sprite exceeds or equals the right side of the resolution -50
		if self.rect.right >= Width - 50:
			self.rect.y += 1
			self.speedx -= 0.2
		#if statement to check if the right side of the sprite exceeds or equals the left side of the resolution +50
		elif self.rect.left <= 0 + 50:
			self.rect.y += 1
			self.speedx += 0.2
		#if statement to check if the boss has reached the player sprite's y-axis
		if self.rect.bottom >= Height - 40:
			pygame.quit()
		#if statement to check if the boss has has been hit (x) times
		if times_hit_boss == 60:
			self.kill()

#adding enemy class
class Enemy_from_boss(pygame.sprite.Sprite):
	#setting enemy_from_boss class attributes
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((25, 25))
		self.image.fill(Red)
		self.rect = self.image.get_rect()
		self.rect.center = (Width / 2, Height / 2)
		self.rect.top = 10 + random.randrange(0, 60)
		self.speedx = random.randrange(-2, 1)
		if self.speedx < 0:
			self.speedx = -2.8
		elif self.speedx >= 0:
			self.speedx = 3.7
	#what the enemies from the boss will do *FPS* times per second
	def update(self):
		self.rect.x += self.speedx
		#if statement to check if the right side of the sprite exceeds or equals the right side of the resolution -50
		if self.rect.right >= Width - 50:
			self.rect.y += 2
			self.speedx -= 0.1
		#if statement to check if the right side of the sprite exceeds or equals the left side of the resolution +50
		elif self.rect.left <= 0 + 50:
			self.rect.y += 2
			self.speedx += 0.1
		#if statement to check if the enemies from the boss has reached the player sprite's y-axis
		if self.rect.bottom >= Height - 40:
			pygame.quit()

#limiter variables used within classes to stop the spawning of more sprites
bullet_limit = 3
global enemies_spawned
enemies_spawned = 0
global enemy_limit
enemy_limit = 30
global enemies_killed
enemies_killed = 0
times_hit_boss = 0
boss_spawned = False

#sprite groups to allow all sprites to update without calling each sprite and to allow hit detection
bullet_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
boss_sprite = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

#function to spawn a set enemies in at a set interval of time
def enemySpawn():
	global enemies_spawned
	#if statement to see if the boss has spawned in
	if boss_spawned == True:
		enemies_spawned += 1
		enemy = Enemy_from_boss()
		#if statement to check if the amount of enemies spawned is less than or equal to the enemy limit
		if enemies_spawned <= enemy_limit:
			threading.Timer(0.3, enemySpawn).start()
			all_sprites.add(enemy)
			enemy_sprites.add(enemy)
	else:
		enemies_spawned += 1
		enemy = Enemy()
		#if statement to check if the amount of enemies spawned is less than or equal to the enemy limit
		if enemies_spawned <= enemy_limit:
			threading.Timer(0.3, enemySpawn).start()
			all_sprites.add(enemy)
			enemy_sprites.add(enemy)
enemySpawn()

#loop to keep the game continuously running until told otherwise
running = True
while running:
	#checking if the bullet and enemy sprites are within another and deletes both if true
	shot_hit = pygame.sprite.groupcollide(bullet_sprites, enemy_sprites, True, True)
	#checks to see if shot_hit has occurred
	if shot_hit:
		enemies_killed += 1
	#checking if the bullet and boss sprites are within another and deletes the bullet if true
	boss_hit = pygame.sprite.groupcollide(bullet_sprites, boss_sprite, True, False)
	#checks to see if all enemies are killed and the boss hasn't spawned yet
	if enemies_killed == enemy_limit and boss_spawned == False:
		#stops multiple bosses spawning in
		boss_spawned = True
		boss = Boss_enemy()
		all_sprites.add(boss)
		boss_sprite.add(boss)
	#checks to see if boss_hit has occurred
	if boss_hit:
		times_hit_boss += 1
		#makes boss invincible if all enemies haven't been killed yet
		if enemies_killed != enemy_limit:
			times_hit_boss = 0
		#checks to see if the boss has been hit 45 times and stops rendering the boss if so
		if times_hit_boss == 45:
			boss_sprite.remove(boss)
			all_sprites.remove(boss)
	clock.tick(FPS)
	all_sprites.update()
	screen.fill(Green)
	all_sprites.draw(screen)
	boss_sprite.draw(screen)
	pygame.display.flip()
	#loop to check for each event declared in the pygame library
	for event in pygame.event.get():
		#if statement to check if the event was to close the tab
		if event.type == pygame.QUIT:
			pygame.quit()
			running = False
		#if statement to check if a key was pressed once
		elif event.type == pygame.KEYDOWN:
			#if statement to check if that key was "k"
			if event.key == pygame.K_k:
				player.fire()
