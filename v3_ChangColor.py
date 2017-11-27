from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTFigure, LTImage
from binascii import b2a_hex
import os
from PIL import Image
import imghdr


"""VERSION 3:
   ----------
   - This version detects the different LTImages of a PDF ( see PDF doc ) recursively and save their type ( LTImage )
     and coord ( start_x, start_y, end_x, end_y ). (coord = bbox or magic coord)
     
   - It saves the pdf_directory, image_directory, the type, the coord and the page of each LTImage detected in a 
     dictionary
     ( dico_image ).
        ex : {'Image13.jpeg': ['LTImage', (210.95, 191.79, 489.84999999999997, 348.53)] }
        
   - It also copies the existing images in a chosen directory ( C:\Users\gauth\PycharmProjects\untitled\pdf )
     with a generated names ( its file name ).
        ex : 'Image13.jpeg' 
        
    | The dictionary ( dico_image ) will allow us to replace the modified image back on the pdf, at the same place. 
   """


def parse_layout(layout, page, saving_directory, dico_image):
    """Function to recursively parse the layout tree."""
    for lt_obj in layout:

        # list that will contains the type, coord of the image and its page
        caract_lt_obj = []
        if isinstance(lt_obj, LTImage) or isinstance(lt_obj, LTImage):

            # gives the page of the objext
            page_lt_obj = page
            caract_lt_obj.append(page_lt_obj)

            # print the type of the object ( here we are interested in LTImage ) <------
            type_lt_obj = lt_obj.__class__.__name__
            caract_lt_obj.append(type_lt_obj)
            # print(type_lt_obj)

            # gives the location of start and end (x,y) of the object ( we want LTImage) <------
            loc_lt_obj = lt_obj.bbox
            caract_lt_obj.append(loc_lt_obj)
            # print(lt_obj.bbox)

            # saves the images but still need the data to store
            # = NONE ????
            im_name = save_image(lt_obj, page, saving_directory, caract_lt_obj, dico_image)
            print "name " + im_name

        # if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
            # print(lt_obj.get_text())
            # Print the text stuff

        elif isinstance(lt_obj, LTFigure):
            parse_layout(lt_obj, page, saving_directory, dico_image)  # Recursive


# Within parse_lt_objs(), the following function is called if an LTImage is found; it was based on studying the
# dumppdf.py source code and how it handled image extraction requests:


def save_image (lt_image, page_number, saving_directory, caract_lt_obj, dico_image):
    """Try to save the image data from this LTImage object, and return the file name, if successful"""
    result = None
    if lt_image.stream:
        file_stream = lt_image.stream.get_rawdata()
        file_ext = determine_image_type(file_stream[0:4])
        if file_ext:
            file_name = lt_image.name + file_ext
            if write_file(saving_directory, file_name, lt_image.stream.get_rawdata(), flags='wb'):
                result = file_name
                dico_image[str(result)] = caract_lt_obj
    # print "\n"
    return result

# The save_image() function needs the following two supporting functions defined:


def determine_image_type (stream_first_4_bytes):
    """Find out the image file type based on the magic number comparison of the first 4 (or 2) bytes"""
    file_type = None
    bytes_as_hex = b2a_hex(stream_first_4_bytes)
    if bytes_as_hex.startswith('ffd8'):
        file_type = '.jpeg'
    elif bytes_as_hex == '89504e47':
        file_type = ',png'
    elif bytes_as_hex == '47494638':
        file_type = '.gif'
    elif bytes_as_hex.startswith('424d'):
        file_type = '.bmp'
    return file_type


def write_file(saving_directory, filename, filedata, flags='wb',):
    """Write the file data to the folder and filename combination
    (flags: 'w' for write text, 'wb' for write binary, use 'a' instead of 'w' for append)"""
    result = False

    if os.path.isdir(saving_directory):
        try:
            # FAILS THIS TEST
            file_obj = open(os.path.join(saving_directory, filename), flags)
            file_obj.write(filedata)
            file_obj.close()
            result = True
        except IOError:
            print "ERROR"
            pass

    return result


def change_color(dico_image, R_value, G_value, B_value):
    """change_color modifies all the pixels of all the images stocked in the dictionary. It ADDS the R_value to the Red
    value of the pixel, ...
    """
    for keys in dico_image.keys():

        if keys != 'image_directory' and keys != 'pdf_directory':

            direct_name = dico_image['image_directory'] + "\\" + keys
            # should be : 'C:\\Users\\gauth\\PycharmProjects\\untitled\\pdf' + keys BUT does not work
            # im = Image.open('C:\\Users\\gauth\\PycharmProjects\\untitled\\pdf' + keys)
            print keys
            im = Image.open(direct_name)  # <---------- FOR SOME REASONS, IT IS ONLY WORKING IN THE CURRENT DIRECTORY ?!!!

            # INFORMATION :
            # -------------
            imtype = imghdr.what(direct_name)  # gives the type of a image so we can remove it from the name and modify it
            print imtype                # image13_m.jpeg and not image13.jpeg_m
            width = im.size[0]          # in pixels
            height = im.size[1]         # in pixels
            file_name = keys.replace("." + imtype.lower(), "")  # name without the type
            format_desc = im.format_description

            for x in range(width):
                for y in range(height):
                    pixel_info = im.getpixel((x, y))  # return the state ( color_ RGB ) of the pixel

                    # MODIFICATION : ( -50, -25, 0) = R'G'B'
                    # --------------
                    r2 = pixel_info[0] + R_value  # R
                    g2 = pixel_info[1] + G_value  # G
                    b2 = pixel_info[2] + B_value    # B
                    im.putpixel((x, y), (r2, g2, b2))

            directory = dico_image['image_directory'] + "\\" + file_name + '_m.' + (imtype.lower())
            print directory
            im.save(directory)


def test(directory, saving_directory, color_blind_filter):
    dico_image = {'pdf_directory': directory, 'image_directory': saving_directory}
    fp = open(directory, 'rb')
    # fp = open("D:\Cours 2017-2018 Q1\AMSI\00-Intro-Course.pdf")  problem if 00 in file name <-------------------------
    # fp = open("D:\Cours 2017-2018 Q1\AMSI\Intro-Course.pdf")
    parser = PDFParser(fp)
    doc = PDFDocument(parser)

    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)
        layout = device.get_result()
        parse_layout(layout, page, saving_directory, dico_image)

    # modifies the images' pixel color
    change_color(dico_image, color_blind_filter[0], color_blind_filter[1], color_blind_filter[2])
    print dico_image



# TEST ZONE :
# -----------
directory = 'D:\PDF_File\PDF_beta.pdf'
# directory = 'D:\PDF_File\PDF_delta.pdf'
saving_directory = 'C:\Users\gauth\PycharmProjects\untitled\pdf'
# directory = 'D:\Cours 2017-2018 Q1\RESEAU\chapitre_01_Computer_Networks_and_the_Internet.pdf'
# saving_directory = 'C:\Users\gauth\PycharmProjects\untitled\pdf\images_des_pdf'
color_blind_filter = (80, 60, 15)
print (test(directory, saving_directory, color_blind_filter))

