import tkinter as tk
from PIL import Image, ImageTk
from tkinter import font
from level1 import level1_game
from level2 import level2_game
from level3 import level3_game
from direction import GameDirectionFactory  # Import the factory

# Enhanced decorator for text styling and color
def style_text(underline=True, color="black"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            widget = func(*args, **kwargs)
            if isinstance(widget, tk.Label):
                current_font = font.Font(font=widget["font"])
                styled_font = font.Font(
                    family=current_font.actual("family"),
                    size=current_font.actual("size"),
                    weight="bold",  # Make it bold
                    slant="italic",  # Italicize
                    underline=underline  # Optional underline
                )
                widget.configure(font=styled_font, fg=color)  # Set the font and color
            return widget
        return wrapper
    return decorator

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

# Flashing effect and color setup
flashing = True
flash_job_id = None
color_index = 0
colors = ["orange", "yellow", "green"]

def start_game(event=None):
    global flashing
    flashing = False
    if flash_job_id is not None:
        root.after_cancel(flash_job_id)
    root.unbind("<Key>")  # Unbind the key event to prevent repeated triggering
    start_screen.destroy()
    level_selection_screen()

def flash_text():
    global flash_job_id, color_index
    if flashing:
        new_color = colors[color_index]
        canvas.itemconfig(instruction_text, fill=new_color)
        color_index = (color_index + 1) % len(colors)
        flash_job_id = root.after(500, flash_text)

# --- Level Selection Screen ---
def level_selection_screen():
    for widget in root.winfo_children():
        widget.destroy()

    selection_screen = tk.Frame(root)
    selection_screen.pack(fill="both", expand=True, padx=20, pady=10)

    # Define level information
    level_info = [
        {
            "name": "Trick-or-treating",
            "image_path": "assets/images/halloween_background.png",
            "start_level": level1_game,
            "color": "purple",
        },
        {
            "name": "Harvesting Festival",
            "image_path": "assets/images/thanksgiving_background.png",
            "start_level": level2_game,
            "color": "orange",
        },
        {
            "name": "Santa's Present",
            "image_path": "assets/images/christmas_background.png",
            "start_level": level3_game,
            "color": "green",
        },
    ]

    # Configure grid columns for alignment and spacing
    selection_screen.grid_columnconfigure(0, weight=1)
    selection_screen.grid_columnconfigure(3, weight=1)

    # Title for level selection screen on the left, without underline
    @style_text(underline=False)
    def create_title_label():
        return tk.Label(selection_screen, text="Select the Holiday\nGame you want to play", font=("Helvetica", 20), justify="right")

    title_label = create_title_label()
    title_label.grid(row=0, column=1, padx=(0, 20), sticky="e")

    # Instructional description below the title, split into two lines
    @style_text(underline=False)
    def create_description_label():
        return tk.Label(selection_screen, text="Click on the images to enter the game.\nThe difficulty increases from Halloween to Christmas", font=("Helvetica", 12), justify="right")

    description_label = create_description_label()
    description_label.grid(row=1, column=1, padx=(0, 20), sticky="e")

    # Display Levels with Images and Names
    for i, info in enumerate(level_info):
        try:
            # Load and resize level image
            level_image = Image.open(info["image_path"]).resize((300, 200), Image.LANCZOS)
            level_photo = ImageTk.PhotoImage(level_image)

            # Image Label for each level
            level_label = tk.Label(selection_screen, image=level_photo)
            level_label.image = level_photo  # Keep a reference
            row, col = (0, 2) if i == 0 else (3, i)
            rowspan = 2 if i == 0 else 1
            level_label.grid(row=row, column=col, rowspan=rowspan, padx=10, pady=(5, 10), sticky="n")

            # Bind to show directions before starting the game
            level_label.bind("<Button-1>", lambda e, level=info: show_direction_screen(level))

            # Name Label below the image with specific color
            @style_text(underline=False, color=info["color"])
            def create_name_label():
                return tk.Label(selection_screen, text=info["name"], font=("Helvetica", 14))

            name_label = create_name_label()
            name_label.grid(row=row + rowspan, column=col, padx=10, pady=(0, 20), sticky="n")
        except Exception as e:
            print(f"Error loading {info['name']} image: {e}")

# --- Show Directions Screen ---
def show_direction_screen(level):
    """Display the direction screen for a selected level."""
    for widget in root.winfo_children():
        widget.destroy()

    # Use the factory to get the appropriate directions
    try:
        direction_instance = GameDirectionFactory.create_direction(level["name"])
        directions = direction_instance.get_directions()
    except ValueError as e:
        directions = str(e)

    # Create a new screen for directions
    direction_screen = tk.Frame(root)
    direction_screen.pack(fill="both", expand=True, padx=20, pady=20)

    # Display directions
    direction_label = tk.Label(direction_screen, text=directions, font=("Helvetica", 14), justify="left", anchor="w")
    direction_label.pack(fill="both", expand=True)

    # Button to start the game
    start_button = tk.Button(
        direction_screen, text="Start Game", font=("Helvetica", 16, "bold"),
        command=lambda: level["start_level"](root, level_selection_screen)
    )
    start_button.pack(pady=20)

# --- Main Start Screen Setup ---
start_screen = tk.Frame(root)
start_screen.pack(fill="both", expand=True)

try:
    cover_image = Image.open("assets/images/cover.png")
    cover_image = cover_image.resize((800, 600), Image.LANCZOS)
    cover_photo = ImageTk.PhotoImage(cover_image)
    canvas = tk.Canvas(start_screen, width=800, height=600)
    canvas.create_image(0, 0, anchor="nw", image=cover_photo)
    canvas.pack()

    global instruction_text
    instruction_text = canvas.create_text(400, 570, text="Press any key to begin the game", font=("Helvetica", 18, "italic"), fill=colors[0])

    flash_text()
    root.bind("<Key>", start_game)

except Exception as e:
    print("Cover image not found:", e)
    tk.Label(start_screen, text="HalloThanksMas", font=("Helvetica", 36, "bold")).pack(pady=50)

root.mainloop()
