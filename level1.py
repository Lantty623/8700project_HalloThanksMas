import random
import tkinter as tk
import pygame
import time
from PIL import Image, ImageTk
import cfg
from memento import Memento, Caretaker

def level1_game(root, level_selection_screen):
    # Clear the current window
    for widget in root.winfo_children():
        widget.destroy()

    # Initialize Pygame and Pygame Mixer for sound
    pygame.init()
    pygame.mixer.init()

    # Load sounds
    try:
        pygame.mixer.music.load("assets/sounds/halloween_background.mp3")
        pygame.mixer.music.set_volume(0.5)  # Adjust volume as needed
        pygame.mixer.music.play(-1)  # Play background music in a loop

        candy_sound = pygame.mixer.Sound("assets/sounds/candy_sound.mp3")
        ghost_sound = pygame.mixer.Sound("assets/sounds/ghost_sound.mp3")
        candy_sound.set_volume(0.7)  # Adjust volume as needed
        ghost_sound.set_volume(0.7)  # Adjust volume as needed
    except Exception as e:
        print("Error loading sound files:", e)

    # Create a tkinter Canvas to hold the pygame surface
    game_canvas = tk.Canvas(root, width=cfg.SCREENSIZE[0], height=cfg.SCREENSIZE[1])
    game_canvas.pack()

    # Create a pygame Surface to render the game
    screen = pygame.Surface(cfg.SCREENSIZE)
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

    # Player setup
    player = pygame.Rect(
        (cfg.SCREENSIZE[0] // 2 - cfg.PLAYER_SIZE[0] // 2,
        cfg.SCREENSIZE[1] - cfg.PLAYER_SIZE[1] - 10),
        cfg.PLAYER_SIZE
    )

    candies = []
    score = 0
    font = pygame.font.SysFont(None, 36)

    # Timer initialization
    start_time = time.time()

    # Key state tracking for movement
    keys_pressed = {"left": False, "right": False}

    # Game state
    game_state = {"paused": False}

    # Define functions to handle key events
    def on_key_press(event):
        if event.keysym == "Left":
            keys_pressed["left"] = True
        elif event.keysym == "Right":
            keys_pressed["right"] = True
        elif event.keysym == "p":  # Pause game on 'p' key press
            game_state["paused"] = not game_state["paused"]

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
        nonlocal running, score

        if not game_state["paused"]:
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

            # Random candy/ghost drop
            if random.randint(1, 20) == 1:
                candy_x = random.randint(0, cfg.SCREENSIZE[0] - cfg.CANDY_SIZE[0])
                new_candy = pygame.Rect(candy_x, 0, *cfg.CANDY_SIZE)
                candy_type = random.choice(["candy", "ghost"])
                candies.append((new_candy, candy_type))

            # Move candies and check for collision with player
            for c in list(candies):
                c[0].move_ip(0, cfg.CANDY_SPEED)
                if c[0].colliderect(player):  # Catch item
                    candies.remove(c)
                    if c[1] == "candy":
                        score += 100  # Add points for candy
                        candy_sound.play()  # Play candy sound
                    elif c[1] == "ghost":
                        score -= 50  # Deduct points for ghost
                        ghost_sound.play()  # Play ghost sound
                elif c[0].top > cfg.SCREENSIZE[1]:  # Out of screen
                    candies.remove(c)

            # Draw everything on the pygame surface
            screen.blit(background_img, (0, 0))
            screen.blit(pumpkin_img, player.topleft)

            # Display candies and ghosts
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

        # Render the pygame surface onto the tkinter canvas
        game_surface = pygame.image.tostring(screen, "RGB")
        game_image = Image.frombytes("RGB", cfg.SCREENSIZE, game_surface)
        game_photo = ImageTk.PhotoImage(game_image)
        game_canvas.create_image(0, 0, anchor="nw", image=game_photo)
        game_canvas.image = game_photo  # Keep a reference to avoid garbage collection

        if running:
            root.after(30, game_loop)  # Schedule the next game loop iteration
        else:
            pygame.mixer.music.stop()  # Stop background music when the game ends
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