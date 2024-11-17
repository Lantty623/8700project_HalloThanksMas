from PIL import Image

# Load the .webp image
image = Image.open("C_score.jpg")

# Save it as a .png
image.save("assets/images/c_score.png", "PNG")
# Load the .webp image
image = Image.open("H_score.jpg")

# Save it as a .png
image.save("assets/images/h_score.png", "PNG")

