import tkinter as tk
from PIL import Image, ImageTk
from level1 import start_level1
from level2 import start_level2
from level3 import start_level3

# Initialize the main window
root = tk.Tk()
root.title("HalloThanksMas")
root.geometry("800x600")

# Flashing effect and color setup
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
    
    root.unbind("<Key>")  # Unbind the key event to prevent repeated triggering
    start_screen.destroy()  # Destroy the start screen
    level_selection_screen()  # Go to level selection


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

    tk.Button(selection_screen, text="Halloween", font=("Arial", 18), command=lambda: start_level1(root), bg="orange", fg="black").pack(pady=10)
    tk.Button(selection_screen, text="Thanksgiving", font=("Arial", 18), command=lambda: start_level2(root), bg="brown", fg="white").pack(pady=10)
    tk.Button(selection_screen, text="Christmas", font=("Arial", 18), command=lambda: start_level3(root), bg="green", fg="white").pack(pady=10)

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
    tk.Label(start_screen, text="HalloThanksMas", font=("Arial", 36, "bold")).pack(pady=50)

root.mainloop()
