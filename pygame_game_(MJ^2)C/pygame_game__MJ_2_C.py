import pygame
pygame.init()
WIDTH = 1500
HEIGHT = 1500
screen = pygame.display.set_mode((WIDTH, 600))
pygame.display.set_caption("PyGame")
clock = pygame.time.Clock()
FPS = 60

running = True
while running:
    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    screen.fill((0, 0, 0))
    # Draw here
    pygame.display.flip() # Can change to .update() if needed
pygame.quit()