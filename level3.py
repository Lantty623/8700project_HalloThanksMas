import random
import tkinter as tk
import pygame
from PIL import Image, ImageTk

import cfg

def start_level3(root, level_selection_screen):
    # Clear the current window
    for widget in root.winfo_children():
        widget.destroy()

    # Display Christmas level-specific UI
    tk.Label(root, text="Christmas Level", font=("Arial", 24, "bold")).pack(pady=50)

    # Load the return icon image
    try:
        return_img = Image.open("assets/images/return_icon.png")
        return_img = return_img.resize((80, 80), Image.LANCZOS)  # Resize as needed
        return_icon = ImageTk.PhotoImage(return_img)

        # Create a label with the return icon, positioned in the top-left corner
        return_label = tk.Label(root, image=return_icon, bg=root["bg"])
        return_label.image = return_icon  # Keep a reference to avoid garbage collection
        return_label.place(x=10, y=10)  # Position in the top-left corner

        # Bind a click event to the label to act like a button
        return_label.bind("<Button-1>", lambda e: level_selection_screen())

    except Exception as e:
        print("Return icon not found:", e)

    # init game
    pygame.init()
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption("Christmas Game")
    clock = pygame.time.Clock()

    # Load images
    background_img = pygame.image.load("assets/images/christmas_background.png")
    background_img = pygame.transform.scale(background_img, cfg.SCREENSIZE)
    sleigh_img = pygame.image.load("assets/images/sleigh.png")
    custom_sleigh_size = (int(cfg.PLAYER_SIZE[0] * 1.5), int(cfg.PLAYER_SIZE[1] * 0.5))
    sleigh_img = pygame.transform.scale(sleigh_img, custom_sleigh_size)
    present_img = pygame.image.load("assets/images/present.png")
    present_img = pygame.transform.scale(present_img, cfg.CANDY_SIZE)
    santa_img = pygame.image.load("assets/images/santa.png")
    santa_img = pygame.transform.scale(santa_img, cfg.CANDY_SIZE)
    snowball_img = pygame.image.load("assets/images/snowball.png")
    snowball_img = pygame.transform.scale(snowball_img, cfg.CANDY_SIZE)
    snowman_img = pygame.image.load("assets/images/snowman.png")
    snowman_img = pygame.transform.scale(snowman_img, cfg.CANDY_SIZE)

    # player in middle bottom screen
    player = pygame.Rect(
        (cfg.SCREENSIZE[0] // 2 - cfg.PLAYER_SIZE[0] // 2,
        cfg.SCREENSIZE[1] - cfg.PLAYER_SIZE[1] -10),
        custom_sleigh_size
    )

    candies = []

    score = 0
    font = pygame.font.SysFont(None, 36)
    candy_speed = cfg.CANDY_SPEED

    # game main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move_ip(-cfg.PLAYER_SPEED, 0)
        if keys[pygame.K_RIGHT]:
            player.move_ip(cfg.PLAYER_SPEED, 0)

        # Ensure the player stays within screen bounds
        if player.left < 0:
            player.left = 0
        if player.right > cfg.SCREENSIZE[0]:
            player.right = cfg.SCREENSIZE[0]

        # random candy drop with further increased frequency
        ranNum = random.randint(1, 10)
        if ranNum == 1:
            candy_x = random.randint(0, cfg.SCREENSIZE[0] - cfg.CANDY_SIZE[0])
            new_candy = pygame.Rect(candy_x, 0, *cfg.CANDY_SIZE)
            candy_type = random.choice(["present", "santa", "snowball", "snowman"])
            candies.append((new_candy, candy_type))

        for c in list(candies):
            c[0].move_ip(0, candy_speed)  # further increased speed
            if c[0].colliderect(player):  # touch player
                candies.remove(c)
                if c[1] == "snowball":
                    score -= 1
                else:
                    score += 1
            elif c[0].top > cfg.SCREENSIZE[1]:  # out of screen
                candies.remove(c)

        # gradually increase candy speed
        candy_speed += 0.01

        # screen rendering
        screen.blit(background_img, (0, 0))
        screen.blit(sleigh_img, player.topleft)

        # display candies
        for c in candies:
            if c[1] == "present":
                screen.blit(present_img, c[0].topleft)
            elif c[1] == "santa":
                screen.blit(santa_img, c[0].topleft)
            elif c[1] == "snowball":
                screen.blit(snowball_img, c[0].topleft)
            elif c[1] == "snowman":
                screen.blit(snowman_img, c[0].topleft)

        # display score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        # update speed
        clock.tick(cfg.FPS)

    pygame.quit()