import pygame
import random
import sys
import math
import os

# OPTION C - Day 2
if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ASSET_DIR = os.path.join(BASE_DIR, "assets")
    MUSIC_PATH = os.path.join(ASSET_DIR, "showdown.mp3")

    # PATCH - if music not found handle error
    try:
        pygame.mixer.init()
        pygame.init()

        pygame.mixer.music.load(MUSIC_PATH)
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)
    except:
        code = True
    PLAYER_SPRITE_PATH = os.path.join(ASSET_DIR, "player.png")
    CHASER_SPRITE_PATH = os.path.join(ASSET_DIR, "chaser.png")
    SHOOTER_SPRITE_PATH = os.path.join(ASSET_DIR, "shooter.png")
    BOSS_SPRITE_PATH = os.path.join(ASSET_DIR, "boss.png")
    ATK_SPRITE_PATH = os.path.join(ASSET_DIR, "Bullet Attack Up.png")
    ATK_SPD_SPRITE_PATH = os.path.join(ASSET_DIR, "Bullet Speed Up.png")
    HP_SPRITE_PATH = os.path.join(ASSET_DIR, "Health-Up.png")
    SPD_SPRITE_PATH = os.path.join(ASSET_DIR, "Speed-Up.png")

    WIDTH = 1000
    HEIGHT = 1000
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PyGame")
    clock = pygame.time.Clock()
    FPS = 60
    bullets = []
    enemy_bullets = []
    sprites = True

    # Player Stats
    player_health = 100
    player_damage = 10
    player_speed = 5
    player_atk_spd = 500

    player_x, player_y = 500, 500
    player_size = 40

    last_shot = 0

    # Enemy type definitions as dictionaries
    chaser  = {"size": 35, "hp": 40,  "damage": 5,  "speed": 2.5, "atk_spd": 1}
    shooter = {"size": 35, "hp": 30,  "damage": 6,  "speed": 1,   "atk_spd": 1}
    boss    = {"size": 90, "hp": 300, "damage": 15, "speed": 0,   "atk_spd": 10}
    summon  = {"size": 35, "hp": 40,  "damage": 5,  "speed": 2,   "atk_spd": 1}

    enemies = [
        pygame.Rect(random.randrange(50, 950), random.randrange(50, 950), 35, 35),
        pygame.Rect(random.randrange(50, 950), random.randrange(50, 950), 35, 35),
        pygame.Rect(random.randrange(50, 950), random.randrange(50, 950), 35, 35)
    ]

    # OPTION C - Day 1
    enemy_stats = [
        {"name": "Chaser",  "hp": 40, "damage": 5, "speed": 2.5, "atk_spd": 1, "last_hit": 0, "last_shot": 0, "last_summon": 0},
        {"name": "Shooter", "hp": 30, "damage": 6, "speed": 1,   "atk_spd": 1, "last_hit": 0, "last_shot": 0, "last_summon": 0},
        {"name": "Chaser",  "hp": 40, "damage": 5, "speed": 2.5, "atk_spd": 1, "last_hit": 0, "last_shot": 0, "last_summon": 0},
    ]

    powerups = []

    wave = 1
    kills = 0
    font = pygame.font.SysFont("Papyrus", 40)

    # PATCH - Catch Missing Sprites Error
    try:
        # Load sprites
        player_img  = pygame.image.load(PLAYER_SPRITE_PATH).convert_alpha()
        chaser_img  = pygame.image.load(CHASER_SPRITE_PATH).convert_alpha()
        shooter_img = pygame.image.load(SHOOTER_SPRITE_PATH).convert_alpha()
        boss_img    = pygame.image.load(BOSS_SPRITE_PATH).convert_alpha()
        summon_img  = pygame.image.load(CHASER_SPRITE_PATH).convert_alpha()
        atk_img     = pygame.image.load(ATK_SPRITE_PATH).convert_alpha()
        atk_spd_img = pygame.image.load(ATK_SPD_SPRITE_PATH).convert_alpha()
        hp_img      = pygame.image.load(HP_SPRITE_PATH).convert_alpha()
        spd_img     = pygame.image.load(SPD_SPRITE_PATH).convert_alpha()

        # Scale sprites
        player_img  = pygame.transform.scale(player_img,  (player_size,        player_size))
        chaser_img  = pygame.transform.scale(chaser_img,  (chaser["size"],     chaser["size"]))
        shooter_img = pygame.transform.scale(shooter_img, (shooter["size"],    shooter["size"]))
        boss_img    = pygame.transform.scale(boss_img,    (boss["size"],       boss["size"]))
        summon_img  = pygame.transform.scale(summon_img,  (summon["size"],     summon["size"]))
        atk_img     = pygame.transform.scale(atk_img,     (50, 50))
        atk_spd_img = pygame.transform.scale(atk_spd_img, (50, 50))
        hp_img      = pygame.transform.scale(hp_img,      (50, 50))
        spd_img     = pygame.transform.scale(spd_img,     (50, 50))
    except:
        sprites = False

    # OPTION C - Day 2
    class Bullet:  # Bullets from the player and the shooter enemy type
        def __init__(self, x, y, target_x, target_y):
            self.x = x
            self.y = y
            self.speed = 10

            # Math gotten from Gemini
            angle = math.atan2(target_y - y, target_x - x)

            self.dx = math.cos(angle) * self.speed
            self.dy = math.sin(angle) * self.speed

        def move(self):
            if self in enemy_bullets:
                self.x += self.dx / 2
                self.y += self.dy / 2
            else:
                self.x += self.dx
                self.y += self.dy

        def draw(self, surface):
            pygame.draw.circle(surface, (255, 255, 0), (int(self.x), int(self.y)), 5)

    class BossBullet:
        def __init__(self, x, y, target_x, target_y):
            self.x = x
            self.y = y
            self.speed = 1

            angle = math.atan2(target_y - y, target_x - x)
            self.dx = math.cos(angle) * self.speed
            self.dy = math.sin(angle) * self.speed

            self.radius = 200

        def move(self):
            self.x += self.dx
            self.y += self.dy

        def draw(self, surface):
            pygame.draw.circle(surface, (255, 120, 0), (int(self.x), int(self.y)), self.radius)

    invince = 500
    last_hit = 0
    def hit(dmg, x, y, enemy_i):
        global player_health, player_x, player_y, last_hit, invince, running  # Searched up how to use the outside variables in the function

        now = pygame.time.get_ticks()
        if now - last_hit > invince:
            if player_health - int(dmg) <= 0:
                running = False
            else:
                player_health -= int(dmg)
                last_hit = now
                if enemy_i != -1:
                    enemy_stats[enemy_i]["last_hit"] = now
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

    # OPTION C - Day 3 - Wave System
    def new_wave():
        global wave, enemies, powerups, player_x, player_y, chaser, shooter, enemy_stats, running
        wave += 1
        enemies = []
        bullets = []
        enemy_bullets = []
        enemy_count = 3
        if wave / 5 + 3 > 15:
            enemy_count = 15
        else:
            enemy_count += math.floor(wave / 5)
        if wave > 30:
            code = True
        if wave % 5 == 0 and wave % 30 != 0:
            # Power ups will spawn
            player_x = 500
            player_y = 500

            powerups = [
                pygame.Rect(200, 200, 50, 50),
                pygame.Rect(400, 200, 50, 50),
                pygame.Rect(600, 200, 50, 50),
                pygame.Rect(800, 200, 50, 50)
            ]
        elif wave % 30 == 0:
            enemies.append(pygame.Rect(455, 0, boss["size"], boss["size"]))
            enemy_stats.append({
                "name": "Boss", "hp": boss["hp"], "damage": boss["damage"],
                "speed": boss["speed"], "atk_spd": boss["atk_spd"],
                "last_hit": 0, "last_shot": 0, "last_summon": 0
            })
        elif wave == 31:
            powerups.append(pygame.Rect(200, 200, 50, 50))
        else:
            player_x = 500
            player_y = 100
            for x in range(enemy_count):
                rando = random.randrange(1, 100)
                if rando > 40:
                    enemies.append(pygame.Rect(random.randrange(50, 950), random.randrange(250, 950), chaser["size"], chaser["size"]))
                    enemy_stats.append({
                        "name": "Chaser", "hp": chaser["hp"], "damage": chaser["damage"],
                        "speed": chaser["speed"], "atk_spd": chaser["atk_spd"],
                        "last_hit": 0, "last_shot": 0, "last_summon": 0
                    })
                else:
                    enemies.append(pygame.Rect(random.randrange(50, 950), random.randrange(250, 950), shooter["size"], shooter["size"]))
                    enemy_stats.append({
                        "name": "Shooter", "hp": shooter["hp"], "damage": shooter["damage"],
                        "speed": shooter["speed"], "atk_spd": shooter["atk_spd"],
                        "last_hit": 0, "last_shot": 0, "last_summon": 0
                    })

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Can hit the minus button to enter a hard mode where your HP is one
            keys = pygame.key.get_pressed()
            if keys[pygame.K_MINUS]:
                player_health = 1

            if wave == 31:
                if keys[pygame.K_r]:
                    wave -= 1
                    running = False
                if keys[pygame.K_n]:
                    powerups = []

            # PATCH - Anti-Spam Cooldown
            if event.type == pygame.MOUSEBUTTONDOWN:
                now = pygame.time.get_ticks()
                if now - last_shot >= player_atk_spd:
                    if 3000 - now <= 0:
                        mx, my = pygame.mouse.get_pos()

                        new_bullet = Bullet(player_x + player_size // 2, player_y + player_size // 2, mx, my)
                        bullets.append(new_bullet)

                        last_shot = now

        now = pygame.time.get_ticks()

        # OPTION C - Day 3 - Object List
        for bullet in bullets[:]:
            bullet.move()

            bullet_rect = pygame.Rect(bullet.x - 5, bullet.y - 5, 10, 10)

            # OPTION C - Day 3 - Offscreen Delete
            # Remove bullet if off screen
            if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT:
                bullets.remove(bullet)
                continue

            # Check collision with enemies
            for i, enemy in enumerate(enemies[:]):
                if bullet_rect.colliderect(enemy):
                    enemy_stats[i]["hp"] -= player_damage  # Reduce enemy HP
                    bullets.remove(bullet)

                    if enemy_stats[i]["hp"] <= 0:
                        enemies.remove(enemy)
                        enemy_stats.pop(i)
                        kills += 1

                    break

            # ^ Bullets from player ^

        for bullet in enemy_bullets[:]:
            bullet.move()

            if isinstance(bullet, BossBullet):
                bullet_rect = pygame.Rect(
                    bullet.x - bullet.radius,
                    bullet.y - bullet.radius,
                    bullet.radius * 2,
                    bullet.radius * 2
                )
            else:
                bullet_rect = pygame.Rect(bullet.x - 5, bullet.y - 5, 10, 10)

            # Remove bullet if off screen
            if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT:
                enemy_bullets.remove(bullet)

            if isinstance(bullet, BossBullet) and bullet_rect.colliderect(player_rect):
                hit(boss["damage"], player_x, player_y, -1)
                enemy_bullets.remove(bullet)
            elif bullet_rect.colliderect(player_rect):
                hit(shooter["damage"], player_x, player_y, -1)
                enemy_bullets.remove(bullet)

            pygame.draw.circle(screen, (255, 0, 0), (int(bullet.x), int(bullet.y)), 5)


        dt = clock.tick(FPS) / 1000.0

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

        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        for i, enemy in enumerate(enemies):
            can_move = (now - enemy_stats[i]["last_hit"]) > invince

            if player_rect.colliderect(enemy):
                hit(enemy_stats[i]["damage"], enemy.x, enemy.y, i)

            if 3000 - now > 0:
                pass
            elif (enemy_stats[i]["name"] == "Chaser" or enemy_stats[i]["name"] == "Summon") and can_move:
                # Chaser movement ONLY
                if player_x > enemy.x:
                    enemy.x += enemy_stats[i]["speed"]
                elif player_x < enemy.x:
                    enemy.x -= enemy_stats[i]["speed"]

                if player_y > enemy.y:
                    enemy.y += enemy_stats[i]["speed"]
                elif player_y < enemy.y:
                    enemy.y -= enemy_stats[i]["speed"]
            elif enemy_stats[i]["name"] == "Shooter" and now - enemy_stats[i]["last_shot"] >= enemy_stats[i]["atk_spd"] * 1000:
                enemy_bullets.append(
                    Bullet(
                        enemy.centerx,
                        enemy.centery,
                        player_x + player_size // 2 + random.randrange(-100, 100),
                        player_y + player_size // 2 + random.randrange(-100, 100)
                    )
                )

                enemy_stats[i]["last_shot"] = now

                randx = random.randrange(-40, 40)
                randy = random.randrange(-40, 40)

                if enemy.x + randx <= 50:
                    enemy.x = 50
                elif enemy.x + randx >= WIDTH - 100:
                    enemy.x = WIDTH - 100
                else:
                    enemy.x += randx
                if enemy.y + randy <= 50:
                    enemy.y = 50
                elif enemy.y + randy >= WIDTH - 100:
                    enemy.y = WIDTH - 100
                else:
                    enemy.y += randy

            if enemy_stats[i]["name"] == "Boss" and now - enemy_stats[i]["last_shot"] >= 7000:
                boss_bullet = BossBullet(
                    enemy.centerx,
                    enemy.centery,
                    player_x + player_size // 2,
                    player_y + player_size // 2
                )
                enemy_bullets.append(boss_bullet)
                enemy_stats[i]["last_shot"] = now

            if enemy_stats[i]["name"] == "Boss" and now - enemy_stats[i]["last_summon"] >= 6000:
                enemies.append(pygame.Rect(370, 0, summon["size"], summon["size"]))
                enemy_stats.append({
                    "name": "Summon", "hp": summon["hp"], "damage": summon["damage"],
                    "speed": summon["speed"], "atk_spd": summon["atk_spd"],
                    "last_hit": 0, "last_shot": 0, "last_summon": 0
                })
                enemies.append(pygame.Rect(595, 0, summon["size"], summon["size"]))
                enemy_stats.append({
                    "name": "Summon", "hp": summon["hp"], "damage": summon["damage"],
                    "speed": summon["speed"], "atk_spd": summon["atk_spd"],
                    "last_hit": 0, "last_shot": 0, "last_summon": 0
                })
                enemies.append(pygame.Rect(482.5, 140, summon["size"], summon["size"]))
                enemy_stats.append({
                    "name": "Summon", "hp": summon["hp"], "damage": summon["damage"],
                    "speed": summon["speed"], "atk_spd": summon["atk_spd"],
                    "last_hit": 0, "last_shot": 0, "last_summon": 0
                })
                enemy_stats[i]["last_summon"] = now

            # Separate enemies slightly if overlapping
            for j, enemy2 in enumerate(enemies):
                if i != j and enemy.colliderect(enemy2):
                    if enemy.x > enemy2.x:
                        enemy.x += 5
                    elif enemy.x < enemy2.x:
                        enemy.x -= 5

                    if enemy.y > enemy2.y:
                        enemy.y += 5
                    elif enemy.y < enemy2.y:
                        enemy.y -= 5


        screen.fill((5, 0, 20))
        for bullet in bullets:
            bullet.draw(screen)
        for bullet in enemy_bullets:
            bullet.draw(screen)

        if len(enemies) <= 0 and len(powerups) <= 0:
            new_wave()
        else:
            for i, enemy in enumerate(enemies):
                # PATCH - If Sprites Missing Use Rectangles
                if sprites == True:
                    if enemy_stats[i]["name"] == "Chaser":
                        screen.blit(chaser_img, enemy.topleft)
                    elif enemy_stats[i]["name"] == "Shooter":
                        screen.blit(shooter_img, enemy.topleft)
                    elif enemy_stats[i]["name"] == "Boss":
                        screen.blit(boss_img, enemy.topleft)
                    elif enemy_stats[i]["name"] == "Summon":
                        screen.blit(summon_img, enemy.topleft)
                else:
                    if enemy_stats[i]["name"] == "Chaser":
                        pygame.draw.rect(screen, (255, 0, 0), enemy)
                    elif enemy_stats[i]["name"] == "Shooter":
                        pygame.draw.rect(screen, (0, 145, 255), enemy)
                    elif enemy_stats[i]["name"] == "Boss":
                        pygame.draw.rect(screen, (138, 138, 138), enemy)
                    elif enemy_stats[i]["name"] == "Summon":
                        pygame.draw.rect(screen, (255, 0, 0), enemy)

        count = 0
        if wave % 5 == 0 and wave % 30 != 0:
            for power in powerups:
                # PATCH - If Sprites Missing Use Rectangles
                if sprites == True:
                    if count == 0:
                        screen.blit(hp_img, (200, 200))
                    if count == 1:
                        screen.blit(atk_img, (400, 200))
                    if count == 2:
                        screen.blit(spd_img, (600, 200))
                    if count == 3:
                        screen.blit(atk_spd_img, (800, 200))
                else:
                    if count == 0:
                        pygame.draw.rect(screen, (0, 255, 0), power)
                    if count == 1:
                        pygame.draw.rect(screen, (255, 0, 0), power)
                    if count == 2:
                        pygame.draw.rect(screen, (0, 195, 255), power)
                    if count == 3:
                        pygame.draw.rect(screen, (255, 255, 0), power)
                if player_rect.colliderect(power):
                    if count == 0:
                        player_health += 50
                        powerups = []
                    if count == 1:
                        player_damage += 10
                        powerups = []
                    if count == 2:
                        player_speed += 2
                        powerups = []
                    if count == 3:
                        player_atk_spd -= 100
                        powerups = []
                count += 1

        # PATCH - If Sprite Missing Use Rectangles
        if sprites == True:
            screen.blit(player_img, (player_x, player_y))
        else:
            pygame.draw.rect(screen, (255, 150, 0), player_rect)
        wave_text = font.render(f"Wave - {wave}", True, (255, 255, 255))
        screen.blit(wave_text, (10, 10))
        kill_text = font.render(f"Kills - {kills}", True, (255, 255, 255))
        screen.blit(kill_text, (10, 80))
        hp_text = font.render(f"Health - {player_health} HP", True, (255, 0, 0))
        screen.blit(hp_text, (WIDTH - 350, 10))

        if now < 1000:
            font = pygame.font.SysFont("Papyrus", 150)
            count_text = font.render(f"Three...", True, (255, 255, 255))
            screen.blit(count_text, (200, 350))
            font = pygame.font.SysFont("Papyrus", 40)
        elif now >= 1000 and now < 2000:
            font = pygame.font.SysFont("Papyrus", 150)
            count_text = font.render(f"Two...", True, (255, 255, 255))
            screen.blit(count_text, (250, 350))
            font = pygame.font.SysFont("Papyrus", 40)
        elif now >= 2000 and now < 3000:
            font = pygame.font.SysFont("Papyrus", 150)
            count_text = font.render(f"One...", True, (255, 255, 255))
            screen.blit(count_text, (250, 350))
            font = pygame.font.SysFont("Papyrus", 40)
        elif now >= 3000 and now < 4000:
            font = pygame.font.SysFont("Papyrus", 150)
            count_text = font.render(f"Draw!", True, (255, 255, 255))
            screen.blit(count_text, (250, 350))
            font = pygame.font.SysFont("Papyrus", 40)

        if wave == 31:
            ask_text = font.render(f"End Run - (R)", True, (255, 255, 255))
            screen.blit(ask_text, (250, 350))
            aske_text = font.render(f"Go to Endless - (N)", True, (255, 255, 255))
            screen.blit(aske_text, (250, 550))

        # OPTION C - Day 3 - Draw Loop for all objects and UI elements
        pygame.display.flip()

    end_running = True
    while end_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_running = False

        screen.fill((0, 0, 0))

        font = pygame.font.SysFont("Papyrus", 100)
        wave_text = font.render(f"Final Wave - {wave}", True, (255, 255, 255))
        screen.blit(wave_text, (200, 350))

        kill_text = font.render(f"Total Kills - {kills}", True, (255, 255, 255))
        screen.blit(kill_text, (200, 500))

        pygame.display.flip()
    pygame.quit()
    sys.exit()
