import random
import tkinter as tk
import pygame
import time
from PIL import Image, ImageTk
import cfg

def start_level3(root, level_selection_screen):
    # Clear the current window
    for widget in root.winfo_children():
        widget.destroy()

    # Initialize Pygame
    pygame.init()
    
    # Create a tkinter Canvas to hold the pygame surface
    game_canvas = tk.Canvas(root, width=cfg.SCREENSIZE[0], height=cfg.SCREENSIZE[1])
    game_canvas.pack()
    
    # Create a pygame Surface to render the game
    screen = pygame.Surface(cfg.SCREENSIZE)
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
        (cfg.SCREENSIZE[0] // 2 - custom_sleigh_size[0] // 2,
        cfg.SCREENSIZE[1] - custom_sleigh_size[1] - 10),
        custom_sleigh_size
    )

    candies = []
    score = 0
    font = pygame.font.SysFont(None, 36)

    # Timer initialization
    start_time = time.time()
    candy_speed = cfg.CANDY_SPEED * 2  # Starting speed for faster gameplay

    # Key state tracking for movement
    keys_pressed = {"left": False, "right": False}

    # Define functions to handle key events
    def on_key_press(event):
        if event.keysym == "Left":
            keys_pressed["left"] = True
        elif event.keysym == "Right":
            keys_pressed["right"] = True

    def on_key_release(event):
        if event.keysym == "Left":
            keys_pressed["left"] = False
        elif event.keysym == "Right":
            keys_pressed["right"] = False

    # Bind the key events to tkinter
    root.bind("<KeyPress>", on_key_press)
    root.bind("<KeyRelease>", on_key_release)

    # Game loop function
    def game_loop():
        nonlocal running, score, candy_speed

        # Check for time elapsed
        elapsed_time = time.time() - start_time
        remaining_time = cfg.GAME_DURATION - elapsed_time

        if remaining_time <= 0:
            running = False  # End the game if time is up

        # Handle player movement based on key presses
        if keys_pressed["left"]:
            player.move_ip(-cfg.PLAYER_SPEED, 0)
        if keys_pressed["right"]:
            player.move_ip(cfg.PLAYER_SPEED, 0)

        # Ensure the player stays within screen bounds
        player.clamp_ip(screen.get_rect())

        # Random item drop with increased frequency
        if random.randint(1, 10) == 1:
            candy_x = random.randint(0, cfg.SCREENSIZE[0] - cfg.CANDY_SIZE[0])
            new_candy = pygame.Rect(candy_x, 0, *cfg.CANDY_SIZE)
            candy_type = random.choice(["present", "santa", "snowball", "snowman"])
            candies.append((new_candy, candy_type))

        # Move candies and check for collision with player
        for c in list(candies):
            c[0].move_ip(0, candy_speed)
            if c[0].colliderect(player):  # Catch item
                candies.remove(c)
                if c[1] == "snowball":
                    score -= 1
                else:
                    score += 1
            elif c[0].top > cfg.SCREENSIZE[1]:  # Out of screen
                candies.remove(c)

        # Gradually increase candy speed
        candy_speed += 0.01

        # Draw everything on the pygame surface
        screen.blit(background_img, (0, 0))
        screen.blit(sleigh_img, player.topleft)

        # Display items
        for c in candies:
            if c[1] == "present":
                screen.blit(present_img, c[0].topleft)
            elif c[1] == "santa":
                screen.blit(santa_img, c[0].topleft)
            elif c[1] == "snowball":
                screen.blit(snowball_img, c[0].topleft)
            elif c[1] == "snowman":
                screen.blit(snowman_img, c[0].topleft)

        # Display score and remaining time
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        time_text = font.render(f"Time: {int(remaining_time)}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(time_text, (10, 50))

        # Render the pygame surface onto the tkinter canvas
        game_surface = pygame.image.tostring(screen, "RGB")
        game_image = Image.frombytes("RGB", cfg.SCREENSIZE, game_surface)
        game_photo = ImageTk.PhotoImage(game_image)
        game_canvas.create_image(0, 0, anchor="nw", image=game_photo)
        game_canvas.image = game_photo  # Keep a reference to avoid garbage collection

        if running:
            root.after(16, game_loop)  # Schedule the next game loop iteration
        else:
            pygame.quit()
            show_final_score(root, score, level_selection_screen)

    # Run the game loop
    running = True
    game_loop()

def show_final_score(root, score, level_selection_screen):
    # Clear screen and display final score
    for widget in root.winfo_children():
        widget.destroy()

    # Display final score message
    tk.Label(root, text=f"Game Over! Your Score: {score}", font=("Arial", 24, "bold")).pack(pady=50)

    # Display the return icon
    try:
        return_img = Image.open("assets/images/return_icon.png")
        return_img = return_img.resize((80, 80), Image.LANCZOS)
        return_icon = ImageTk.PhotoImage(return_img)

        # Create a label with the return icon, placed in the center below the score
        return_label = tk.Label(root, image=return_icon)
        return_label.image = return_icon  # Keep a reference to avoid garbage collection
        return_label.pack(pady=20)

        # Bind the click event to return to level selection
        return_label.bind("<Button-1>", lambda e: level_selection_screen())

    except Exception as e:
        print("Return icon not found:", e)
