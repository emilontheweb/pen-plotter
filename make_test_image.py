from PIL import Image, ImageDraw

img = Image.new("RGB", (600, 600), "white")
draw = ImageDraw.Draw(img)

draw.ellipse([50, 50, 250, 250], fill=(0, 0, 0))  # black circle, top-left
draw.rectangle([350, 50, 550, 250], fill=(220, 30, 30)) # red square, top right
draw.polygon([(300, 350), (150, 550), (450, 550)], fill=(30, 60, 200)) # blue triangle, bottom
draw.rectangle([430, 320, 560, 480], fill=(20, 140, 60)) # green rectangle, right side

img.save("images/test_pattern.png")