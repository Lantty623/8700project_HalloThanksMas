from PIL import Image

# Load the .webp image
image = Image.open("assets/images/return_icon.webp")

# Save it as a .png
image.save("assets/images/return_icon.png", "PNG")
