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
player_size = 80
enemies = [
    pygame.Rect(random.randrange(50, 950), random.randrange(50, 950), 50, 50),
    pygame.Rect(random.randrange(50, 950), random.randrange(50, 950), 50, 50),
    pygame.Rect(random.randrange(50, 950), random.randrange(50, 950), 50, 50)
]
# Name, HP, Damage, Speed, ATK Speed, Scale
enemy_stats = [
    ["Chaser", 40, 5, 6, 1],
    ["Shooter", 30, 6, 3, 1],
    ["Chaser", 40, 5, 6, 1],
]

wave = 0
kills = 0
font = pygame.font.SysFont("Papyrus", 40)

running = True
while running:
    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if (player_x - player_speed) <= 40:
            player_x =
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    if wave % 5 == 0 and wave % 10 != 0:
        code = True
        # Power ups will spawn
    if wave % 10 == 0:
        code = True
        # Boss will spawn

    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    for enemy in enemies[:]:
        if player_rect.colliderect(enemy):
            code = True
            # Add code for collision

    screen.fill((5, 0, 20))
    for enemy in enemies:
        pygame.draw.rect(screen, (110, 0, 0), enemy)
    pygame.draw.rect(screen, (255, 110, 0), (player_x, player_y, player_size, player_size))
    wave_text = font.render(f"Wave - {wave}", True, (255, 255, 255))
    screen.blit(wave_text, (10, 10))

    pygame.display.flip() # Can change to .update() if needed
pygame.quit()
