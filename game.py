import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance
from level1 import level1_game
from level2 import level2_game
from level3 import level3_game

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
        },
        {
            "name": "Harvesting Festival",
            "image_path": "assets/images/thanksgiving_background.png",
            "start_level": level2_game,
        },
        {
            "name": "Santa's Present",
            "image_path": "assets/images/christmas_background.png",
            "start_level": level3_game,
        },
    ]

    # Configure grid columns for alignment and spacing
    selection_screen.grid_columnconfigure(0, weight=1)
    selection_screen.grid_columnconfigure(3, weight=1)

    # Title for level selection screen on the left, split into two lines
    title_label = tk.Label(selection_screen, text="Select the Holiday\nGame you want to play", font=("Helvetica", 20, "bold"), justify="right")
    title_label.grid(row=0, column=1, padx=(0, 20), sticky="e")

    # Instructional description below the title, split into two lines
    description_label = tk.Label(selection_screen, text="Click on the images to enter the game.\nThe difficulty increases from Halloween to Christmas", font=("Helvetica", 12, "italic"), justify="right")
    description_label.grid(row=1, column=1, padx=(0, 20), sticky="e")

    # Display Halloween Level on the first row
    try:
        # Load and resize Halloween image
        halloween_image = Image.open(level_info[0]["image_path"]).resize((300, 200), Image.LANCZOS)
        halloween_photo = ImageTk.PhotoImage(halloween_image)

        # Image Label for Halloween Level
        halloween_label = tk.Label(selection_screen, image=halloween_photo)
        halloween_label.image = halloween_photo  # Keep a reference
        halloween_label.grid(row=0, column=2, rowspan=2, padx=10, pady=(5, 10), sticky="n")
        halloween_label.bind("<Button-1>", lambda e: level_info[0]["start_level"](root, level_selection_screen))

        # Name Label for Halloween Level below the image
        halloween_name = tk.Label(selection_screen, text=level_info[0]["name"], font=("Helvetica", 16, "bold"))
        halloween_name.grid(row=2, column=2, padx=10, pady=(0, 20), sticky="n")

    except Exception as e:
        print(f"Error loading Halloween image: {e}")

    # Display Thanksgiving and Christmas Levels on the second row
    for i, info in enumerate(level_info[1:], start=1):
        try:
            # Load and resize image for each level
            level_image = Image.open(info["image_path"]).resize((300, 200), Image.LANCZOS)
            level_photo = ImageTk.PhotoImage(level_image)

            # Image Label for Thanksgiving and Christmas Levels
            level_label = tk.Label(selection_screen, image=level_photo)
            level_label.image = level_photo  # Keep a reference
            level_label.grid(row=3, column=i, padx=10, pady=(0, 10), sticky="n")
            level_label.bind("<Button-1>", lambda e, func=info["start_level"]: func(root, level_selection_screen))

            # Name Label for each level below the image
            level_name = tk.Label(selection_screen, text=info["name"], font=("Helvetica", 16, "bold"))
            level_name.grid(row=4, column=i, padx=10, pady=(0, 20), sticky="n")

        except Exception as e:
            print(f"Error loading {info['name']} image: {e}")


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