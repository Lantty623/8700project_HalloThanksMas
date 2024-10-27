import tkinter as tk
from PIL import Image, ImageTk

# Initialize the main window
root = tk.Tk()
root.title("HalloThanksMas")
root.geometry("800x600")

# Initialize variables for flashing
flashing = True
flash_job_id = None
color_index = 0
colors = ["orange", "yellow", "green"]

# Function to start the game and go to level selection
def start_game(event=None):
    global flashing
    flashing = False
    if flash_job_id is not None:
        root.after_cancel(flash_job_id)
    start_screen.destroy()  # Destroy the start screen
    level_selection_screen()  # Go to level selection

# Flashing effect function with color cycling
def flash_text():
    global flash_job_id, color_index
    if flashing:
        new_color = colors[color_index]
        canvas.itemconfig(instruction_text, fill=new_color)
        color_index = (color_index + 1) % len(colors)
        flash_job_id = root.after(500, flash_text)

# --- Level Selection Screen ---
def level_selection_screen():
    selection_screen = tk.Frame(root)
    selection_screen.pack(fill="both", expand=True)

    title_label = tk.Label(selection_screen, text="Choose Your Level", font=("Arial", 24, "bold"))
    title_label.pack(pady=20)

    # Buttons for each level
    halloween_button = tk.Button(selection_screen, text="Halloween", font=("Arial", 18),
                                 command=load_halloween, bg="orange", fg="black")
    halloween_button.pack(pady=10)

    thanksgiving_button = tk.Button(selection_screen, text="Thanksgiving", font=("Arial", 18),
                                    command=load_thanksgiving, bg="brown", fg="white")
    thanksgiving_button.pack(pady=10)

    christmas_button = tk.Button(selection_screen, text="Christmas", font=("Arial", 18),
                                 command=load_christmas, bg="green", fg="white")
    christmas_button.pack(pady=10)

# --- Level Loading Functions ---
def load_halloween():
    for widget in root.winfo_children():
        widget.destroy()
    halloween_screen()

def load_thanksgiving():
    for widget in root.winfo_children():
        widget.destroy()
    thanksgiving_screen()

def load_christmas():
    for widget in root.winfo_children():
        widget.destroy()
    christmas_screen()

# --- Level-Specific Screens ---
def halloween_screen():
    tk.Label(root, text="Halloween Level", font=("Arial", 24, "bold")).pack(pady=50)

def thanksgiving_screen():
    tk.Label(root, text="Thanksgiving Level", font=("Arial", 24, "bold")).pack(pady=50)

def christmas_screen():
    tk.Label(root, text="Christmas Level", font=("Arial", 24, "bold")).pack(pady=50)

# --- Main Start Screen Setup ---
start_screen = tk.Frame(root)
start_screen.pack(fill="both", expand=True)

# Load the cover image on the start screen
try:
    cover_image = Image.open("assets/images/cover.png")
    cover_image = cover_image.resize((800, 600), Image.LANCZOS)
    cover_photo = ImageTk.PhotoImage(cover_image)

    #Create a Canvas to hold the image and text
    canvas = tk.Canvas(start_screen, width=800, height=600)
    canvas.create_image(0, 0, anchor="nw", image=cover_photo)
    canvas.pack()

    # Flashing text as a separate label, displayed at the bottom of the start screen
    global instruction_text
    instruction_text = canvas.create_text(
        400, 570,  # Position near the bottom center
        text="Press any key to begin the game .......",
        font=("Helvetica", 18, "italic"),  # Change font as desired
        fill=colors[0]  # Start with the first color
    )

    # Start the flashing effect
    flash_text()

    # Bind any key press to start the game
    root.bind("<Key>", start_game)



except Exception as e:
    print("Cover image not found:", e)
    cover_label = tk.Label(start_screen, text="HalloThanksMas", font=("Arial", 36, "bold"))
    cover_label.pack(pady=50)


root.mainloop()
