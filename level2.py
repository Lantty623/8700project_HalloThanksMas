import tkinter as tk
from PIL import Image, ImageTk

def start_level2(root, level_selection_screen):
    # Clear the current window
    for widget in root.winfo_children():
        widget.destroy()
    
    # Display Thanksgiving level-specific UI
    tk.Label(root, text="Thanksgiving Level", font=("Arial", 24, "bold")).pack(pady=50)
    
    # Load the return icon image
    try:
        return_img = Image.open("assets/images/return_icon.png")
        return_img = return_img.resize((80, 80), Image.LANCZOS)  # Resize as needed
        return_icon = ImageTk.PhotoImage(return_img)
        
        # Create a label with the return icon, positioned in the top-left corner
        return_label = tk.Label(root, image=return_icon, bg=root["bg"])
        return_label.image = return_icon  # Keep a reference to avoid garbage collection
        return_label.place(x=10, y=10)  # Position in the top-left corner
        
        # Bind a click event to the label to act like a button
        return_label.bind("<Button-1>", lambda e: level_selection_screen())
    
    except Exception as e:
        print("Return icon not found:", e)
