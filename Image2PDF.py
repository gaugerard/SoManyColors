from PIL import Image
import os

filename = "C:\Users\gauth\PycharmProjects\untitled\pdf\images_des_pdf\Im196.jpeg"
im = Image.open(filename)
if im.mode == "RGBA":
    im = im.convert("RGB")
new_filename = "C:\Users\gauth\PycharmProjects\untitled\pdf\images_des_pdf\Im196.pdf"
if not os.path.exists(new_filename):
    im.save(new_filename, "pdf", resolution=100.0)


# -----------------------------------------------------------------------

def change2pdf(jpeg_name, type_im):
    filename = "C:\Users\gauth\PycharmProjects\untitled\pdf\images_des_pdf\\" + str(jpeg_name)
    im = Image.open(filename)
    if im.mode == "RGBA":
        im = im.convert("RGB")
        pdf_name = jpeg_name.remove(type_im)
    new_filename = "C:\Users\gauth\PycharmProjects\untitled\pdf\images_des_pdf\\" + str(pdf_name) + ".pdf"
    if not os.path.exists(new_filename):
        im.save(new_filename, "pdf", resolution=100.0)