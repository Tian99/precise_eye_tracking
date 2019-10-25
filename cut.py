from PIL import Image

imageObject = Image.open("input/sample.png")

cropped = imageObject.crop((350,230,1700,3000))

cropped.save('output/cropped.png')