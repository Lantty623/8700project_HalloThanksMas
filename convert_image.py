from PIL import Image

# Load the .webp image
image = Image.open("assets/images/LevelSectionalTheme.webp")

# Save it as a .png
image.save("assets/images/LevelSelection.png", "PNG")
