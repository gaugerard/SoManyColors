from PIL import Image

im = Image.open("D:\PDF_File\imagesPDF\image-0_m.png")
width = im.size[0]  # size in pixels
height = im.size[1]
print width
print height
print width*height