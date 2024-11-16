import json
import pygame
from qtawesome.iconic_font import text_color
import tkinter as tk
from PIL import Image, ImageTk

jsonfile = "scoreboard.json"


# init and load file
def init_scoreboard():
    try:
        with open(jsonfile,"r") as file:
            return json.load(file)
    except FileNotFoundError:
        data = {"level1": [],"level2": [],"level3": []}
        with open(jsonfile, "w") as file:
            json.dump(data, file)

        return  data

# save
def save_scoreboard(data):
    with open(jsonfile, "w") as file:
        json.dump(data, file, indent=4)


# add score to scoreboard
def add_score(level, name, score):
    data = init_scoreboard()
    data[level].append({"name": name, "score": score})

    #sort scoreboard
    data[level].sort(key=lambda x: x["score"], reverse=True)

    save_scoreboard(data)

def display_scoreboard(level):
    data = init_scoreboard()
    scores = data.get(level,[])

    root = tk.Tk()
    root.title(f"{level.capitalize()} Scoreboard")
    root.geometry("400x600")

    # title
    title_label = tk.Label(root, text=f"{level.capitalize()} Scoreboard", font=("Arial", 20, "bold"))
    title_label.pack(pady=20)

    # scoreboard
    frame = tk.Frame(root)
    frame.pack(pady=10)

    for i, entry in enumerate(scores[:10], 1):  # only show top 10
        rank_label = tk.Label(frame, text=f"{i}. {entry['name']}    {entry['score']}", font=("Arial", 14))
        rank_label.pack(anchor="w")

    # close button
    close_button = tk.Button(root, text="Close", command=root.destroy, font=("Arial", 12))
    close_button.pack(pady=20)


    root.mainloop()


