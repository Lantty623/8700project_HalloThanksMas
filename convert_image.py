from PIL import Image

# Load the .webp image
image = Image.open("pumkin.PNG")

# Save it as a .png
image.save("assets/images/pumkin.png", "PNG")
