import pygame
from sys import exit
import random

# Game states
GAME_RUNNING = 1
GAME_OVER = 2
GAME_WIN = 3

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load("Space shooter/space 1 setup/images/player.png").convert_alpha()
        self.rect = self.image.get_rect(center = (width/2, height/2 + 230))
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 200

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        laser_key = pygame.key.get_pressed()
        if laser_key[pygame.K_SPACE] and self.can_shoot == True:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center = (random.randint(0, width), random.randint(0, height)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(midbottom = pos)

    def update(self, dt):
        self.rect.centery -= 10
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups, speed):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed  # Speed of the meteor

    def update(self, dt):
        self.rect.centery += self.speed
        if self.rect.bottom > height:
            self.kill()

def collision():
    global running, score_value
    if pygame.sprite.spritecollide(player, meteor_sprites, False):
        return GAME_OVER  # Return game over state

    for laser in laser_sprites:
        if pygame.sprite.spritecollide(laser, meteor_sprites, True):
            laser.kill()
            explosion_sound.play()
            score_value += 1

    return GAME_RUNNING  # Return game running state

def score(score_value):
    score_surf = score_font.render(str(score_value), True, (240, 240, 240))
    score_rect = score_surf.get_rect(midbottom = (width / 2, height - 100))
    screen.blit(score_surf, score_rect)

pygame.init()
height = 700
width = 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('SPACE FIGHTER')
running = True
clock = pygame.time.Clock()

# general text on the losing screen when running = false
text_font = pygame.font.Font('Space shooter/space 1 setup/images/Oxanium-Bold.ttf', 30)
text_surf = text_font.render('YOU JUST LOST. PRESS SPACE TO PLAY AGAIN', False, 'white')
text_rect = text_surf.get_rect(center = (width / 2, height / 2))
win_text_surf = text_font.render('YOU WIN! PRESS SPACE TO PLAY AGAIN', False, 'green')
win_text_rect = win_text_surf.get_rect(center = (width / 2, height / 2))
score_font = pygame.font.Font('Space shooter/space 1 setup/images/Oxanium-Bold.ttf', 40)

# sound
explosion_sound = pygame.mixer.Sound("Space shooter/space 1 setup/audio/explosion.wav")
game_music = pygame.mixer.Sound("Space shooter/space 1 setup/audio/space-station-247790.mp3")

# player setup and star setup
meteor_surf = pygame.image.load("Space shooter/space 1 setup/images/meteor.png").convert_alpha()
laser_surf = pygame.image.load("Space shooter/space 1 setup/images/laser.png").convert_alpha()
star_surface = pygame.image.load("Space shooter/space 1 setup/images/star.png").convert_alpha()

player_dir = 1
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

for i in range(20):
    Star(all_sprites, star_surface)
player = Player(all_sprites)

# timer for meteor event and meteors falling down
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

score_value = 0  # Initialize score
meteor_speed = 6  # Initial speed of meteors
game_state = GAME_RUNNING  # Initial game state

while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
            exit()

        if event.type == meteor_event and game_state == GAME_RUNNING:
            x, y = random.randint(0, width), random.randint(-200, -100)
            Meteor(meteor_surf, (x, y), (all_sprites, meteor_sprites), meteor_speed)

    # Game loop
    if game_state == GAME_RUNNING:
        screen.fill('black')
        all_sprites.update(dt)

        game_state = collision()  # Check for collisions (game over or running)

        # Check if score reaches a multiple of 10 to increase meteor speed
        if score_value % 10 == 0 and score_value > 0:
            meteor_speed = 6 + (score_value // 10)  # Increase meteor speed by 1 every 10 points

        # End the game if score reaches 70
        if score_value >= 10:
            game_state = GAME_WIN
            screen.fill('black')
            screen.blit(win_text_surf, win_text_rect)
            pygame.display.update()
            pygame.time.wait(2000)  # Wait for 2 seconds before exiting

        all_sprites.draw(screen)
        score(score_value)  # Display the current score

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            player.rect.x += player_dir * 4

        if keys[pygame.K_LEFT]:
            player.rect.x += player_dir * (-4)

        if keys[pygame.K_UP]:
            player.rect.y += player_dir * (-4)

        if keys[pygame.K_DOWN]:
            player.rect.y += player_dir * 4

        if keys[pygame.K_d]:
            player.rect.x += player_dir * 4

        if keys[pygame.K_a]:
            player.rect.x += player_dir * (-4)

        if keys[pygame.K_w]:
            player.rect.y += player_dir * (-4)

        if keys[pygame.K_s]:
            player.rect.y += player_dir * (4)

        if keys[pygame.K_q]:
            running = False
            exit()

    elif game_state == GAME_OVER:
        screen.fill('black')
        screen.blit(text_surf, text_rect)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            # Restart the game
            game_state = GAME_RUNNING
            score_value = 0  # Reset the score when restarting
            meteor_speed = 6  # Reset meteor speed
            for meteor in meteor_sprites:
                meteor.kill()

    elif game_state == GAME_WIN:
        screen.fill('black')
        screen.blit(win_text_surf, win_text_rect)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            # Restart the game
            game_state = GAME_RUNNING
            score_value = 0  # Reset the score when restarting
            meteor_speed = 6  # Reset meteor speed
            for meteor in meteor_sprites:
                meteor.kill()

    pygame.display.update()

