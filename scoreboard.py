import json
import tkinter as tk
from PIL import Image, ImageTk

jsonfile = "scoreboard.json"

# Initialize and load file
def init_scoreboard():
    try:
        with open(jsonfile, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        data = {"level1": [], "level2": [], "level3": []}
        with open(jsonfile, "w") as file:
            json.dump(data, file)
        return data

# Save scoreboard data
def save_scoreboard(data):
    with open(jsonfile, "w") as file:
        json.dump(data, file, indent=4)

# Add score to scoreboard
def add_score(level, name, score):
    data = init_scoreboard()
    data[level].append({"name": name, "score": score})

    # Sort scoreboard in descending order of scores
    data[level].sort(key=lambda x: x["score"], reverse=True)
    save_scoreboard(data)

# Display scoreboard with custom background and title
def display_scoreboard(level, background_image_path=None):
    data = init_scoreboard()
    scores = data.get(level, [])

    root = tk.Toplevel()  # Create a pop-up window for the scoreboard
    root.title(f"{level.capitalize()} Scoreboard")
    root.geometry("400x600")

    # Set up the canvas
    canvas = tk.Canvas(root, width=400, height=600)
    canvas.pack(fill="both", expand=True)

    # Set up the background if the image path is provided
    if background_image_path:
        background_image = Image.open(background_image_path)
        background_image = background_image.resize((400, 600), Image.LANCZOS)
        background_photo = ImageTk.PhotoImage(background_image)

        canvas.create_image(0, 0, anchor="nw", image=background_photo)

        # Keep a reference to avoid garbage collection
        canvas.background_photo = background_photo
    else:
        canvas.configure(bg="white")

    # Titles for levels
    titles = {
        "level1": "Trick-or-Treating",
        "level2": "Harvesting Festival",
        "level3": "Santa's Present",
    }
    # Add the title label to the canvas
    canvas.create_text(
        200, 50,
        text=titles.get(level, "Scoreboard"),
        font=("Helvetica", 20, "bold"),
        fill="white" if background_image_path else "black"
    )

    # Display the scores
    for i, entry in enumerate(scores[:10], 1):  # Show top 10 scores
        canvas.create_text(
            200, 100 + i * 30,
            text=f"{i}. {entry['name']} - {entry['score']}",
            font=("Helvetica", 16),
            fill="white" if background_image_path else "black"
        )

    # Add a close button
    close_button = tk.Button(
        canvas,
        text="Close",
        font=("Helvetica", 12),
        command=root.destroy,
        bg="white",
        fg="black",
    )
    canvas.create_window(200, 550, anchor="center", window=close_button)

    root.mainloop()
