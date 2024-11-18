import random
import tkinter as tk
import pygame
import time
from PIL import Image, ImageTk
import cfg
from memento import Memento, Caretaker
import scoreboard

def level2_game(root, level_selection_screen):
    # Clear the current window
    for widget in root.winfo_children():
        widget.destroy()

    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()  # Initialize the mixer for sound

    # Load sounds
    item_catch_sound = pygame.mixer.Sound("assets/sounds/item_catch.mp3")  # Sound when item is caught
    set_complete_sound = pygame.mixer.Sound("assets/sounds/set_complete.mp3")  # Sound when set is completed
    pygame.mixer.music.load("assets/sounds/thanksgiving_background.mp3")  # Background music
    pygame.mixer.music.play(-1)  # Loop the background music indefinitely

    # Create a tkinter Canvas to hold the pygame surface
    game_canvas = tk.Canvas(root, width=cfg.SCREENSIZE[0], height=cfg.SCREENSIZE[1])
    game_canvas.pack()

    # Create a pygame Surface to render the game
    screen = pygame.Surface(cfg.SCREENSIZE)
    clock = pygame.time.Clock()

    # Load images
    background_img = pygame.image.load("assets/images/thanksgiving_background.png")
    background_img = pygame.transform.scale(background_img, cfg.SCREENSIZE)
    tray_img = pygame.image.load("assets/images/tray.png")
    custom_tray_size = (int(cfg.PLAYER_SIZE[0] * 1.5), int(cfg.PLAYER_SIZE[1] * 0.5))
    tray_img = pygame.transform.scale(tray_img, custom_tray_size)

    # Load individual images for each falling object type
    turkey_img = pygame.image.load("assets/images/turkey.png")
    turkey_img = pygame.transform.scale(turkey_img, cfg.CANDY_SIZE)
    pie_img = pygame.image.load("assets/images/pie.png")
    pie_img = pygame.transform.scale(pie_img, cfg.CANDY_SIZE)
    mash_img = pygame.image.load("assets/images/mash.png")
    mash_img = pygame.transform.scale(mash_img, cfg.CANDY_SIZE)

    # Load checkmark image
    checkmark_img = pygame.image.load("assets/images/checkmark.png")
    checkmark_img = pygame.transform.scale(checkmark_img, (30, 30))

    # Player setup
    player = pygame.Rect(
        (cfg.SCREENSIZE[0] // 2 - custom_tray_size[0] // 2,
        cfg.SCREENSIZE[1] - custom_tray_size[1] - 10),
        custom_tray_size
    )

    candies = []
    score = 0
    font = pygame.font.SysFont(None, 36)

    # Item points
    item_points = {"turkey": 100, "pie": 50, "mash": 150}  # Points for each item type

    # Timer initialization
    start_time = time.time()
    pause_start_time = 0  # Track when the pause begins
    total_pause_time = 0  # Track total time spent paused
    candy_speed = cfg.CANDY_SPEED*2  # Set to original speed

    # Combo tracking
    combo_requirements = {"turkey": 1, "pie": 2, "mash": 1}  # Initial requirement
    collected_items = {"turkey": 0, "pie": 0, "mash": 0}

    # Key state tracking for movement
    keys_pressed = {"left": False, "right": False}

    # Game state
    game_state = {"paused": False}

    # Memento caretaker
    caretaker = Caretaker()

    # Define functions to handle key events
    def on_key_press(event):
        nonlocal pause_start_time, total_pause_time, candies, score, start_time, collected_items, combo_requirements, player
        if event.keysym == "Left":
            keys_pressed["left"] = True
        elif event.keysym == "Right":
            keys_pressed["right"] = True
        elif event.keysym == "p":
            if not game_state["paused"]:
                pause_start_time = time.time()
                game_state["paused"] = True
                caretaker.save_state(Memento({
                    "player_pos": player.topleft,
                    "candies": [(c[0].topleft, c[2]) for c in candies],
                    "score": score,
                    "start_time": start_time,
                    "total_pause_time": total_pause_time,
                    "pause_start_time": pause_start_time,
                    "keys_pressed": keys_pressed,
                    "collected_items": collected_items,
                    "combo_requirements": combo_requirements
                }))
            else:
                game_state["paused"] = False
                saved_state = caretaker.load_state()
                if saved_state:
                    player.topleft = saved_state["player_pos"]
                    candies = [(pygame.Rect(pos, cfg.CANDY_SIZE), get_candy_image(candy_type), candy_type) for
                               pos, candy_type in saved_state["candies"]]
                    score = saved_state["score"]
                    start_time = saved_state["start_time"]
                    total_pause_time = saved_state["total_pause_time"]
                    pause_start_time = saved_state["pause_start_time"]
                    total_pause_time += time.time() - pause_start_time
                    keys_pressed.update(saved_state["keys_pressed"])
                    collected_items = saved_state["collected_items"]
                    combo_requirements = saved_state["combo_requirements"]
    def get_candy_image(candy_type):
        if candy_type == "turkey":
            return turkey_img
        elif candy_type == "pie":
            return pie_img
        elif candy_type == "mash":
            return mash_img
        return None

    def on_key_release(event):
        if event.keysym == "Left":
            keys_pressed["left"] = False
        elif event.keysym == "Right":
            keys_pressed["right"] = False

    # Bind the key events to tkinter
    root.bind("<KeyPress>", on_key_press)
    root.bind("<KeyRelease>", on_key_release)

    # Function to refresh combo requirements after a set is completed
    def refresh_combo_requirements():
        nonlocal combo_requirements
        combo_requirements = {
            "turkey": random.randint(1, 2),
            "pie": random.randint(1, 2),
            "mash": random.randint(1, 2)
        }

    # Function to check if current collection meets combo requirements
    def check_combo_completion():
        for item, required_count in combo_requirements.items():
            if collected_items[item] < required_count:
                return False
        return True

    # Function to calculate score based on current combo requirements
    def calculate_combo_score():
        return sum(item_points[item] * count for item, count in combo_requirements.items())

    # Game loop function
    def game_loop():
        nonlocal running, score, candy_speed, collected_items

        if not game_state["paused"]:
            # Calculate elapsed time excluding pause time
            current_time = time.time()
            actual_elapsed_time = current_time - start_time - total_pause_time
            remaining_time = cfg.GAME_DURATION - actual_elapsed_time

            if remaining_time <= 0:
                running = False  # End the game if time is up

            # Handle player movement based on key presses
            if keys_pressed["left"]:
                player.move_ip(-cfg.PLAYER_SPEED, 0)
            if keys_pressed["right"]:
                player.move_ip(cfg.PLAYER_SPEED, 0)

            # Ensure the player stays within screen bounds
            player.clamp_ip(screen.get_rect())

            # Randomly drop a new object
            if random.randint(1, 15) == 1:
                candy_x = random.randint(0, cfg.SCREENSIZE[0] - cfg.CANDY_SIZE[0])
                candy_type = random.choice(["turkey", "pie", "mash"])  # Randomly select the type
                candy_img = turkey_img if candy_type == "turkey" else pie_img if candy_type == "pie" else mash_img
                new_candy = pygame.Rect(candy_x, 0, *cfg.CANDY_SIZE)
                candies.append((new_candy, candy_img, candy_type))  # Append as (position, image, type)

            # Move candies and check for collision with player
            for c in list(candies):
                # random candy and turkey move
                if c[2] == "turkey":
                    speed_x = random.choice([-30,-20,-10, 0, 10, 20, 30])
                else:
                    speed_x = random.choice([-5, 0, 5])

                c[0].move_ip(speed_x, candy_speed)
                if c[0].colliderect(player):  # Catch object
                    candies.remove(c)
                    collected_items[c[2]] += 1  # Update collected count for the object type
                    item_catch_sound.play()  # Play item catch sound

                    # Check for combo completion
                    if check_combo_completion():
                        combo_score = calculate_combo_score()  # Calculate dynamic score for the completed set
                        score += combo_score  # Add calculated score
                        set_complete_sound.play()  # Play set completion sound
                        collected_items = {key: 0 for key in collected_items}  # Reset collection
                        refresh_combo_requirements()  # Set a new combo requirement

                elif c[0].top > cfg.SCREENSIZE[1]:  # Out of screen
                    candies.remove(c)

            # Draw everything on the pygame surface
            screen.blit(background_img, (0, 0))
            screen.blit(tray_img, player.topleft)

            # Display falling objects
            for c in candies:
                screen.blit(c[1], c[0].topleft)  # Use the image stored in the tuple

            # Display score and remaining time
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            time_text = font.render(f"Time: {int(remaining_time)}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))
            screen.blit(time_text, (10, 50))

            # Display required set images and counters
            item_x = 10  # Starting x position for displaying the required items
            for item, required_count in combo_requirements.items():
                item_img = turkey_img if item == "turkey" else pie_img if item == "pie" else mash_img
                screen.blit(item_img, (item_x, 100))  # Display item image
                required_text = font.render(f"{collected_items[item]}/{required_count}", True, (255, 255, 255))
                screen.blit(required_text, (item_x, 130))  # Display collected/required count below the image

                # Display checkmark if item count is met or exceeded
                if collected_items[item] >= required_count:
                    screen.blit(checkmark_img, (item_x + 35, 105))  # Position the checkmark to the right of the image

                item_x += 50  # Move x position for the next item

        # Render the pygame surface onto the tkinter canvas
        game_surface = pygame.image.tostring(screen, "RGB")
        game_image = Image.frombytes("RGB", cfg.SCREENSIZE, game_surface)
        game_photo = ImageTk.PhotoImage(game_image)
        game_canvas.create_image(0, 0, anchor="nw", image=game_photo)
        game_canvas.image = game_photo  # Keep a reference to avoid garbage collection

        if running:
            root.after(30, game_loop)  # Schedule the next game loop iteration
        else:
            pygame.quit()
            ask_player_name(root, score, level_selection_screen,"assets/images/thanksgiving_background.png")

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
        font=("Helvetica", 24, "bold"), fill="brown"
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
    error_label = tk.Label(root, text="", font=("Helvetica", 12), fg="white", bg="brown")
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

    # Load the background image for the final score screen
    background_image_path = "assets/images/thanksgiving_background.png"
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
        font=("Helvetica", 24, "bold"), fill="brown"
    )

    # Display the player's name
    canvas.create_text(
        400, 150, text=f"Congratulations, {player_name}!",
        font=("Helvetica", 20, "italic"), fill="orange"
    )

    # Update the scoreboard with the player's score
    scoreboard.add_score("level2", player_name, score)

    # Add a "Show Scoreboard" button with the custom background image
    show_scoreboard_button = tk.Button(
        root,
        text="Show Current Scoreboard",
        font=("Helvetica", 16, "bold"),
        bg="#6F4E37",
        fg="orange",
        command=lambda: scoreboard.display_scoreboard("level2", "assets/images/t_score.png")  # Pass the background image path
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
            bg="#6F4E37",  # Match the canvas background to blend
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