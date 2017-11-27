from subprocess import call


def PDF2jpg(pdf_file, jpg_file, ImageMagickConvert_file = 'D:\ProgrammePDF\ImageMagick-6.4.7-Q16\convert'):

    call(ImageMagickConvert_file + ' ' + pdf_file + ' ' + jpg_file)

    return jpg_file

# ImageMagickConvert_file = 'D:\ProgrammePDF\ImageMagick-6.4.7-Q16\convert'
# pdf_file = 'D:\PDF_File\PDF_delta.pdf'
# jpg_file = 'D:\PDF_File\delt.png'
# PDF2jpg(ImageMagickConvert_file, pdf_file, jpg_file)
