import random
import tkinter as tk
import pygame
import time
from PIL import Image, ImageTk

import cfg

def start_level1(root, level_selection_screen):
    # Clear the current window
    for widget in root.winfo_children():
        widget.destroy()

    # Display Halloween level-specific UI
    tk.Label(root, text="Halloween Level", font=("Arial", 24, "bold")).pack(pady=50)

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
    pygame.display.set_caption("Halloween Game")
    clock = pygame.time.Clock()

    # Load images
    background_img = pygame.image.load("assets/images/halloween_background.png")
    background_img = pygame.transform.scale(background_img, cfg.SCREENSIZE)
    pumpkin_img = pygame.image.load("assets/images/pumpkin.png")
    pumpkin_img = pygame.transform.scale(pumpkin_img, cfg.PLAYER_SIZE)
    candy_img = pygame.image.load("assets/images/candy.png")
    candy_img = pygame.transform.scale(candy_img, cfg.CANDY_SIZE)
    ghost_img = pygame.image.load("assets/images/ghost.png")
    ghost_img = pygame.transform.scale(ghost_img, cfg.CANDY_SIZE)

    # player in middle bottom screen
    player = pygame.Rect(
        (cfg.SCREENSIZE[0] // 2 - cfg.PLAYER_SIZE[0] // 2,
        cfg.SCREENSIZE[1] - cfg.PLAYER_SIZE[1] -10),
        cfg.PLAYER_SIZE
    )

    candies = []

    score = 0
    font = pygame.font.SysFont(None, 36)

    # **Timer Initialization**
    start_time = time.time()  # Capture the start time


    # game main loop
    running = True
    while running:
        # Check for time elapsed
        elapsed_time = time.time() - start_time
        remaining_time = cfg.GAME_DURATION - elapsed_time

        # End game when time is up
        if remaining_time <= 0:
            running = False  # Exit the game loop to end the game

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

        # random candy drop
        ranNum = random.randint(1, 20)
        if ranNum == 1:
            candy_x = random.randint(0, cfg.SCREENSIZE[0] - cfg.CANDY_SIZE[0])
            new_candy = pygame.Rect(candy_x, 0, *cfg.CANDY_SIZE)
            candy_type = random.choice(["candy", "ghost"])
            # Ensure new candy does not overlap with existing candies
            if not any(new_candy.colliderect(c[0]) for c in candies):
                candies.append((new_candy, candy_type))

        for c in list(candies):
            c[0].move_ip(0, cfg.CANDY_SPEED)
            if c[0].colliderect(player):  # touch player
                candies.remove(c)
                score += 1
            elif c[0].top > cfg.SCREENSIZE[1]:  # out of screen
                candies.remove(c)

        # screen rendering
        screen.blit(background_img, (0, 0))
        screen.blit(pumpkin_img, player.topleft)

        # display candies
        for c in candies:
            if c[1] == "candy":
                screen.blit(candy_img, c[0].topleft)
            else:
                screen.blit(ghost_img, c[0].topleft)

        # Display score and remaining time
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        time_text = font.render(f"Time: {int(remaining_time)}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(time_text, (10, 50))

        pygame.display.flip()
        # update speed
        clock.tick(cfg.FPS)

    # End the game and return to the level selection screen
    show_final_score(root, score, level_selection_screen)    

    pygame.quit()

def show_final_score(root, score, level_selection_screen):
    # Clear screen and display final score
    for widget in root.winfo_children():
        widget.destroy()

    # Display final score message
    tk.Label(root, text=f"Game Over! Your Score: {score}", font=("Arial", 24, "bold")).pack(pady=50)

    # Display the return icon
    try:
        return_img = Image.open("assets/images/return_icon.png")
        return_img = return_img.resize((80, 80), Image.LANCZOS)  # Resize if needed
        return_icon = ImageTk.PhotoImage(return_img)

        # Create a label with the return icon, placed in the center below the score
        return_label = tk.Label(root, image=return_icon)
        return_label.image = return_icon  # Keep a reference to avoid garbage collection
        return_label.pack(pady=20)  # Position below the score

        # Bind the click event to return to level selection
        return_label.bind("<Button-1>", lambda e: level_selection_screen())

    except Exception as e:
        print("Return icon not found:", e)