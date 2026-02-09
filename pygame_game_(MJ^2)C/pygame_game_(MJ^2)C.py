import pygame
import random
import sys
import math

pygame.init()
WIDTH = 1000
HEIGHT = 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyGame")
clock = pygame.time.Clock()
FPS = 60
bullets = []

# Player Stats
player_health = 100
player_damage = 10
player_speed = 5
player_atk_spd = 0.75

player_x, player_y = 500, 500
player_size = 40
enemies = [
    pygame.Rect(random.randrange(50, 950), random.randrange(50, 950), 35, 35),
    pygame.Rect(random.randrange(50, 950), random.randrange(50, 950), 35, 35),
    pygame.Rect(random.randrange(50, 950), random.randrange(50, 950), 35, 35)
]
# Name - 0, HP - 1, Damage - 2, Speed - 3, ATK Speed - 4, Last time hit player - 5
enemy_stats = [
    ["Chaser", 40, 5, 2.5, 1, 0],
    ["Shooter", 30, 6, 1, 1, 0],
    ["Chaser", 40, 5, 2.5, 1, 0],
]

powerups = [
    pygame.Rect(200, 200, 50, 50),
    pygame.Rect(400, 200, 50, 50),
    pygame.Rect(600, 200, 50, 50),
    pygame.Rect(800, 200, 50, 50)
]

wave = 0
kills = 0
font = pygame.font.SysFont("Papyrus", 40)

class Bullet: # Bullets from the player and the shooter enemy type
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.speed = 10
        
        # Math gotten from Gemini
        angle = math.atan2(target_y - y, target_x - x)
        
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 0), (int(self.x), int(self.y)), 5)

invince = 500
last_hit = 0
def hit(dmg, x, y, enemy_i):
    global player_health, player_x, player_y, last_hit, invince # Searched up how to use the outside variables in the function

    now = pygame.time.get_ticks()
    if now - last_hit > invince:
        if player_health - int(dmg) <= 0:
            pygame.quit()
            sys.exit()
        else:
            player_health -= int(dmg)
            last_hit = now
            enemy_stats[enemy_i][5] = now
        if player_x > x:
            player_x += 15
        if player_x < x:
            player_x -= 15
        if player_y > y:
            player_y += 15
        if player_y < y:
            player_y -= 15
    else:
        if player_x > x:
            player_x += 5
        if player_x < x:
            player_x -= 5
        if player_y > y:
            player_y += 5
        if player_y < y:
            player_y -= 5

def new_wave():
    code = True
  
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            new_bullet = Bullet(player_x + player_size//2, player_y + player_size//2, mx, my)
            bullets.append(new_bullet)

    now = pygame.time.get_ticks()

    for bullet in bullets[:]:
        bullet.move()
        if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT:
            bullets.remove(bullet)

        # ^ Bullets from player ^

    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_w] and keys[pygame.K_d]) or (keys[pygame.K_w] and keys[pygame.K_a]) or (keys[pygame.K_s] and keys[pygame.K_d]) or (keys[pygame.K_s] and keys[pygame.K_a]):
        player_speed = player_speed / 1.75
        if keys[pygame.K_a]:
            if (player_x - player_speed) <= 50:
                player_x = 50
            else:
                player_x -= player_speed
        if keys[pygame.K_d]:
            if (player_x + player_speed) >= WIDTH - 120:
                player_x = WIDTH - 120
            else:
                player_x += player_speed
        if keys[pygame.K_w]:
            if (player_y - player_speed) <= 50:
                player_y = 50
            else:
                player_y -= player_speed
        if keys[pygame.K_s]:
            if (player_y + player_speed) >= WIDTH - 120:
                player_y = WIDTH - 120
            else:
                player_y += player_speed
        player_speed = player_speed * 1.75
    else:
        if keys[pygame.K_a]:
            if (player_x - player_speed) <= 50:
                player_x = 50
            else:
                player_x -= player_speed
        if keys[pygame.K_d]:
            if (player_x + player_speed) >= WIDTH - 120:
                player_x = WIDTH - 120
            else:
                player_x += player_speed
        if keys[pygame.K_w]:
            if (player_y - player_speed) <= 50:
                player_y = 50
            else:
                player_y -= player_speed
        if keys[pygame.K_s]:
            if (player_y + player_speed) >= WIDTH - 120:
                player_y = WIDTH - 120
            else:
                player_y += player_speed

    if wave % 5 == 0 and wave % 10 != 0:
        code = True
        # Power ups will spawn
        player_x = 500
        player_y = 500

        for powerup in powerups:
            pygame.draw.rect(screen, (0, 255, 0), powerup)


    if wave % 10 == 0:
        code = True
        # Boss will spawn

    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    count = 0
    for enemy in enemies[:]:
        can_move = (now - enemy_stats[count][5]) > invince
        if player_rect.colliderect(enemy):
            hit(enemy_stats[count][2], enemy.x, enemy.y, count)
        if 5000 - now > 0:
            code = True # Do nothing
        elif enemy_stats[count][0] == "Chaser" and can_move == True:
            if (player_x > enemy.x or player_x < enemy.x) and (player_y > enemy.y or player_y < enemy.y):
                enemy_stats[count][3] = enemy_stats[count][3] / 1.5
                if player_x > enemy.x:
                    enemy.x += enemy_stats[count][3]
                elif player_x < enemy.x:
                    enemy.x -= enemy_stats[count][3]
                if player_y > enemy.y:
                    enemy.y += enemy_stats[count][3]
                elif player_y < enemy.y:
                    enemy.y -= enemy_stats[count][3]
                enemy_stats[count][3] = enemy_stats[count][3] * 1.5
            else:
                if player_x > enemy.x:
                    enemy.x += enemy_stats[count][3]
                elif player_x < enemy.x:
                    enemy.x -= enemy_stats[count][3]
                if player_y > enemy.y:
                    enemy.y += enemy_stats[count][3]
                elif player_y < enemy.y:
                    enemy.y -= enemy_stats[count][3]
        for enemy2 in enemies[:]:
            if enemy.colliderect(enemy2):
                if enemy.x > enemy2.x:
                    enemy.x += 5
                elif enemy.x < enemy2.x:
                    enemy.x -= 5
                if enemy.y > enemy2.y:
                    enemy.y += 5
                elif enemy.y < enemy2.y:
                    enemy.y -= 5
        count += 1

    screen.fill((5, 0, 20))
    for bullet in bullets:
        bullet.draw(screen)

    count = 0
    for enemy in enemies:
        if enemy_stats[count][0] == "Chaser":
            pygame.draw.rect(screen, (110, 0, 0), enemy)
            count += 1
        elif enemy_stats[count][0] == "Shooter":
            pygame.draw.rect(screen, (110, 0, 62), enemy)
            count += 1
    pygame.draw.rect(screen, (255, 110, 0), (player_x, player_y, player_size, player_size))
    wave_text = font.render(f"Wave - {wave}", True, (255, 255, 255))
    screen.blit(wave_text, (10, 10))
    kill_text = font.render(f"Kills - {kills}", True, (255, 255, 255))
    screen.blit(kill_text, (10, 80))
    hp_text = font.render(f"Health - {player_health} HP", True, (255, 0, 0))
    screen.blit(hp_text, (WIDTH - 350, 10))

    pygame.display.flip() # Can change to .update() if needed
pygame.quit()
sys.exit()
