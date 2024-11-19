import tkinter as tk
from PIL import Image, ImageTk
from tkinter import font
from level1 import level1_game
from level2 import level2_game
from level3 import level3_game
from direction import GameDirectionFactory 

# Decorator for text modifying(Decorator pattern)
def style_text(underline=True, color="black"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            widget = func(*args, **kwargs)
            if isinstance(widget, tk.Label):
                current_font = font.Font(font=widget["font"])
                styled_font = font.Font(
                    family=current_font.actual("family"),
                    size=current_font.actual("size"),
                    weight="bold",
                    slant="italic",
                    underline=underline
                )
                widget.configure(font=styled_font, fg=color)  
            return widget
        return wrapper
    return decorator

# Singleton to ensure only one game instance(Singleton pattern)
class SingletonTkinter:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SingletonTkinter, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.root = tk.Tk()
        self.root.title("HalloThanksMas")
        self.root.geometry("800x600")

# Initialize the main window
singleton_tk = SingletonTkinter()
root = singleton_tk.root

# Flashing effect and color setup for the main screen
flashing = True
flash_job_id = None
color_index = 0
colors = ["orange", "yellow", "green"]

# Function to start the game from the start screen
def start_game(event=None):
    global flashing
    flashing = False
    if flash_job_id is not None:
        root.after_cancel(flash_job_id)
    root.unbind("<Key>")  
    start_screen.destroy()
    level_selection_screen()

# Function to add flashing effect to the text on start screen
def flash_text():
    global flash_job_id, color_index
    if flashing:
        new_color = colors[color_index]
        canvas.itemconfig(instruction_text, fill=new_color)
        color_index = (color_index + 1) % len(colors)
        flash_job_id = root.after(500, flash_text)

# --- Level Selection Screen ---
# Player is able to pick what level they want here
def level_selection_screen():
    for widget in root.winfo_children():
        widget.destroy()

    selection_screen = tk.Frame(root)
    selection_screen.pack(fill="both", expand=True, padx=20, pady=10)

    # Define level information
    level_info = [
        {"name": "Trick-or-treating", "image_path": "assets/images/halloween_background.png", "start_level": level1_game, "color": "purple"},
        {"name": "Harvesting Festival", "image_path": "assets/images/thanksgiving_background.png", "start_level": level2_game, "color": "orange"},
        {"name": "Santa's Present", "image_path": "assets/images/christmas_background.png", "start_level": level3_game, "color": "green"},
    ]

    # Title for level selection screen on the left
    @style_text(underline=False)
    def create_title_label():
        return tk.Label(selection_screen, text="Select the Holiday\nGame you want to play", font=("Helvetica", 20), justify="right")

    title_label = create_title_label()
    title_label.grid(row=0, column=1, padx=(0, 20), sticky="e")

    # Description of what to do below the title
    @style_text(underline=False)
    def create_description_label():
        return tk.Label(selection_screen, text="Click on the images to enter the game.\nThe difficulty increases from Halloween to Christmas", font=("Helvetica", 12), justify="right")

    description_label = create_description_label()
    description_label.grid(row=1, column=1, padx=(0, 20), sticky="e")

    # Display Levels with Game Images and Game Names
    for i, info in enumerate(level_info):
        try:
            # Load and resize level image
            level_image = Image.open(info["image_path"]).resize((300, 200), Image.LANCZOS)
            level_photo = ImageTk.PhotoImage(level_image)

            # Image Label for each level
            level_label = tk.Label(selection_screen, image=level_photo)
            level_label.image = level_photo
            row, col = (0, 2) if i == 0 else (3, i)
            rowspan = 2 if i == 0 else 1
            level_label.grid(row=row, column=col, rowspan=rowspan, padx=10, pady=(5, 10), sticky="n")

            # Show the instruction screen before starting the game
            level_label.bind("<Button-1>", lambda e, level=info: show_direction_screen(level))

            # Label below image with holiday color
            @style_text(underline=False, color=info["color"])
            def create_name_label():
                return tk.Label(selection_screen, text=info["name"], font=("Helvetica", 14))

            name_label = create_name_label()
            name_label.grid(row=row + rowspan, column=col, padx=10, pady=(0, 20), sticky="n")
        except Exception as e:
            print(f"Error loading {info['name']} image: {e}")

# --- Show Directions Screen ---
# Provide instructions on how to play the game
def show_direction_screen(level):
    for widget in root.winfo_children():
        widget.destroy()

    # Use the factory to get the directions for the level that was selected
    try:
        direction_instance = GameDirectionFactory.create_direction(level["name"])
    except ValueError as e:
        direction_instance = None

    # Create a new screen for the player to see the direction
    direction_screen = tk.Frame(root)
    direction_screen.pack(fill="both", expand=True, padx=20, pady=20)

    if direction_instance:
        @style_text(color=level["color"])
        def create_title_label():
            return tk.Label(direction_screen, text=direction_instance.title, font=("Helvetica", 25, "bold"), anchor="center")

        title_label = create_title_label()
        title_label.pack(pady=(10, 20))

        # Point Guide Section
        point_guide_frame = tk.Frame(direction_screen, padx=10, pady=10)
        point_guide_frame.pack(fill="x", anchor="w")

        @style_text(color="black")
        def create_point_guide_label():
            return tk.Label(point_guide_frame, text="Point Guide:", font=("Helvetica", 20, "bold"), anchor="w")

        point_guide_label = create_point_guide_label()
        point_guide_label.pack(anchor="w", pady=(0, 5))

        for image_path, description in direction_instance.point_guide:
            item_frame = tk.Frame(point_guide_frame)
            item_frame.pack(anchor="w", pady=2)
            image = Image.open(image_path).resize((40, 40), Image.LANCZOS)
            image_photo = ImageTk.PhotoImage(image)
            item_image_label = tk.Label(item_frame, image=image_photo)
            item_image_label.image = image_photo
            item_image_label.pack(side="left", padx=(0, 10))

            @style_text(color="black")
            def create_item_description_label():
                return tk.Label(item_frame, text=description, font=("Helvetica", 20), anchor="w")

            item_description_label = create_item_description_label()
            item_description_label.pack(side="left", anchor="w")

        # Objectiuve of the game or goal
        @style_text(color="black")
        def create_section_label(section_name):
            return tk.Label(direction_screen, text=section_name, font=("Helvetica", 18, "bold"), anchor="w")

        objective_label = create_section_label("Objective:")
        objective_label.pack(anchor="w", pady=(20, 5), padx=10)

        objective_text = tk.Label(direction_screen, text=direction_instance.objective, font=("Helvetica", 16), anchor="w", justify="left", wraplength=750)
        objective_text.pack(anchor="w", padx=20)

        # The control that the player will be using
        control_label = create_section_label("Control:")
        control_label.pack(anchor="w", pady=(20, 5), padx=10)

        control_text = tk.Label(direction_screen, text=direction_instance.control, font=("Helvetica", 16), anchor="w", justify="left", wraplength=750)
        control_text.pack(anchor="w", padx=20)

    # Button to start the game
    start_button = tk.Button(direction_screen, text="Start Game", font=("Helvetica", 16, "bold"), command=lambda: level["start_level"](root, level_selection_screen))
    start_button.pack(pady=20)

# --- Main Start Screen ---
# What the player will see when game is executed
start_screen = tk.Frame(root)
start_screen.pack(fill="both", expand=True)

try:
    cover_image = Image.open("assets/images/cover.png")
    cover_image = cover_image.resize((800, 600), Image.LANCZOS)
    cover_photo = ImageTk.PhotoImage(cover_image)
    canvas = tk.Canvas(start_screen, width=800, height=600)
    canvas.create_image(0, 0, anchor="nw", image=cover_photo)
    canvas.pack()

    instruction_text = canvas.create_text(400, 570, text="Press any key to begin the game", font=("Helvetica", 18, "italic"), fill=colors[0])
    flash_text()
    root.bind("<Key>", start_game)

except Exception as e:
    print("Cover image not found:", e)
    tk.Label(start_screen, text="HalloThanksMas", font=("Helvetica", 36, "bold")).pack(pady=50)

root.mainloop()