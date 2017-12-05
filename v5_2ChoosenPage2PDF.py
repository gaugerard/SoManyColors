
import os
from PIL import Image
import imghdr
from PyPDF2 import PdfFileMerger
import ntpath
from subprocess import call


def PDF2jpg(pdf_file, jpg_file, page, dpi, ImageMagickConvert_file = 'D:\ProgrammePDF\ImageMagick-6.4.7-Q16\convert'):
    """
    Converts each page of a PDF into png and saves them in jpg_file directory

    -density 300 = will set the dpi to 300
    -quality 100 = will set the compression to 100 for PNG, JPG and MIFF file format ( 100 means NO compresion )

    :param pdf_file: the pdf source's directory
    :param jpg_file: the file of destination
    :param page: the page of the PDF that needs to be converted
    :param dpi: the dpi of each image
    :param ImageMagickConvert_file: the directory where ImageMagick\convert is located
    """
    stringDensity = ' -density ' + str(dpi) + ' '
    call(ImageMagickConvert_file + stringDensity + pdf_file + '[' + str(page-1) + ']' + ' -quality 100 ' + jpg_file + '\im-0.png')

    # RENAME THE IMAGE WITH THE CORRECT PAGES THEY REPRESENTS
    renameImage((page - 1), jpg_file)
    return


def renameImage(page, jpg_file):
    """
    Renames the produced PNG with the correct name ( its page number )
    :param page: int that represents a page of a PDF ( ex : 0 ) where 0 is the first page of the PDF
    :param jpg_file: the directory where the PNG are stored
    """

    # REPLACE 0 BY THE PDF'S PAGE NUMBER
    name = jpg_file + '\im-0.png'
    newName = name.replace('im-0', 'image-' + str(page))

    pathexists(name)
    os.rename(name, newName)
    pathexists(newName)
    return


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
    width = im.size[0]  # size in pixels
    height = im.size[1]
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
    im.close()
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
        im.save(new_filename, "pdf", resolution=100.0)

    im.close()
    return pdf_name


def mergePDF(pdf_file, png_file, dico_im_pdf):
    """
    Merges every PDF of a file into a single bigger PDF
    :param pdf_file: the directory where the PDF is saved
    :param png_file: the directory where the png from the PDF are saved
    :param dico_im_pdf: a dictionary which contains all the name of the PDFs that needs to be merged
    """

    pdf_m_name = str(path_leaf(pdf_file)).replace('.pdf', '_m.pdf')  # exe : PDF_delta.pdf --> PDF_delta_m.pdf
    merger = PdfFileMerger()

    if (dico_im_pdf[0] in os.listdir(png_file)) and ((dico_im_pdf[0]).endswith('.pdf')):
            merger.append(png_file + '\\' + dico_im_pdf[0])
            del dico_im_pdf[0]

    merger.write(pdf_m_name)
    merger.close()
    return


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
    return


def setup(pdf_file, png_file):
    """
    Deletes the PDF on the png_file path
    :param pdf_file: the path where the pdf is stored
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
    return

def pathexists(path):
    """
    Checks if a path to a directory exists or not.
    :param path:
    :return: True if path exists, else False
    """
    if not os.path.exists(path):
        raise Exception('NotExistingPathException')
    return True


def colorfilterok(colorfilter):
    """
    Checks if the color filter is correct or not. it checks its length, its variables ( must be int/float ) and its
    variables values ( between 0 and 255 ).
    :param colorfilter: a list of 3 int that represents the RGB of an image
    :return: True if colorfilter is correct, else False
    """
    if len(colorfilter) != 3:
        raise Exception('SizeTupleException')

    for val in colorfilter:
        if type(val) != int and type(val) != float and type(val) != long:
            raise Exception('NotIntegerInTupleException')

        if val > 255 or val < -255:
            raise Exception('TupleValuesException')

    return True


def main(pdf_file, png_file, page, color_blind_filter, dpi):
    """
    Converts a page from the PDF into a PDF for colorblind. It changes every pixels of the selected page to suit a specific colorblind
    type.

    VERSION 5.2:
    ----------
    Create a new pdf for a selected page of a src PDF ( ONLY ONE PAGE )
    :param pdf_file: the directory of the pdf that you want to convert into .png
    :param png_file: file where all the created .png will be saved
    :param color_blind_filter: a list of 3 integer that are added to the RGB of a pixel ( exe : (80, 60, 30) )
    :param page: the page we want to process ( INTEGER ), ( exe :  page = 1 --> image-0.png )
    :param dpi: the dpi of each image
    """
    colorfilterok(color_blind_filter)
    pathexists(pdf_file)
    pathexists(png_file)

    # CLEANS THE DIRECTORY WHERE .png WILL BE MANIPULATED
    setup(pdf_file, png_file)

    # PRINT INFORMATION ABOUT THE PROCESS
    print '\n'
    print 'PDF source path : ', pdf_file
    print 'File of processes : ', png_file
    print 'Page to process : ', page
    print 'Filter to apply : ', color_blind_filter

    # CREATES PNG OUT OF A PDF
    PDF2jpg(pdf_file, png_file, page, dpi)

    # ---------------------------------------------------------
    # TEST IF IT IS A PNG OR NOT AND THEN CONVERT ITS COLOR

    liste_im_m = []  # list of modified images ( will be completed after the FOR )
    dico_im_pdf = {}

    im_name = 'image-' + str(page-1) + '.png'
    num = 0
    if im_name in os.listdir(png_file):
        if im_name.endswith('.png'):
            liste_im_m.append(change_color(png_file, im_name, color_blind_filter[0], color_blind_filter[1], color_blind_filter[2]))
            dico_im_pdf[num] = ''

    dico_im_pdf['nbr_pages'] = (num + 1)

    # ---------------------------------------------------------
    # CHANGES .png INTO .pdf

    image_m = 'image-' + str(page-1) + '_m.png'
    direct_name = png_file + '\\' + image_m
    type_im_m = imghdr.what(direct_name)
    dico_im_pdf[num] = (change2pdf(png_file, image_m, type_im_m))

    # ---------------------------------------------------------
    # DELETES THE .png SINCE WE DON'T NEED THEM ANYMORE

    png = 'image-' + str(page-1) + '.png'
    if png.endswith('.png'):
        os.remove(png_file + '\\' + png)

    # ---------------------------------------------------------
    # MERGES THE PDF

    mergePDF(pdf_file, png_file, dico_im_pdf)

    # MOVES THE NEW PDF IN THE PDF, THAT WE WANT TO MODIFY, DIRECTORY
    movePDF(pdf_file)
    return


# main('D:\PDF_File\PDF_charlie.pdf', 'D:\PDF_File\imagesPDF', 1, (25, 50, 100), 72)
# PDF2jpg('D:\PDF_File\PDF_delta.pdf', 'D:\PDF_File\imagesPDF', 4, 72)

