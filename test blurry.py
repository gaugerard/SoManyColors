from subprocess import call

def PDF2jpg(pdf_file, jpg_file, ImageMagickConvert_file = 'D:\ProgrammePDF\ImageMagick-6.4.7-Q16\convert'):
    """
    Converts each page of a PDF into png and saves them in jpg_file directory
    :param pdf_file: the pdf source's directory
    :param jpg_file: the file of destination
    :param ImageMagickConvert_file: the directory where ImageMagick\convert is located
    """
    # -density 300 = will set the dpi to 300
    # -quality 100 = will set the compression to 100 for PNG, JPG and MIFF file format ( 100 means NO compresion )
    call(ImageMagickConvert_file + ' -density 300 ' + pdf_file + ' -quality 100 ' + jpg_file + '\image.png')

PDF2jpg('D:\PDF_File\PDF_delta.pdf', 'D:\PDF_File\imagesPDF')