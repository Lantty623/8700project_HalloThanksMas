import tkinter as tk

def start_level2(root):
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Label(root, text="Thanksgiving Level", font=("Arial", 24, "bold")).pack(pady=50)
    # Add Thanksgiving-specific game components here
