
import os
from PIL import Image, EpsImagePlugin
import imghdr
from PyPDF2 import PdfFileMerger
import ntpath
from subprocess import call
import os.path
import sys
import time
#import thread
import math


def PDF2jpg(pdf_file, jpg_file, dpi, ImageMagickConvert_file = 'D:\ProgrammePDF\ImageMagick-6.4.7-Q16\convert'):
    """
    Converts each page of a PDF into png and saves them in jpg_file directory
    :param pdf_file: the pdf source's directory
    :param jpg_file: the file of destination
    :param ImageMagickConvert_file: the directory where ImageMagick\convert is located
    """
    stringDensity = ' -density ' + str(dpi) + ' '
    # -density 300 = will set the dpi to 300
    # -quality 100 = will set the compression to 100 for PNG, JPG and MIFF file format ( 100 means NO compresion )
    call(ImageMagickConvert_file + stringDensity + pdf_file + ' -quality 100 ' + jpg_file + '\image.png')
    #call(ImageMagickConvert_file + ' ' + pdf_file + ' ' + jpg_file + '\image.png')


def change_color(png_file, image, R_value, G_value, B_value):
    """
    Modifies all the pixels of the image stocked in the png_file directory. It ADDS the R_value to the Red
    value of the pixel and gives it a new name ( name.png --> name_m.png )
    :param png_file: the directory where the image is saved ( exe : D:\Users\Images )
    :param image: name of the specific image to process ( exe : 'image1.png' )
    :param R_value: integer that will be added to the R value of the pixel ( (R, G, B) )
    :param G_value: integer that will be added to the G value of the pixel ( (R, G, B) )
    :param B_value: integer that will be added to the B value of the pixel ( (R, G, B) )
    :return image_m_name: the name of the modified png ( exe : image_name = image1.png --> image_m_name = image1_m.png )
    """

    # OPENS THE IMAGE DIRECTORY
    direct_name = png_file + "\\" + image
    pathexists(direct_name)
    im = Image.open(direct_name)

    # INFORMATION :
    imtype = imghdr.what(direct_name)  # give the type of a image so we can remov it from the name and modify it

    width = im.size[0]  # in pixels
    height = im.size[1]  # in pixels
    image_name = image.replace("." + imtype.lower(), "")  # name without the type

    for x in range(width):
        for y in range(height):
            pixel_info = im.getpixel((x, y))  # return the state ( color_ RGB ) of the pixel
            # MODIFICATION : ( -50, -25, 0) = R'G'B'
            r2 = pixel_info[0] + R_value  # R
            g2 = pixel_info[1] + G_value  # G
            b2 = pixel_info[2] + B_value  # B
            im.putpixel((x, y), (r2, g2, b2))

    image_m_name = image_name + '_m.' + (imtype.lower())
    directory = png_file + "\\" + str(image_m_name)
    im.save(directory)

    return image_m_name


def change2pdf(png_file, jpeg_name, type_im):
    """
    Changes a the png ( jpeg_name ) in the file (png_file) into a pdf file
    :param png_file: the directory where the image is saved ( exe : D:\Users\Images )
    :param jpeg_name: name of the specific image to process ( exe : 'image1.png' )
    :param type_im: the type of the image ( here it is '.png' )
    :return pdf_name: the name of the PDF that has been created from the png
    """

    filename = png_file + '\\' + str(jpeg_name)
    pathexists(filename)
    im = Image.open(filename)

    if im.mode == "RGBA":
        im = im.convert("RGB")

    pdf_name = jpeg_name.replace('.' + type_im, '.pdf')
    new_filename = png_file + '\\' + pdf_name

    if not os.path.exists(new_filename):
        im.save(new_filename, "pdf", density='300x300')

    return pdf_name


def mergePDF(pdf_file, png_file, dico_im_pdf):
    """
    Merges every PDF of a file into a single bigger PDF
    :param pdf_file: the directory where the PDF is saved
    :param png_file: the directory where the png from the PDF are saved
    :param merger: an object merger that allows the merging of PDF pages
    :param dico_im_pdf: a dictionary which contains all the name of the PDFs that needs to be merged
    """
    pdf_m_name = str(path_leaf(pdf_file)).replace('.pdf', '_m.pdf')  # exe : PDF_delta.pdf --> PDF_delta_m.pdf
    merger = PdfFileMerger()

    for num in range(dico_im_pdf['nbr_pages']):
        if (dico_im_pdf[num] in os.listdir(png_file)) and ((dico_im_pdf[num]).endswith('.pdf')):

                merger.append(png_file + '\\' + dico_im_pdf[num])
                # os.remove(png_file + '\\' + dico_im_pdf[num])  cant remove the pdf :/ ...
                del dico_im_pdf[num]
                # print 'SUPPRESION dico_im_m MERGEPDF = ', dico_im_pdf

    merger.write(pdf_m_name)


def path_leaf(path):
    """
    :param path: a directory ( exe : 'C\User\Program\Images\image1.png' )
    :return tail : the tail of the path ( exe : 'image1.png' )
    """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def movePDF(pdf_file):
    """
    Moves a pdf from the current directory ( where the PDF is created by the program )  to the directory where the src
    PDF was taken from.

    (
    exe :
    src PDF = PDF_delta.pdf       in directory 'C\pdf'
    dest PDF = PDF_delta_m.pdf    in directory 'C\pdf'
    )

    :param pdf_file: the directory of the source PDF
    """
    pdf_name = str(path_leaf(pdf_file)).replace('.pdf', '_m.pdf')  # ( exe : PDF_delta.pdf --> PDF_delta_m.pdf )
    current_dir = os.getcwd() + '\\' + pdf_name  # ( exe : current directory of the PDF_delta_m.pdf )
    final_dir = pdf_file.replace('.pdf', '_m.pdf')  # ( exe : directory of PDF_delta.pdf )

    print 'Created PDF src path : ', current_dir
    print 'PDF destination path : ', final_dir

    pathexists(current_dir)

    os.rename(current_dir, final_dir)

    pathexists(final_dir)


def setup(pdf_file, png_file):
    """
    Deletes the PDF on the png_file path
    :param png_file: the path where the images and pdf will be manipulated by the program
    """

    pdf_m_name = path_leaf(pdf_file).replace('.pdf', '_m.pdf')
    pdf_m_path = pdf_file.replace('\\' + path_leaf(pdf_file), '')

    if pdf_m_name in os.listdir(pdf_m_path):
        os.remove(pdf_m_path + '\\' + pdf_m_name)

    current_dir = os.getcwd()
    if pdf_m_name in os.listdir(current_dir):
        os.remove(current_dir + '\\' + pdf_m_name)

    for file in os.listdir(png_file):
        if file.endswith('.pdf') or file.endswith('.png'):
            os.remove(png_file + '\\' + file)


def pathexists(path):
    if not os.path.exists(path):
        raise Exception('NotExistingPathException')

    return True


def colorfilterok(colorfilter):
    if len(colorfilter) != 3:
        raise Exception('SizeTupleException')

    for val in colorfilter:
        if type(val) != int and type(val) != float and type(val) != long:
            raise Exception('NotIntegerInTupleException')

        if val > 255 or val < 0:
            raise Exception('TupleValuesException')

    return True


def main(pdf_file, color_blind_filter, dpi, png_file='D:\PDF_File\imagesPDF'):
    """
    |----------------------------------------------------------------------|
    |/!\ - This version is radically different from the version 5 !!!  /!\ |
    |----------------------------------------------------------------------|

    VERSION 5.1:
    ----------
    Create a new pdf where every pages has been modified to suit colorblindness
    :param pdf_file: the directory of the pdf that you want to convert into .png
    :param png_file: file where all the created .png will be saved
    :param color_blind_filter: a tuple of 3 integer that are added to the RGB of a pixel ( exe : (80, 60, 30) )

    |----------------------------------------------------------------------|
    |/!\ - This version is radically different from the version 5 !!!  /!\ |
    |----------------------------------------------------------------------|
    """
    t1 = time.time()
    colorfilterok(color_blind_filter)
    pathexists(pdf_file)
    pathexists(png_file)


    # CLEANS THE DIRECTORY WHERE .png WILL BE MANIPULATED
    setup(pdf_file, png_file)

    # PRINT INFORMATION ABOUT THE PROCESS
    print '\n'
    print 'PDF source path : ', pdf_file
    print 'File of processes : ', png_file
    print 'Filter to apply : ', color_blind_filter

    # CREATES PNG OUT OF A PDF
    PDF2jpg(pdf_file, png_file, dpi)

    # ---------------------------------------------------------
    # TEST IF IT IS A PNG OR NOT AND THEN CONVERT ITS COLOR
    liste_im_m = []  # list of modified images ( will be completed after the FOR )
    dico_im_pdf = {}

    # print 'INITIALISATION liste_im_m0 = ', liste_im_m, 'dico_im_m0 = ', dico_im_pdf

    num = 0
    for element in os.listdir(png_file):
        if element.endswith('.png'):
            # print("'%s' est un fichier png" % element)
            liste_im_m.append(change_color(png_file, element, color_blind_filter[0], color_blind_filter[1], color_blind_filter[2]))
            dico_im_pdf[num] = ''
            num = num + 1

    dico_im_pdf['nbr_pages'] = num

    #print 'ETAT liste_im_m1 = ', liste_im_m, 'dico_im_m1 = ', dico_im_pdf
    # ---------------------------------------------------------


    # CHANGES .png INTO .pdf
    for num in range(dico_im_pdf['nbr_pages']):
        image_m = 'image-' + str((num)) + '_m.png'
        direct_name = png_file + '\\' + image_m
        type_im_m = imghdr.what(direct_name)
        dico_im_pdf[num] = (change2pdf(png_file, image_m, type_im_m))

    # print 'ETAT liste_im_m2 = ', liste_im_m, 'dico_im_m2 = ', dico_im_pdf
    # ---------------------------------------------------------
    # DELETES THE .png SINCE WE DON'T NEED THEM ANYMORE
    for png in os.listdir(png_file):
        if png.endswith('.png'):
            os.remove(png_file + '\\' + png)

    # ---------------------------------------------------------
    # MERGES THE PDF
    mergePDF(pdf_file, png_file, dico_im_pdf)

    t2 = time.time()

    print ('Time taken to process the PDF : ', t2 - t1)

    # MOVES THE NEW PDF IN THE PDF, THAT WE WANT TO MODIFY, DIRECTORY
    movePDF(pdf_file)  # <-------------------------------------------------------------


# main('C:\Users\gauth\PycharmProjects\untitled\pdf\SoManyColors\PDFsrc.gitignore\ML_12_clustering_slides_300dpi.pdf', (0, 100, 0), 'C:\Users\gauth\PycharmProjects\untitled\pdf\SoManyColors\TraitementDir.gitignore')
# main('D:\Cours2017-2018Q1\RESEAU\chapitre_02_Cryptography_Basics.pdf', (10, 25, 80), 'D:\PDF_File\imagesPDF')
# main('D:\PDF_File\intro_prog_01_introduction_slides.pdf',  (30, 10, 80), 'D:\PDF_File\imagesPDF')
# main('D:\PDF_File\PDF_echo.pdf',  (30, 10, 80), 'D:\PDF_File\imagesPDF')
# PDF2jpg('D:\PDF_File\intro_prog_01_introduction_slides.pdf', 'D:\PDF_File\imagesPDF')