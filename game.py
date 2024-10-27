import tkinter as tk
from PIL import Image, ImageTk

# Initialize the main window
root = tk.Tk()
root.title("HalloThanksMas")
root.geometry("800x600")  # Adjust to your screen size

# Initialize variables for flashing
flashing = True
flash_job_id = None
color_index = 0
colors = ["orange", "yellow", "green"]  # List of colors to cycle through

# Function to start the game when any key is pressed
def start_game(event=None):
    global flashing
    flashing = False  # Stop the flashing effect
    if flash_job_id is not None:
        root.after_cancel(flash_job_id)  # Cancel the flashing job
    start_screen.destroy()  # Destroy the start screen
    game_screen()  # Proceed to the game screen

# Function to set up the game screen (placeholder)
def game_screen():
    game_label = tk.Label(root, text="Game Screen (Level 1)", font=("Arial", 24))
    game_label.pack(pady=100)

# Flashing effect function with color cycling
def flash_text():
    global flash_job_id, color_index
    if flashing:  # Only run if flashing is True
        # Cycle through the colors
        new_color = colors[color_index]
        canvas.itemconfig(instruction_text, fill=new_color)
        color_index = (color_index + 1) % len(colors)  # Move to the next color in the list
        flash_job_id = root.after(500, flash_text)  # Save the job ID to be able to cancel it

# Create the start screen frame
start_screen = tk.Frame(root)
start_screen.pack(fill="both", expand=True)

# Load and resize the cover image
try:
    cover_image = Image.open("assets/images/cover.png")
    cover_image = cover_image.resize((800, 600), Image.LANCZOS)
    cover_photo = ImageTk.PhotoImage(cover_image)
    
    # Create a Canvas to hold the image and text
    canvas = tk.Canvas(start_screen, width=800, height=600)
    canvas.create_image(0, 0, anchor="nw", image=cover_photo)
    canvas.pack()

    # Add flashing instruction text at the bottom of the canvas
    global instruction_text  # Declare as global so flash_text can access it
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

# Run the application
root.mainloop()
