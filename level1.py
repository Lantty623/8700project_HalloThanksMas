import random
import tkinter as tk
import pygame
import time
from PIL import Image, ImageTk
import cfg
import scoreboard
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
            # Pass the image path instead of the Pygame surface
            ask_player_name(root, score, level_selection_screen, "assets/images/halloween_background.png")

    # Run the game loop
    running = True
    game_loop()


def ask_player_name(root, score, level_select_screen, background_image):
    # Clear the screen
    for widget in root.winfo_children():
        widget.destroy()

    # Load the background image
    background_image = Image.open(background_image)
    background_image = background_image.resize((800, 600), Image.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)

    # Create a canvas to hold the background
    canvas = tk.Canvas(root, width=800, height=600)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image=background_photo)

    # Keep a reference to avoid garbage collection
    canvas.image = background_photo

    # Display final score message
    canvas.create_text(
        400, 100, text=f"Game Over! Your Score: {score}",
        font=("Helvetica", 24, "bold"), fill="purple"
    )

    canvas.create_text(
        400, 180, text="Enter Your Name Below",
        font=("Helvetica", 20, "italic"), fill="orange"
    )

    # Name entry
    name_input = tk.StringVar()
    name_entry = tk.Entry(
        root, textvariable=name_input,
        font=("Helvetica", 16), justify="center",
        highlightthickness=4, highlightbackground="orange"
    )
    name_entry_window = canvas.create_window(400, 230, anchor="center", window=name_entry)

    # Error label
    error_label = tk.Label(root, text="", font=("Helvetica", 12), fg="white", bg="purple")
    error_label_window = canvas.create_window(400, 270, anchor="center", window=error_label)

    # Confirm button
    def confirm_button():
        player_name = name_input.get().strip()
        if player_name:
            show_final_score(root, player_name, score, level_select_screen)
        else:
            error_label.config(text="Name cannot be empty!")

    confirm_button_widget = tk.Button(
        root, text="Confirm", font=("Helvetica", 16, "bold"),
        bg="white", fg="orange", command=confirm_button
    )
    canvas.create_window(400, 330, anchor="center", window=confirm_button_widget)


def show_final_score(root, player_name, score, level_selection_screen):
    # Clear the screen
    for widget in root.winfo_children():
        widget.destroy()

    # Load the background image
    background_image_path = "assets/images/halloween_background.png"  # Use the appropriate path
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((800, 600), Image.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)

    # Create a canvas to hold the background
    canvas = tk.Canvas(root, width=800, height=600)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image=background_photo)

    # Keep a reference to avoid garbage collection
    canvas.image = background_photo

    # Display final score message
    canvas.create_text(
        400, 100, text=f"Game Over! Your Score: {score}",
        font=("Helvetica", 24, "bold"), fill="purple"
    )

    # Display the player's name
    canvas.create_text(
        400, 150, text=f"Congratulations, {player_name}!",
        font=("Helvetica", 20, "italic"), fill="orange"
    )

    # update scoreboard
    # player_name = input("Enter your name: ")
    scoreboard.add_score("level1", player_name, score)

    # Add a "Show Scoreboard" button
    show_scoreboard_button = tk.Button(
        root,
        text="Show Current Scoreboard",
        font=("Helvetica", 16, "bold"),
        fg="orange",
        command=lambda: scoreboard.display_scoreboard("level1")
    )
    canvas.create_window(400, 250, anchor="center", window=show_scoreboard_button)

    # Add a return button to go back to the level selection screen
    try:
        return_img = Image.open("assets/images/return_icon.png")
        return_img = return_img.resize((80, 80), Image.LANCZOS)
        return_icon = ImageTk.PhotoImage(return_img)

        # Create a label with the return icon
        return_label = tk.Label(
            root,
            image=return_icon,
            bg="black",  # Match the canvas background to blend
            borderwidth=0  # Remove border for a cleaner look
        )
        return_label.image = return_icon  # Keep a reference to avoid garbage collection
        return_label_window = canvas.create_window(
            400, 350, anchor="center", window=return_label
        )
        # Bind the click event to return to level selection
        return_label.bind("<Button-1>", lambda e: level_selection_screen())
    except Exception as e:
        print("Return icon not found:", e)
