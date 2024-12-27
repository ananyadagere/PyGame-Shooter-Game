import pygame 
from pygame import mixer
import os
import random
import csv
import button
import math

# Initialize Pygame
mixer.init()
pygame.init()

# Set up the game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooter")

# Set framerate
clock = pygame.time.Clock()
FPS = 60

# Define game variables
GRAVITY = 0.75
SCROLL_THRESH = 200
TILE_SIZE = 40
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 22
screen_scroll = 0
bg_scroll = 0
level = 1
start_game = False
MAX_LEVELS = 3
SCORE = 0
MUSIC_ON = True

# Define player action variables
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False

# Load music and sounds
pygame.mixer.music.load('audio/music2.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1,0.0,5000)
jump_fx = pygame.mixer.Sound('audio/jump.wav')
jump_fx.set_volume(0.5)
shot_fx = pygame.mixer.Sound('audio/shot.wav')
shot_fx.set_volume(0.5)
grenade_fx = pygame.mixer.Sound('audio/grenade.wav')
grenade_fx.set_volume(0.5)

# Load Images
# Button images
start_img = pygame.image.load('img/start_btn.jpg').convert_alpha()
exit_img = pygame.image.load('img/exit_btn.jpg').convert_alpha()
restart_img = pygame.image.load('img/restart_btn.jpg').convert_alpha()

start_img = pygame.transform.scale(start_img, (start_img.get_width() // 2, start_img.get_height() // 2))
exit_img = pygame.transform.scale(exit_img, (exit_img.get_width() // 2, exit_img.get_height() // 2))
restart_img = pygame.transform.scale(restart_img, (restart_img.get_width() // 5, restart_img.get_height() // 5))

# Background
pine1_img = pygame.image.load('img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()

#new buttons
settings_img = pygame.image.load('img/options_btn.jpg').convert_alpha()
settings_img = pygame.transform.scale(settings_img, (settings_img.get_width() // 2, settings_img.get_height() // 2))
shop_img = pygame.image.load('img/shop_btn.jpg').convert_alpha()
shop_img = pygame.transform.scale(shop_img, (shop_img.get_width() // 2, shop_img.get_height() // 2))
music_on_img = pygame.image.load('img/icons/music.png').convert_alpha()
music_off_img = pygame.image.load('img/icons/mute.png').convert_alpha()
resume_img = pygame.image.load('img/icons/play.png').convert_alpha()
pause_img = pygame.image.load('img/icons/pause.png').convert_alpha()
pause_img = pygame.transform.scale(pause_img, (pause_img.get_width() * 2, pause_img.get_height() * 2))


# Store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/Tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)
# Bullet
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
#grenade
grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()
#pick up boxes
heal_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha()
grenade_box_img = pygame.image.load('img/icons/grenade_box.png').convert_alpha()
coin_img = pygame.image.load('img/icons/coin.png').convert_alpha()
back_img = pygame.image.load('img/back.png').convert_alpha()

item_boxes = {
    'Health' : heal_box_img,
    'Ammo' : ammo_box_img,
    'Grenade': grenade_box_img
}

# Define colors
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0,255,0)
BLACK = (0,0,0)
PINK = (235,65,54)

# Define font
font = pygame.font.SysFont('Futura', 30)

def draw_text(text, font, text_col, x, y):
    img = font.render(text,True,text_col)
    screen.blit(img, (x,y))

# Function to draw the background
def draw_bg():
    screen.fill(BG)
    width = sky_img.get_width()
    for x in range(5):
        screen.blit(sky_img,((x*width) - bg_scroll * 0.5,0))
        screen.blit(mountain_img,((x*width)-bg_scroll * 0.6,SCREEN_HEIGHT - mountain_img.get_height() -300))
        screen.blit(pine1_img,((x*width)-bg_scroll*0.7,SCREEN_HEIGHT - pine1_img.get_height() -150))
        screen.blit(pine2_img,((x*width)-bg_scroll*0.8,SCREEN_HEIGHT - pine2_img.get_height()))

# Function to reset level
def reset_level():
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()
    coin_group.empty()

    # Create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)
    return data


class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, grenades):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.speed = speed
        self.ammo = ammo 
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.grenades = grenades
        self.health = 100
        self.max_health = self.health
        self.char_type = char_type
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        # Create AI specific variables
        self.move_counter = 0
        self.ideling = False
        self.ideling_counter = 0
        self.vision = pygame.Rect(0,0,150,20)

        # load all images for the players
        animation_types = ['Idle','Run','Jump','Death']

        # Load animations
        for animation in animation_types:
            #reset temporary list of images
            temp_list = []
            # Count number of files in the folder
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        # Reset movement variables
        screen_scroll = 0
        dx = 0
        dy = 0

        # Assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # Jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -12
            self.jump = False
            self.in_air = True

        # Apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Check for collision
        for tile in world.obstacle_list:
            # Check for collission in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                # If AI has hit a wall then make it turn around
                if self.char_type == 'enemy':
                    self.direction *= -1
                    self.move_counter = 0
            # Check for collision in y direction
            if tile[1].colliderect(self.rect.x , self.rect.y + dy, self.width, self.height):
                # Check if below the ground, i.e jumping 
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # Check if falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom  

        # Check for collision with water
        if pygame.sprite.spritecollide(self,water_group, False):
            self.health = 0
        # Check if fallen off the map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0
        #Check for collision with exit
        level_complete = False
        if pygame.sprite.spritecollide(self,exit_group, False):
            level_complete = True


        # Check if going off the edges of the screen
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

        # Update rectangle position
        self.rect.x += dx
        self.rect.y += dy
        
        # Update scroll based on player position
        if self.char_type == 'player':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE)- SCREEN_WIDTH) \
                or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete
    
    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0]) * self.direction, self.rect.centery, self.direction)
            bullet_group.add(bullet)
            # Reduce ammo
            self.ammo -= 1
            shot_fx.play()

    def AI(self):
        if self.alive and player.alive:
            if self.ideling == False and random.randint(1,200) == 1:
                self.update_action(0)
                self.ideling = True
                self.ideling_counter = 50
            # Check if the AI is near the player
            if self.vision.colliderect(player.rect):
                # Stop running and face the player
                self.update_action(0)
                # Shoot
                self.shoot()
            else:
                if self.ideling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left,ai_moving_right)
                    self.update_action(1)
                    self.move_counter += 1
                    # Update AI vision as the enemy moves
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.ideling_counter -= 1
                    if self.ideling_counter <= 0:
                        self.ideling = False
        #scroll
        self.rect.x += screen_scroll

    def update_animation(self):
        # Update animation
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # Check if the new action is different from the previous one
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)
            #if self.char_type == 'enemy':
            #   SCORE += 5

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self,data):
        self.level_length = len(data[0])
        # Iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <= 10:
                        water = Water(img,x*TILE_SIZE, y*TILE_SIZE)
                        water_group.add(water)
                    elif tile >= 11 and tile <= 14:
                        decoration = Decoration(img,x*TILE_SIZE, y*TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 15:
                        player = Soldier('player', x*TILE_SIZE, y*TILE_SIZE, 1.65, 5, 20, 5)
                        health_bar = HealthBar(10,10,player.health,player.health)
                    elif tile == 16:
                        enemy = Soldier('enemy',x*TILE_SIZE,y*TILE_SIZE,1.65,2,20,0)
                        enemy_group.add(enemy)
                    elif tile == 17: # Create ammo box
                        item_box = ItemBox('Ammo',x*TILE_SIZE, y*TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 18:
                        item_boxes3 = ItemBox('Grenade',x*TILE_SIZE,y*TILE_SIZE)
                        item_box_group.add(item_boxes3)
                    elif tile == 19:
                        item_boxes1 = ItemBox('Health',x*TILE_SIZE,y*TILE_SIZE)
                        item_box_group.add(item_boxes1)
                    elif tile == 20: # Create exit
                        exit = Exit(img,x*TILE_SIZE, y*TILE_SIZE)
                        exit_group.add(exit)
                    elif tile == 21:
                        coins = Coin((x*TILE_SIZE)+20,(y*TILE_SIZE)+10)
                        coin_group.add(coins)

        return player, health_bar

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0],tile[1])

class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll

class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))


    def update(self):
        self.rect.x += screen_scroll   
    
class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(coin_img, (coin_img.get_width() // 2, coin_img.get_height() // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.original_y = y
        self.bounce_offset = 0
        self.bounce_speed = 5
        self.bounce_amplitude = 5

    def update(self):
        self.rect.x += screen_scroll  # Make coins scroll with the background
        # Update bounce offset to create up-and-down motion
        self.bounce_offset += self.bounce_speed
        self.rect.y = self.original_y + math.sin(math.radians(self.bounce_offset)) * self.bounce_amplitude

    
class ItemBox(pygame.sprite.Sprite):
    def __init__(self,item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        # Scroll
        self.rect.x += screen_scroll
        # Check if the player has picked up the box
        if pygame.sprite.collide_rect(self,player):
            #Check what kind of box it was
            if self.item_type == "Health":
                player.health += 25
                if player.health >= player.max_health:
                    player.health = player.max_health
            elif self.item_type == "Ammo":
                player.ammo += 10
            elif self.item_type == "Grenade":
                player.grenades += 2
            # Delete the item box
            self.kill()

class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        # Update with new health 
        self.health = health
        # Calculate health ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x - 2,self.y - 2,154,24))
        pygame.draw.rect(screen, RED, (self.x,self.y,150,20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 *ratio, 20))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10 
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction

    def update(self):
        # Move bullet
        self.rect.x += (self.direction * self.speed) + screen_scroll
        # Check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        # Check for collision with level
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
        # Check collision with chatacters
        if pygame.sprite.spritecollide(player,bullet_group,False):
            if player.alive:
                player.health -= 5
                self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy,bullet_group,False):
                if enemy.alive:
                    enemy.health -= 25
                    print(enemy.health)
                    self.kill()

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction

    def update(self):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y

        # Check for collision with level
        for tile in world.obstacle_list:
            # Check collision with walls
            if tile[1].colliderect(self.rect.x+ dx, self.rect.y, self.width, self.height):
                self.direction *= -1  
                dx = self.direction * self.speed
            # Check for collision in y direction
            if tile[1].colliderect(self.rect.x , self.rect.y + dy, self.width, self.height):
                self.speed = 0
                # Check if below the ground, i.e throwing up
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # Check if falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom 
        
        #Update grenade position
        self.rect.x += dx + screen_scroll
        self.rect.y += dy

        #countdown timer
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            grenade_fx.play()
            explosion = Explosion(self.rect.x,self.rect.y, 0.5)
            explosion_group.add(explosion)
            #do damage to anyone that is nearby
            # I want to change this around adding multiple checks like 1 tile around is instant kill
            if(abs(self.rect.centerx - player.rect.centerx)) < TILE_SIZE * 1 and \
                abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 1:
                player.health -= 100
            elif(abs(self.rect.centerx - player.rect.centerx)) < TILE_SIZE * 2 and \
                abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.health -= 50
            elif(abs(self.rect.centerx - player.rect.centerx)) < TILE_SIZE * 5 and \
                abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 5:
                player.health -= 5
            
            for enemy in enemy_group:
                if(abs(self.rect.centerx - enemy.rect.centerx)) < TILE_SIZE * 1 and \
                abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 1:
                    enemy.health -= 100

                elif(abs(self.rect.centerx - enemy.rect.centerx)) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                    enemy.health -= 50

                elif(abs(self.rect.centerx - enemy.rect.centerx)) < TILE_SIZE * 5 and \
                    abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 5:
                    enemy.health -= 10
                    print(enemy.health)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y,scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1,6):
            img = pygame.image.load(f'img/explosion/exp{num}.png').convert_alpha()
            img = pygame.transform.scale(img,(int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter = 0

    def update(self):
        self.rect.x += screen_scroll
        EXPLOSION_SPEED = 4
        # Update explosion animation
        self.counter += 1
        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            #if animation is complete then delete the explosion
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]

class SettingsMenu:
    def __init__(self):
        self.width = 400
        self.height = 300
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = (SCREEN_HEIGHT - self.height) // 2
        
        # Scale the music button by 3x
        self.music_btn_img = pygame.transform.scale(music_on_img, (music_on_img.get_width() * 3, music_on_img.get_height() * 3))
        self.music_btn = button.Button(self.x + 50, self.y + 100, self.music_btn_img, 5)
        
        # Back button is commented out; remove if unnecessary
        self.back_btn = button.Button(self.x + 150, self.y + 200, exit_img, 0.5)
        
    def draw(self, screen):
        # Draw fully black overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))  # Fully black
        overlay.set_alpha(255)  # Fully opaque
        screen.blit(overlay, (0, 0))
        
        # Draw settings panel
        pygame.draw.rect(screen, (70, 70, 70), (self.x, self.y, self.width, self.height))
        draw_text('Settings', font, WHITE, self.x + 150, self.y + 20)
        
        # Handle music button
        global MUSIC_ON
        if self.music_btn.draw(screen):
            MUSIC_ON = not MUSIC_ON
            if MUSIC_ON:
                pygame.mixer.music.play(-1, 0.0, 5000)
            else:
                pygame.mixer.music.stop()
        
        # Update music button image based on state
        self.music_btn.image = music_on_img if MUSIC_ON else music_off_img

    def handle_event(self, event):
        # Handle key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                # Return to the menu instead of exiting the game
                return "menu"
        return None

class PauseMenu:
    def __init__(self):
        self.width = 400
        self.height = 400
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = (SCREEN_HEIGHT - self.height) // 2
        self.resume_btn = button.Button(self.x + 100, self.y + 300, resume_img, 5)
        self.settings_btn = button.Button(self.x + 100, self.y + 100, settings_img, 0.8)
        self.quit_btn = button.Button(self.x + 100, self.y + 200, exit_img, 0.8)
        
    def draw(self, screen):
        # Draw semi-transparent background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))
        
        # Draw pause panel
        pygame.draw.rect(screen, (70, 70, 70), (self.x, self.y, self.width, self.height))
        draw_text('Paused', font, WHITE, self.x + 150, self.y + 20)
        
        return (self.resume_btn.draw(screen), 
                self.settings_btn.draw(screen),
                self.quit_btn.draw(screen))

            
# Modify your ScreenFade class to handle multiple types of fades
class ScreenFade:
    def __init__(self, direction, colour, speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        
        if self.direction == 1:  # Whole screen fade
            pygame.draw.rect(screen, self.colour, 
                           (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, 
                           (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, 
                           (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.colour, 
                           (0, SCREEN_HEIGHT // 2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
        
        if self.direction == 2:  # Vertical screen fade down
            pygame.draw.rect(screen, self.colour, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
            
        if self.fade_counter >= SCREEN_WIDTH:
            fade_complete = True
            
        return fade_complete

  

# Create buttons
# Create sprite groups
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()




# Constants for gap
button_gap = 20  # Gap between buttons in pixels

# Calculate the horizontal center for all buttons
button_x = SCREEN_WIDTH // 2 - start_img.get_width() // 2

# Calculate vertical positions for each button
start_button_y = SCREEN_HEIGHT // 2 - (2 * start_img.get_height() + 1.5 * button_gap)
exit_button_y = start_button_y + start_img.get_height() + button_gap
settings_button_y = exit_button_y + exit_img.get_height() + button_gap
shop_button_y = settings_button_y + settings_img.get_height() + button_gap

# Create buttons
start_button = button.Button(button_x, start_button_y, start_img, 1)
exit_button = button.Button(button_x, exit_button_y, exit_img, 1)
settings_button = button.Button(button_x, settings_button_y, settings_img, 1)
shop_button = button.Button(button_x, shop_button_y, shop_img, 1)
pause_button = button.Button(750, 10, pause_img, 1)  # Place the pause button in the top-left corner
restart_button = button.Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 30, restart_img, 1)


# Create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
# Load in level data and create world
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y,tile in enumerate(row):
            world_data[x][y] = int(tile)
world = World()
player, health_bar = world.process_data(world_data)

# Create menu instances
settings_menu = SettingsMenu()
pause_menu = PauseMenu()

# Create screen fade effects
death_fade = ScreenFade(2, BLACK, 4)
level_fade = ScreenFade(1, BLACK, 4)
start_fade = ScreenFade(1, BLACK, 4)

# Game states
start_game = False
game_paused = False
current_menu = None


# Main game loop

# Initialize necessary components
#pause_img = pygame.transform.scale(pause_img, (pause_img.get_width() * 2, pause_img.get_height() * 2))
#pause_button = button.Button(10, 10, pause_img, 1)

pause_menu = PauseMenu()
settings_menu = SettingsMenu()
current_menu = None

run = True
game_paused = False
start_game = False

while run:
    clock.tick(FPS)
    
    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_q:
                grenade = True
            if (event.key == pygame.K_w or event.key == pygame.K_UP) and player.alive:
                player.jump = True
                jump_fx.play()
            if event.key == pygame.K_ESCAPE:
                if current_menu == settings_menu:
                    current_menu = None
                else:
                    game_paused = not game_paused

        # Keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False

    # Handle game logic
    if game_paused:
        # Draw pause menu
        resume, settings, quit = pause_menu.draw(screen)
        if resume:
            game_paused = False
        if settings:
            current_menu = settings_menu
        if quit:
            run = False
    else:
        if not start_game:
            # Draw main menu
            draw_bg()
            if start_button.draw(screen):
                start_game = True
                start_fade = ScreenFade(1, BLACK, 4)
            if exit_button.draw(screen):
                run = False
            if settings_button.draw(screen):
                current_menu = settings_menu
            if shop_button.draw(screen):
                pass

            # Draw settings menu if active
            if current_menu == settings_menu:
                if settings_menu.draw(screen):
                    current_menu = None
        else:
            if not game_paused and current_menu is None:
                # Update and draw the game
                draw_bg()
                if pause_button.draw(screen):
                    game_paused = True

                # Show player stats
                draw_text('AMMO: ', font, WHITE, 10, 35)
                for x in range(player.ammo):
                    screen.blit(bullet_img, (90 + (x * 10), 40))
                draw_text('GRENADES: ', font, WHITE, 10, 65)
                for x in range(player.grenades):
                    screen.blit(grenade_img, (135 + (x * 15), 65))
                health_bar.draw(player.health)
                draw_text(f'Coins: {SCORE}', font, WHITE, SCREEN_WIDTH - 150, 10)

                # Update and draw game entities
                world.draw()
                player.update()
                player.draw()

                # Check for coin collection
                for coin in coin_group:
                    if pygame.sprite.collide_rect(player, coin):
                        SCORE += 1
                        coin.kill()

                # Update and draw enemies
                for enemy in enemy_group:
                    enemy.AI()
                    enemy.update()
                    enemy.draw()

                # Update and draw other game elements
                bullet_group.update()
                grenade_group.update()
                explosion_group.update()
                item_box_group.update()
                decoration_group.update()
                water_group.update()
                exit_group.update()
                coin_group.update()

                bullet_group.draw(screen)
                grenade_group.draw(screen)
                explosion_group.draw(screen)
                item_box_group.draw(screen)
                decoration_group.draw(screen)
                water_group.draw(screen)
                exit_group.draw(screen)
                coin_group.draw(screen)

                # Player actions
                if player.alive:
                    if shoot:
                        player.shoot()
                    elif grenade and not grenade_thrown and player.grenades > 0:
                        grenade = Grenade(player.rect.centerx + 0.5 * player.rect.size[0] * player.direction,
                                          player.rect.top, player.direction)
                        grenade_group.add(grenade)
                        player.grenades -= 1
                        grenade_thrown = True

                    if player.in_air:
                        player.update_action(2)  # 2: jump
                    elif moving_left or moving_right:
                        player.update_action(1)  # 1: run
                    else:
                        player.update_action(0)  # 0: idle

                    screen_scroll, level_complete = player.move(moving_left, moving_right)
                    bg_scroll -= screen_scroll

                    if level_complete:
                        if level_fade.fade():
                            level += 1
                            bg_scroll = 0
                            world_data = reset_level()
                            if level <= MAX_LEVELS:
                                with open(f'level{level}_data.csv', newline='') as csvfile:
                                    reader = csv.reader(csvfile, delimiter=',')
                                    for x, row in enumerate(reader):
                                        for y, tile in enumerate(row):
                                            world_data[x][y] = int(tile)
                                world = World()
                                player, health_bar = world.process_data(world_data)
                                #level_fade = ScreenFade(1, BLACK, 4)
                else:
                    screen_scroll = 0
                    if death_fade.fade():
                        draw_text("YOU DIED", font, RED, SCREEN_WIDTH // 2 - 30, SCREEN_HEIGHT // 2 - 60)
                        if restart_button.draw(screen):
                            death_fade = ScreenFade(2, BLACK, 4)
                            bg_scroll = 0
                            world_data = reset_level()
                            with open(f'level{level}_data.csv', newline='') as csvfile:
                                reader = csv.reader(csvfile, delimiter=',')
                                for x, row in enumerate(reader):
                                    for y, tile in enumerate(row):
                                        world_data[x][y] = int(tile)
                            world = World()
                            player, health_bar = world.process_data(world_data)

            # Handle settings menu when opened from pause
            if current_menu == settings_menu:
                if settings_menu.draw(screen):
                    current_menu = None

    pygame.display.update()

pygame.quit()
