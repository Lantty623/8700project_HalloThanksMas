import tkinter as tk

def start_level1(root, level_selection_screen):
    # Clear the current window
    for widget in root.winfo_children():
        widget.destroy()
    
    # Display Halloween level-specific UI
    tk.Label(root, text="Halloween Level", font=("Arial", 24, "bold")).pack(pady=50)
    
    # Add a "Return" button to go back to the level selection screen
    return_button = tk.Button(root, text="Return to Level Selection", font=("Arial", 16), command=level_selection_screen)
    return_button.pack(pady=20)
