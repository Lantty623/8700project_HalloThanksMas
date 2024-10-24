import pygame
pygame.init()

# Initialize the game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("HalloThanksMas Game")

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Update game states here (score, level, etc.)

    # Render game elements here
    screen.fill((0, 0, 0))  # Fill the screen with black
    pygame.display.update()

pygame.quit()
