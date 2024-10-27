from PIL import Image

# Load the .webp image
image = Image.open("assets/images/cover.webp")

# Save it as a .png
image.save("assets/images/cover.png", "PNG")
