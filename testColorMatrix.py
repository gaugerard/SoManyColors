from subprocess import call
import time

def PDF2jpg(PNG, ImageMagickConvert_file = 'D:\ProgrammePDF\ImageMagick-6.4.7-Q16\convert'):
    """
    Converts each page of a PDF into png and saves them in jpg_file directory

    -density 300 = will set the dpi to 300
    -quality 100 = will set the compression to 100 for PNG, JPG and MIFF file format ( 100 means NO compresion )

    :param pdf_file: the pdf source's directory
    :param jpg_file: the file of destination
    :param dpi: the dpi of each image
    :param ImageMagickConvert_file: the directory where ImageMagick\convert is located
    """
    arg = ImageMagickConvert_file + """ helix_nebula.jpg -recolor ' .1 .0 .0
                                                                    .1 .0 .0
                                                                    .1 .0 .0 ' gray_recolor.png"""
    call(arg)
    print "ok"
    return


PNG = "helix_nebula.jpg"
time1 = time.time()
PDF2jpg(PNG)
time2 = time.time()
print "time : ",(time2 - time1)
