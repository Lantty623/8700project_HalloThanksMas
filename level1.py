import tkinter as tk

def start_level1(root):
    # Clear the current window
    for widget in root.winfo_children():
        widget.destroy()
    
    # Display Halloween level-specific UI
    tk.Label(root, text="Halloween Level", font=("Arial", 24, "bold")).pack(pady=50)
    # Add Halloween-specific game components here
