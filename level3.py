import tkinter as tk

def start_level3(root, level_selection_screen):
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Label(root, text="Christmas Level", font=("Arial", 24, "bold")).pack(pady=50)
    
    # Add a "Return" button to go back to the level selection screen
    return_button = tk.Button(root, text="Return to Level Selection", font=("Arial", 16), command=level_selection_screen)
    return_button.pack(pady=20)
