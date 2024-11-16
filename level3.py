import random
import tkinter as tk
import pygame
import time
from PIL import Image, ImageTk
import cfg
from memento import Memento, Caretaker
import scoreboard

def level3_game(root, level_selection_screen):
    # Clear the current window
    for widget in root.winfo_children():
        widget.destroy()

    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()  # Initialize mixer for sound effects

    # Load sound files
    pygame.mixer.music.load("assets/sounds/christmas_background.mp3")  # Background music file
    present_sound = pygame.mixer.Sound("assets/sounds/present_sound.mp3")  # Sound effect for catching a present
    snowball_sound = pygame.mixer.Sound("assets/sounds/snowball_sound.mp3")  # Sound effect for catching a snowball
    freeze_sound = pygame.mixer.Sound("assets/sounds/freeze_sound.mp3")  # Sound effect for catching a snowman

    # Start background music
    pygame.mixer.music.play(loops=-1)  # Loop the music indefinitely

    # Create a tkinter Canvas to hold the pygame surface
    game_canvas = tk.Canvas(root, width=cfg.SCREENSIZE[0], height=cfg.SCREENSIZE[1])
    game_canvas.pack()

    # Create a pygame Surface to render the game
    screen = pygame.Surface(cfg.SCREENSIZE)
    clock = pygame.time.Clock()

    # Load images
    background_img = pygame.image.load("assets/images/christmas_background.png")
    background_img = pygame.transform.scale(background_img, cfg.SCREENSIZE)
    snow_background_img = pygame.image.load("assets/images/snow_background.png")
    snow_background_img = pygame.transform.scale(snow_background_img, (cfg.SCREENSIZE[0], cfg.SCREENSIZE[1] // 4))
    sleigh_img = pygame.image.load("assets/images/sleigh.png")
    custom_sleigh_size = (int(cfg.PLAYER_SIZE[0] * 1.5), int(cfg.PLAYER_SIZE[1] * 0.5))
    sleigh_img = pygame.transform.scale(sleigh_img, custom_sleigh_size)
    present_img = pygame.image.load("assets/images/present.png")
    present_img = pygame.transform.scale(present_img, cfg.CANDY_SIZE)
    snowball_img = pygame.image.load("assets/images/snowball.png")
    snowball_img = pygame.transform.scale(snowball_img, cfg.CANDY_SIZE)
    snowman_img = pygame.image.load("assets/images/snowman.png")
    snowman_img = pygame.transform.scale(snowman_img, cfg.CANDY_SIZE)

    # Initial position for the sleigh, set to move up as snow height increases
    player = pygame.Rect(
        (cfg.SCREENSIZE[0] // 2 - custom_sleigh_size[0] // 2,
         cfg.SCREENSIZE[1] - custom_sleigh_size[1] - 10),
        custom_sleigh_size
    )

    candies = []
    score = 0
    font = pygame.font.SysFont(None, 36)

    # Timer and speed variables
    start_time = time.time()
    candy_speed = cfg.CANDY_SPEED * 2
    freeze_end_time = 0  # Initialize freeze time to zero
    freeze_warning_popup = None  # Popup for freeze warning
    freeze_warning_shown = False  # Track if warning has been shown for current freeze
    snow_height = 0  # Initial height of the snow accumulation

    # Key state tracking for movement
    keys_pressed = {"left": False, "right": False}

    # Game state
    game_state = {"paused": False}

    # Memento and Caretaker for saving and restoring game state
    caretaker = Caretaker()

    # Define functions to handle key events
    def on_key_press(event):
        if event.keysym == "Left":
            keys_pressed["left"] = True
        elif event.keysym == "Right":
            keys_pressed["right"] = True
        elif event.keysym == "p":  # Pause game on 'p' key press
            if game_state["paused"]:
                state = caretaker.load_state()
                if state:
                    restore_state(state)
                game_state["paused"] = False
            else:
                caretaker.save_state(Memento(save_state()))
                game_state["paused"] = True

    def on_key_release(event):
        if event.keysym == "Left":
            keys_pressed["left"] = False
        elif event.keysym == "Right":
            keys_pressed["right"] = False

    # Bind the key events to tkinter
    root.bind("<KeyPress>", on_key_press)
    root.bind("<KeyRelease>", on_key_release)

    # Function to save the current game state
    def save_state():
        return {
            "candies": candies.copy(),
            "score": score,
            "candy_speed": candy_speed,
            "freeze_end_time": freeze_end_time,
            "snow_height": snow_height,
            "keys_pressed": keys_pressed.copy()
        }

    # Function to restore the game state from a memento
    def restore_state(state):
        nonlocal candies, score, candy_speed, freeze_end_time, snow_height, keys_pressed
        candies = state["candies"]
        score = state["score"]
        candy_speed = state["candy_speed"]
        freeze_end_time = state["freeze_end_time"]
        snow_height = state["snow_height"]
        keys_pressed = state["keys_pressed"]

    # Function to show freeze warning with countdown
    def show_freeze_warning():
        nonlocal freeze_warning_popup, freeze_warning_shown
        if freeze_warning_popup is not None:
            freeze_warning_popup.destroy()
            freeze_warning_popup = None

        # Only create a new popup if one does not already exist
        freeze_warning_popup = tk.Toplevel(root)
        freeze_warning_popup.title("Freeze Warning")
        freeze_warning_popup.geometry("300x100")
        freeze_warning_popup.transient(root)
        freeze_warning_popup.grab_set()
        freeze_warning_popup.lift()
        freeze_warning_popup.focus_force()
        freeze_warning_shown = True  # Set flag to indicate warning has been shown

        label = tk.Label(freeze_warning_popup, font=("Arial", 14), fg="red")
        label.pack(expand=True)

        # Update countdown in real-time
        def update_countdown():
            nonlocal freeze_warning_popup
            remaining_time = int(freeze_end_time - time.time())
            if remaining_time > 0:
                label.config(text=f"Frozen! {remaining_time} seconds remaining...")
                freeze_warning_popup.after(1000, update_countdown)
            else:
                if freeze_warning_popup:
                    freeze_warning_popup.destroy()
                    freeze_warning_popup = None  # Reset popup reference

        update_countdown()

    # Game loop function
    def game_loop():
        nonlocal running, score, candy_speed, freeze_end_time, freeze_warning_shown, snow_height

        if not game_state["paused"]:
            # Check for time elapsed
            elapsed_time = time.time() - start_time
            remaining_time = cfg.GAME_DURATION - elapsed_time

            if remaining_time <= 0:
                running = False  # End the game if time is up

            # Handle player movement based on key presses, only if not frozen
            if time.time() > freeze_end_time:
                sleigh_speed = cfg.PLAYER_SPEED
                if keys_pressed["left"]:
                    player.move_ip(-sleigh_speed, 0)
                if keys_pressed["right"]:
                    player.move_ip(sleigh_speed, 0)
                freeze_warning_shown = False  # Reset warning flag once freeze ends
            else:
                # Show freeze warning only during freeze caused by snowman
                if not freeze_warning_shown:
                    show_freeze_warning()

            # Ensure the player stays within screen bounds horizontally
            player.clamp_ip(pygame.Rect(0, player.top, cfg.SCREENSIZE[0], player.height))

            # Gradually increase snow height over time, up to half the screen height
            snow_height = min(snow_height + 0.2, cfg.SCREENSIZE[1] // 2)

            # Adjust the sleigh's vertical position based on snow height
            player.top = cfg.SCREENSIZE[1] - custom_sleigh_size[1] - 10 - int(snow_height)

            # Random item drop with specified frequency and ratio (4:2:1 for presents, snowballs, and snowmen)
            if random.randint(1, 20) == 1:
                candy_x = random.randint(0, cfg.SCREENSIZE[0] - cfg.CANDY_SIZE[0])
                candy_type = random.choices(["present", "snowball", "snowman"], weights=[4, 2, 1], k=1)[0]
                new_candy = pygame.Rect(candy_x, 0, *cfg.CANDY_SIZE)  # Spawn from the top of the screen
                candies.append((new_candy, candy_type))

            # Move candies and check for collision with player
            for candy in list(candies):

                # random candy and snowman move
                if candy[1] == "snowman":
                    speed_x = random.choice([-30,-20,-10, 0, 10, 20, 30])
                else:
                    speed_x = random.choice([-5, 0, 5])

                candy[0].move_ip(speed_x, candy_speed)
                if candy[0].colliderect(player):  # Catch item
                    candies.remove(candy)
                    if candy[1] == "snowball":
                        score -= 50  # Deduct points for catching a snowball
                        snowball_sound.play()  # Play snowball sound effect
                    elif candy[1] == "snowman":
                        freeze_end_time = time.time() + 5  # Freeze player for 5 seconds
                        freeze_sound.play()  # Play freeze sound effect
                        show_freeze_warning()  # Show freeze warning immediately
                    else:
                        score += 100  # Add points for catching a present
                        present_sound.play()  # Play present sound effect
                elif candy[0].top > cfg.SCREENSIZE[1]:  # Out of screen
                    candies.remove(candy)

            # Gradually increase candy speed
            candy_speed += 0.01

            # Draw everything on the pygame surface
            screen.blit(background_img, (0, 0))

            # Draw falling items
            for candy in candies:
                if candy[1] == "present":
                    screen.blit(present_img, candy[0].topleft)
                elif candy[1] == "snowball":
                    screen.blit(snowball_img, candy[0].topleft)
                elif candy[1] == "snowman":
                    screen.blit(snowman_img, candy[0].topleft)

            # Draw the snow background starting from the bottom, rising with `snow_height`
            for y in range(cfg.SCREENSIZE[1] - int(snow_height), cfg.SCREENSIZE[1], snow_background_img.get_height()):
                screen.blit(snow_background_img, (0, y))

            # Draw the sleigh on top of the snow background
            screen.blit(sleigh_img, player.topleft)

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
            if pygame.mixer.get_init():  # Only stop music if mixer is initialized
                pygame.mixer.music.stop()  # Stop background music
            ask_player_name(root, score, level_selection_screen)

    # Run the game loop
    running = True
    game_loop()


def ask_player_name(root, score, level_select_screen):
    # clear screen
    for widget in root.winfo_children():
        widget.destroy()

    # Display final score message
    tk.Label(root, text=f"Game Over! Your Score: {score}", font=("Arial", 24, "bold")).pack(pady=50)

    tk.Label(root, text="Enter Your Name", font=("Arial", 20, "bold")).pack(pady=50)

    # input
    name_input = tk.StringVar()
    name_entry = tk.Entry(root, textvariable = name_input, font=("Arial", 16), justify="center")
    name_entry.pack(pady=20)

    # error label
    error_label = tk.Label(root, text="", font=("Arial", 12), fg="red")
    error_label.pack()

    # confirm button
    def confirm_button():
        player_name = name_input.get().strip()
        if player_name:
            show_final_score(root, player_name, score, level_select_screen)
        else:
            error_label.config(text="Name cannot be empty!")

    tk.Button(root,text="Confirm", font=("Arial", 16), command= confirm_button).pack(pady=20)


def show_final_score(root,player_name,  score, level_selection_screen):
    # Clear screen and display final score
    for widget in root.winfo_children():
        widget.destroy()

    # Display final score message
    tk.Label(root, text=f"Game Over! Your Score: {score}", font=("Arial", 24, "bold")).pack(pady=50)

    # update scoreboard
    # player_name = input("Enter your name: ")
    scoreboard.add_score("level3", player_name, score)

    # add a "show scoreboard" button
    show_scoreboard_button = tk.Button(
        root,
        text = "Show Scoreboard",
        font=("Arial", 16),
        command=lambda: scoreboard.display_scoreboard("level3")
    )
    show_scoreboard_button.pack(pady=20)

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



