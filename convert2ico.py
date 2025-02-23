from PIL import Image

# img = Image.open("gw2iconpng.png")
img = Image.open("gw2icon.ico")

# img.save("gw2icon.ico", format="ICO", sizes=[(256,256)])
print(img.info)