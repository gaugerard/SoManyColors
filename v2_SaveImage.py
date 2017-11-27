from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTFigure, LTImage
from binascii import b2a_hex
import os

# dans chaque LTPage, checker si il y a des LTImage, si oui, prendre leur bbox ( la position ) et la retirer.
# layout = LTPage ( je pense )


def parse_layout(layout, page):
    """Function to recursively parse the layout tree."""
    for lt_obj in layout:

        if isinstance(lt_obj, LTImage) or isinstance(lt_obj, LTImage):
            # print the type of the object ( here we are interested in LTImage ) <------
            print(lt_obj.__class__.__name__)
            # gives the location of start and end (x,y) of the object ( we want LTImage) <------
            print(lt_obj.bbox)
            # saves the images but still need the data to store
            # = NONE ????
            save_image(lt_obj, page, 'C:\Users\gauth\PycharmProjects')

        # if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
            # print(lt_obj.get_text())
            # Print the text stuff

        elif isinstance(lt_obj, LTFigure):
            parse_layout(lt_obj, page)  # Recursive


# Within parse_lt_objs(), the following function is called if an LTImage is found; it was based on studying the
# dumppdf.py source code and how it handled image extraction requests:


def save_image (lt_image, page_number, images_folder):
    """Try to save the image data from this LTImage object, and return the file name, if successful"""
    result = None
    if lt_image.stream:
        file_stream = lt_image.stream.get_rawdata()
        file_ext = determine_image_type(file_stream[0:4])
        print file_stream[0:4]
        if file_ext:
            file_name = lt_image.name + file_ext
            if write_file(images_folder, file_name, lt_image.stream.get_rawdata(), flags='wb'):
                result = file_name
    print "file name : " + result
    print "file directory : " + images_folder
    print "\n"
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


def write_file(folder, filename, filedata, flags='wb'):
    """Write the file data to the folder and filename combination
    (flags: 'w' for write text, 'wb' for write binary, use 'a' instead of 'w' for append)"""
    result = False

    if os.path.isdir(folder):
        try:
            # FAILS THIS TEST
            file_obj = open(os.path.join(folder, filename), flags)
            file_obj.write(filedata)
            file_obj.close()
            result = True
        except IOError:
            print "ERROR"
            pass

    return result


def test(directory):
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
        parse_layout(layout, page)


test('D:\PDF_File\PDF_alpha.pdf')
test('D:\PDF_File\PDF_beta.pdf')
test('D:\PDF_File\PDF_charlie.pdf')