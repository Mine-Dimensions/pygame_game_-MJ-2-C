import pygame
import random

pygame.init()
WIDTH = 1000
HEIGHT = 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyGame")
clock = pygame.time.Clock()
FPS = 60

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
# Name, HP, Damage, Speed, ATK Speed
enemy_stats = [
    ["Chaser", 40, 5, 3, 1],
    ["Shooter", 30, 6, 1, 1],
    ["Chaser", 40, 5, 3, 1],
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

invince = 2000
last_hit = 0
def hit(dmg, x, y):
    now = pygame.time.get_ticks()
    if now - last_hit > invince:
        player_health -= int(dmg) # Fix this
        if player_x > x:
            player_x += 15
        if player_x < x:
            player_x -= 15
        if player_y > y:
            player_y += 15
        if player_y < y:
            player_y -= 15

running = True
while running:
    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if (player_x - player_speed) <= 50:
            player_x = 50
        else:
            player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        if (player_x + player_speed) >= WIDTH - 120:
            player_x = WIDTH - 120
        else:
            player_x += player_speed
    if keys[pygame.K_UP]:
        if (player_y - player_speed) <= 50:
            player_y = 50
        else:
            player_y -= player_speed
    if keys[pygame.K_DOWN]:
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
    now = pygame.time.get_ticks()
    for enemy in enemies[:]:
        if player_rect.colliderect(enemy):
            hit(enemy_stats[count][2], enemy.x, enemy.y)
            # Add code for collision
        if 5000 - now > 0:
            code = True # Do nothing
        elif enemy_stats[count][0] == "Chaser":
            if player_x > enemy.x:
                enemy.x += (enemies[count][3] / 10)
            elif player_x < enemy.x:
                enemy.x -= (enemies[count][3] / 10)
            if player_y > enemy.y:
                enemy.y += (enemies[count][3] / 10)
            elif player_y < enemy.y:
                enemy.y -= (enemies[count][3] / 10)
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
    for enemy in enemies:
        pygame.draw.rect(screen, (110, 0, 0), enemy)
    pygame.draw.rect(screen, (255, 110, 0), (player_x, player_y, player_size, player_size))
    wave_text = font.render(f"Wave - {wave}", True, (255, 255, 255))
    screen.blit(wave_text, (10, 10))
    kill_text = font.render(f"Kills - {kills}", True, (255, 255, 255))
    screen.blit(kill_text, (10, 80))
    hp_text = font.render(f"Health - {player_health} HP", True, (255, 0, 0))
    screen.blit(hp_text, (WIDTH - 350, 10))

    pygame.display.flip() # Can change to .update() if needed
pygame.quit()
