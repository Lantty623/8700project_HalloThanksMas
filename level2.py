import random
import tkinter as tk
import pygame
import time
from PIL import Image, ImageTk
import cfg

def start_level2(root, level_selection_screen):
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

    # Timer initialization
    start_time = time.time()
    candy_speed = cfg.CANDY_SPEED*2  # Set to original speed

    # Combo tracking
    combo_requirements = {"turkey": 1, "pie": 2, "mash": 1}  # Initial requirement
    collected_items = {"turkey": 0, "pie": 0, "mash": 0}

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

    # Game loop function
    def game_loop():
        nonlocal running, score, candy_speed, collected_items

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

        # Randomly drop a new object
        if random.randint(1, 15) == 1:
            candy_x = random.randint(0, cfg.SCREENSIZE[0] - cfg.CANDY_SIZE[0])
            candy_type = random.choice(["turkey", "pie", "mash"])  # Randomly select the type
            candy_img = turkey_img if candy_type == "turkey" else pie_img if candy_type == "pie" else mash_img
            new_candy = pygame.Rect(candy_x, 0, *cfg.CANDY_SIZE)
            candies.append((new_candy, candy_img, candy_type))  # Append as (position, image, type)

        # Move candies and check for collision with player
        for c in list(candies):
            c[0].move_ip(0, candy_speed)
            if c[0].colliderect(player):  # Catch object
                candies.remove(c)
                collected_items[c[2]] += 1  # Update collected count for the object type

                # Check for combo completion
                if check_combo_completion():
                    score += 100  # Award points for completing the set
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
            show_final_score(root, score, level_selection_screen)



    # Run the game loop
    running = True
    game_loop()

# Final score display
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
