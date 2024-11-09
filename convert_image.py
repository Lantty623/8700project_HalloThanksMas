from PIL import Image

# Load the .webp image
image = Image.open("checkmark.jfif")

# Save it as a .png
image.save("assets/images/checkmark.png", "PNG")
