
import os
from PIL import Image
import imghdr
from PyPDF2 import PdfFileMerger
import ntpath
from subprocess import call
import os.path
import time
from threading import Thread
import time

def PDF2jpg(pdf_file, jpg_file, list_pages, dpi, ImageMagickConvert_file = 'D:\ProgrammePDF\ImageMagick-6.4.7-Q16\convert'):
    """
    Converts each page of a PDF into png and saves them in jpg_file directory.

    -density 300 = will set the dpi to 300.
    -quality 100 = will set the compression to 100 for PNG, JPG and MIFF file format ( 100 means NO compresion ).

    :param pdf_file: the pdf source's directory.
    :param jpg_file: the file of destination.
    :param list_pages: a list of pages (integer) to convert. ( exe : [1, 3, 10 ,45, 46, 47, 100] ).
    :param dpi: the dpi of each image.
    :param ImageMagickConvert_file: the directory where ImageMagick\convert is located.
    """

    stringDensity = ' -density ' + str(dpi) + ' '

    # if list_pages is NONE, it converts all the pdf.
    if list_pages is None:
        call(ImageMagickConvert_file + stringDensity + pdf_file + ' -quality 100 ' + jpg_file + '\image.png')
        return

    if len(list_pages) >= 1:
        pages = []
        for page in list_pages:
            pages.append(page - 1)

        liste = str(pages).replace(' ', '')
        call(ImageMagickConvert_file + stringDensity + pdf_file + liste + ' -quality 100 ' + jpg_file + '\im.png')

        # RENAME THE IMAGE WITH THE CORRECT PAGES THEY REPRESENTS
        renameImage(pages, jpg_file)
        return

def renameImage(pages, jpg_file):
    """
    Renames the produced PNG with the correct name ( its page number ).

    :param pages: list of pages ( ex : [0, 2, 4] ) where 0 is the first page of the PDF.
    :param jpg_file: the directory where the PNG are stored.
    """
    if len(pages) == 1:
        # REPLACE 0 BY THE PDF'S PAGE NUMBER
        name = jpg_file + '\im.png'
        newName = name.replace('im', 'image-' + str(pages[0]))
        # print name, newName

    else:
        for nbr in range(len(pages)):
            name = jpg_file + '\im-' + str(nbr) + '.png'
            newName = name.replace('im-' + str(nbr), 'image-' + str(pages[nbr]))

    pathexists(name)

    os.rename(name, newName)

    pathexists(newName)
    return


# Based on visionary-be/visionary-anderton
# https://github.com/visionary-be/visionary-anderton/blob/master/src/assets/js/contentscript/mutagen.js


def defineSVGMatrix(typeCVD, amountDalto, amountTransf):
    """
    Creates the color-matrix according to the given arguments.

    :param typeCVD: the type of colorblindness (typeCVD = "normal_vision", "protanope_vision",
    "deuteranope_vision", "tritanope_vision").
    :param amountDalto: the severity of colorblindness.
    :param amountTransf: the severity of the transformation.
    :return colorMatrix: the created color-matrix.
    """

    CVDMatrix = {}

    # Color Vision Deficiency
    CVDMatrix["normal_vision"] = [[1.0, 0.0, 0.0],
                                  [0.0, 1.0, 0.0],
                                  [0.0, 0.0, 1.0]]

    CVDMatrix["protanope_vision"] = [[0.0, 2.02344, -2.52581],  # reds are greatly reduced
                                     [0.0, 1.0, 0.0],
                                     [0.0, 0.0, 1.0]]

    CVDMatrix["deuteranope_vision"] = [[1.0, 0.0, 0.0],
                                       [0.494207, 0.0, 1.24827],  # greens are greatly reduced
                                       [0.0, 0.0, 1.0]]

    CVDMatrix["tritanope_vision"] = [[1.0, 0.0, 0.0],  # blues are greatly reduced
                                     [0.0, 1.0, 0.0],
                                     [-0.395913, 0.801109, 0.0]]

    valA = 0.0
    valB = 0.0
    valC = 0.0
    valD = 0.7
    valE = 1.0
    valF = 0.0
    valG = 0.7
    valH = 0.0
    valI = 1.0

    # Apply Daltonization
    cvd = CVDMatrix[typeCVD]

    cvda = cvd[0][0]
    cvdb = cvd[0][1]
    cvdc = cvd[0][2]
    cvdd = cvd[1][0]
    cvde = cvd[1][1]
    cvdf = cvd[1][2]
    cvdg = cvd[2][0]
    cvdh = cvd[2][1]
    cvdi = cvd[2][2]

    amountG = float(amountDalto) + float(amountTransf)
    amountB = float(amountDalto) - float(amountTransf)

    R1 = (valA - (1.44748099512696 * valA * cvda) - (0.279715681385635 * valA * cvdb) - (0.00242482044796114 * valA * cvdc) + 2.3337320435016 * valA * cvdd + 0.45097756096085 * valA * cvde + 0.0039094683786494 * valA * cvdf - (2.0872527906384 * valA * cvdg) - (0.4033471517229 * valA * cvdh) - (0.0034965662857356 * valA * cvdi) + 0.1832683754604 * valB * cvda + 0.035415344789275 * valB * cvdb + 0.0003070112186461 * valB * cvdc - (0.96599520599184 * valB * cvdd) - (0.18667188596529 * valB * cvde) - (0.00161823535922556 * valB * cvdf) + 2.0317036543392 * valB * cvdg + 0.3926126657002 * valB * cvdh + 0.0034035103616728 * valB * cvdi + 0.0065323859640912 * valC * cvda + 0.0012623383637997 * valC * cvdb + 1.09430542528908e-5 * valC * cvdc + 0.073704362532456 * valC * cvdd + 0.0142428578034985 * valC * cvde + 0.000123469562622454 * valC * cvdf - (12.401648348772 * valC * cvdg) - (2.39653268668825 * valC * cvdh) - (0.020775243755023 * valC * cvdi) + 1)
    R2 = (-(3.52238668926119 * valA * cvda) - (2.19807886050366 * valA * cvdb) - (0.0149187902480011 * valA * cvdc) + 5.6790429124849 * valA * cvdd + 3.5438994281586 * valA * cvde + 0.024053137118381 * valA * cvdf - (5.0792455801626 * valA * cvdg) - (3.1696072356564 * valA * cvdh) - (0.021512742953394 * valA * cvdi) + valB + 0.44597620863935 * valB * cvda + 0.2783030266059 * valB * cvdb + 0.0018888969608515 * valB * cvdc - (2.35071041825826 * valB * cvdd) - (1.46691642155364 * valB * cvde) - (0.0099562480663194 * valB * cvdf) + 4.9440689947988 * valB * cvdg + 3.0852528416232 * valB * cvdh + 0.020940213216772 * valB * cvdi + 0.0158962980837018 * valC * cvda + 0.0099197844701652 * valC * cvdb + 6.7327513345842e-5 * valC * cvdc + 0.179356597011509 * valC * cvdd + 0.111924095552826 * valC * cvde + 0.00075965068189921 * valC * cvdf - (30.1789116511205 * valC * cvdg) - (18.832579607337 * valC * cvdh) - (0.127820393544145 * valC * cvdi))
    R3 = (-(0.333438511456865 * valA * cvda) - (0.313023512252006 * valA * cvdb) - (0.118752790069611 * valA * cvdc) + 0.53759333721415 * valA * cvdd + 0.50467882022026 * valA * cvde + 0.19146171339981 * valA * cvdf - (0.4808149232271 * valA * cvdg) - (0.45137670317124 * valA * cvdh) - (0.17124030871794 * valA * cvdi) + 0.042217296473225 * valB * cvda + 0.03963251383919 * valB * cvdb + 0.015035521012515 * valB * cvdc - (0.22252451302971 * valB * cvdd) - (0.208900298667924 * valB * cvde) - (0.079251213861594 * valB * cvdf) + 0.4680187473998 * valB * cvdg + 0.43936398189512 * valB * cvdh + 0.16668300195972 * valB * cvdi + valC + 0.0015047859415503 * valC * cvda + 0.00141265440081732 * valC * cvdb + 0.00053592348477042 * valC * cvdc + 0.0169783734732515 * valC * cvdd + 0.0159388610322866 * valC * cvde + 0.0060467796955521 * valC * cvdf - (2.85681620618675 * valC * cvdg) - (2.6819056947317 * valC * cvdh) - (1.01744364716145 * valC * cvdi))
    G1 = (valD - (1.44748099512696 * valD * cvda) - (0.279715681385635 * valD * cvdb) - (0.00242482044796114 * valD * cvdc) + 2.3337320435016 * valD * cvdd + 0.45097756096085 * valD * cvde + 0.0039094683786494 * valD * cvdf - (2.0872527906384 * valD * cvdg) - (0.4033471517229 * valD * cvdh) - (0.0034965662857356 * valD * cvdi) + valD * amountG - (1.44748099512696 * valD * amountG * cvda) - (0.279715681385635 * valD * amountG * cvdb) - (0.00242482044796114 * valD * amountG * cvdc) + 2.3337320435016 * valD * amountG * cvdd + 0.45097756096085 * valD * amountG * cvde + 0.0039094683786494 * valD * amountG * cvdf - (2.0872527906384 * valD * amountG * cvdg) - (0.4033471517229 * valD * amountG * cvdh) - (0.0034965662857356 * valD * amountG * cvdi) + 0.1832683754604 * valE * cvda + 0.035415344789275 * valE * cvdb + 0.0003070112186461 * valE * cvdc - (0.96599520599184 * valE * cvdd) - (0.18667188596529 * valE * cvde) - (0.00161823535922556 * valE * cvdf) + 2.0317036543392 * valE * cvdg + 0.3926126657002 * valE * cvdh + 0.0034035103616728 * valE * cvdi + 0.1832683754604 * valE * amountG * cvda + 0.035415344789275 * valE * amountG * cvdb + 0.0003070112186461 * valE * amountG * cvdc - (0.96599520599184 * valE * amountG * cvdd) - (0.18667188596529 * valE * amountG * cvde) - (0.00161823535922556 * valE * amountG * cvdf) + 2.0317036543392 * valE * amountG * cvdg + 0.3926126657002 * valE * amountG * cvdh + 0.0034035103616728 * valE * amountG * cvdi + 0.0065323859640912 * valF * cvda + 0.0012623383637997 * valF * cvdb + 1.09430542528908e-5 * valF * cvdc + 0.073704362532456 * valF * cvdd + 0.0142428578034985 * valF * cvde + 0.000123469562622454 * valF * cvdf - (12.401648348772 * valF * cvdg) - (2.39653268668825 * valF * cvdh) - (0.020775243755023 * valF * cvdi) + 0.0065323859640912 * valF * amountG * cvda + 0.0012623383637997 * valF * amountG * cvdb + 1.09430542528908e-5 * valF * amountG * cvdc + 0.073704362532456 * valF * amountG * cvdd + 0.0142428578034985 * valF * amountG * cvde + 0.000123469562622454 * valF * amountG * cvdf - (12.401648348772 * valF * amountG * cvdg) - (2.39653268668825 * valF * amountG * cvdh) - (0.020775243755023 * valF * amountG * cvdi))
    G2 = (-(3.52238668926119 * valD * cvda) - (2.19807886050366 * valD * cvdb) - (0.0149187902480011 * valD * cvdc) + 5.6790429124849 * valD * cvdd + 3.5438994281586 * valD * cvde + 0.024053137118381 * valD * cvdf - (5.0792455801626 * valD * cvdg) - (3.1696072356564 * valD * cvdh) - (0.021512742953394 * valD * cvdi) - (3.52238668926119 * valD * amountG * cvda) - (2.19807886050366 * valD * amountG * cvdb) - (0.0149187902480011 * valD * amountG * cvdc) + 5.6790429124849 * valD * amountG * cvdd + 3.5438994281586 * valD * amountG * cvde + 0.024053137118381 * valD * amountG * cvdf - (5.0792455801626 * valD * amountG * cvdg) - (3.1696072356564 * valD * amountG * cvdh) - (0.021512742953394 * valD * amountG * cvdi) + valE + 0.44597620863935 * valE * cvda + 0.2783030266059 * valE * cvdb + 0.0018888969608515 * valE * cvdc - (2.35071041825826 * valE * cvdd) - (1.46691642155364 * valE * cvde) - (0.0099562480663194 * valE * cvdf) + 4.9440689947988 * valE * cvdg + 3.0852528416232 * valE * cvdh + 0.020940213216772 * valE * cvdi + valE * amountG + 0.44597620863935 * valE * amountG * cvda + 0.2783030266059 * valE * amountG * cvdb + 0.0018888969608515 * valE * amountG * cvdc - (2.35071041825826 * valE * amountG * cvdd) - (1.46691642155364 * valE * amountG * cvde) - (0.0099562480663194 * valE * amountG * cvdf) + 4.9440689947988 * valE * amountG * cvdg + 3.0852528416232 * valE * amountG * cvdh + 0.020940213216772 * valE * amountG * cvdi + 0.0158962980837018 * valF * cvda + 0.0099197844701652 * valF * cvdb + 6.7327513345842e-5 * valF * cvdc + 0.179356597011509 * valF * cvdd + 0.111924095552826 * valF * cvde + 0.00075965068189921 * valF * cvdf - (30.1789116511205 * valF * cvdg) - (18.832579607337 * valF * cvdh) - (0.127820393544145 * valF * cvdi) + 0.0158962980837018 * valF * amountG * cvda + 0.0099197844701652 * valF * amountG * cvdb + 6.7327513345842e-5 * valF * amountG * cvdc + 0.179356597011509 * valF * amountG * cvdd + 0.111924095552826 * valF * amountG * cvde + 0.00075965068189921 * valF * amountG * cvdf - (30.1789116511205 * valF * amountG * cvdg) - (18.832579607337 * valF * amountG * cvdh) - (0.127820393544145 * valF * amountG * cvdi) + 1)
    G3 = (-(0.333438511456865 * valD * cvda) - (0.313023512252006 * valD * cvdb) - (0.118752790069611 * valD * cvdc) + 0.53759333721415 * valD * cvdd + 0.50467882022026 * valD * cvde + 0.19146171339981 * valD * cvdf - (0.4808149232271 * valD * cvdg) - (0.45137670317124 * valD * cvdh) - (0.17124030871794 * valD * cvdi) - (0.333438511456865 * valD * amountG * cvda) - (0.313023512252006 * valD * amountG * cvdb) - (0.118752790069611 * valD * amountG * cvdc) + 0.53759333721415 * valD * amountG * cvdd + 0.50467882022026 * valD * amountG * cvde + 0.19146171339981 * valD * amountG * cvdf - (0.4808149232271 * valD * amountG * cvdg) - (0.45137670317124 * valD * amountG * cvdh) - (0.17124030871794 * valD * amountG * cvdi) + 0.042217296473225 * valE * cvda + 0.03963251383919 * valE * cvdb + 0.015035521012515 * valE * cvdc - (0.22252451302971 * valE * cvdd) - (0.208900298667924 * valE * cvde) - (0.079251213861594 * valE * cvdf) + 0.4680187473998 * valE * cvdg + 0.43936398189512 * valE * cvdh + 0.16668300195972 * valE * cvdi + 0.042217296473225 * valE * amountG * cvda + 0.03963251383919 * valE * amountG * cvdb + 0.015035521012515 * valE * amountG * cvdc - (0.22252451302971 * valE * amountG * cvdd) - (0.208900298667924 * valE * amountG * cvde) - (0.079251213861594 * valE * amountG * cvdf) + 0.4680187473998 * valE * amountG * cvdg + 0.43936398189512 * valE * amountG * cvdh + 0.16668300195972 * valE * amountG * cvdi + valF + 0.0015047859415503 * valF * cvda + 0.00141265440081732 * valF * cvdb + 0.00053592348477042 * valF * cvdc + 0.0169783734732515 * valF * cvdd + 0.0159388610322866 * valF * cvde + 0.0060467796955521 * valF * cvdf - (2.85681620618675 * valF * cvdg) - (2.6819056947317 * valF * cvdh) - (1.01744364716145 * valF * cvdi) + valF * amountG + 0.0015047859415503 * valF * amountG * cvda + 0.00141265440081732 * valF * amountG * cvdb + 0.00053592348477042 * valF * amountG * cvdc + 0.0169783734732515 * valF * amountG * cvdd + 0.0159388610322866 * valF * amountG * cvde + 0.0060467796955521 * valF * amountG * cvdf - (2.85681620618675 * valF * amountG * cvdg) - (2.6819056947317 * valF * amountG * cvdh) - (1.01744364716145 * valF * amountG * cvdi))
    B1 = (valG - (1.44748099512696 * valG * cvda) - (0.279715681385635 * valG * cvdb) - (0.00242482044796114 * valG * cvdc) + 2.3337320435016 * valG * cvdd + 0.45097756096085 * valG * cvde + 0.0039094683786494 * valG * cvdf - (2.0872527906384 * valG * cvdg) - (0.4033471517229 * valG * cvdh) - (0.0034965662857356 * valG * cvdi) + valG * amountB - (1.44748099512696 * valG * amountB * cvda) - (0.279715681385635 * valG * amountB * cvdb) - (0.00242482044796114 * valG * amountB * cvdc) + 2.3337320435016 * valG * amountB * cvdd + 0.45097756096085 * valG * amountB * cvde + 0.0039094683786494 * valG * amountB * cvdf - (2.0872527906384 * valG * amountB * cvdg) - (0.4033471517229 * valG * amountB * cvdh) - (0.0034965662857356 * valG * amountB * cvdi) + 0.1832683754604 * valH * cvda + 0.035415344789275 * valH * cvdb + 0.0003070112186461 * valH * cvdc - (0.96599520599184 * valH * cvdd) - (0.18667188596529 * valH * cvde) - (0.00161823535922556 * valH * cvdf) + 2.0317036543392 * valH * cvdg + 0.3926126657002 * valH * cvdh + 0.0034035103616728 * valH * cvdi + 0.1832683754604 * valH * amountB * cvda + 0.035415344789275 * valH * amountB * cvdb + 0.0003070112186461 * valH * amountB * cvdc - (0.96599520599184 * valH * amountB * cvdd) - (0.18667188596529 * valH * amountB * cvde) - (0.00161823535922556 * valH * amountB * cvdf) + 2.0317036543392 * valH * amountB * cvdg + 0.3926126657002 * valH * amountB * cvdh + 0.0034035103616728 * valH * amountB * cvdi + 0.0065323859640912 * valI * cvda + 0.0012623383637997 * valI * cvdb + 1.09430542528908e-5 * valI * cvdc + 0.073704362532456 * valI * cvdd + 0.0142428578034985 * valI * cvde + 0.000123469562622454 * valI * cvdf - (12.401648348772 * valI * cvdg) - (2.39653268668825 * valI * cvdh) - (0.020775243755023 * valI * cvdi) + 0.0065323859640912 * valI * amountB * cvda + 0.0012623383637997 * valI * amountB * cvdb + 1.09430542528908e-5 * valI * amountB * cvdc + 0.073704362532456 * valI * amountB * cvdd + 0.0142428578034985 * valI * amountB * cvde + 0.000123469562622454 * valI * amountB * cvdf - (12.401648348772 * valI * amountB * cvdg) - (2.39653268668825 * valI * amountB * cvdh) - (0.020775243755023 * valI * amountB * cvdi))
    B2 = (-(3.52238668926119 * valG * cvda) - (2.19807886050366 * valG * cvdb) - (0.0149187902480011 * valG * cvdc) + 5.6790429124849 * valG * cvdd + 3.5438994281586 * valG * cvde + 0.024053137118381 * valG * cvdf - (5.0792455801626 * valG * cvdg) - (3.1696072356564 * valG * cvdh) - (0.021512742953394 * valG * cvdi) - (3.52238668926119 * valG * amountB * cvda) - (2.19807886050366 * valG * amountB * cvdb) - (0.0149187902480011 * valG * amountB * cvdc) + 5.6790429124849 * valG * amountB * cvdd + 3.5438994281586 * valG * amountB * cvde + 0.024053137118381 * valG * amountB * cvdf - (5.0792455801626 * valG * amountB * cvdg) - (3.1696072356564 * valG * amountB * cvdh) - (0.021512742953394 * valG * amountB * cvdi) + valH + 0.44597620863935 * valH * cvda + 0.2783030266059 * valH * cvdb + 0.0018888969608515 * valH * cvdc - (2.35071041825826 * valH * cvdd) - (1.46691642155364 * valH * cvde) - (0.0099562480663194 * valH * cvdf) + 4.9440689947988 * valH * cvdg + 3.0852528416232 * valH * cvdh + 0.020940213216772 * valH * cvdi + valH * amountB + 0.44597620863935 * valH * amountB * cvda + 0.2783030266059 * valH * amountB * cvdb + 0.0018888969608515 * valH * amountB * cvdc - (2.35071041825826 * valH * amountB * cvdd) - (1.46691642155364 * valH * amountB * cvde) - (0.0099562480663194 * valH * amountB * cvdf) + 4.9440689947988 * valH * amountB * cvdg + 3.0852528416232 * valH * amountB * cvdh + 0.020940213216772 * valH * amountB * cvdi + 0.0158962980837018 * valI * cvda + 0.0099197844701652 * valI * cvdb + 6.7327513345842e-5 * valI * cvdc + 0.179356597011509 * valI * cvdd + 0.111924095552826 * valI * cvde + 0.00075965068189921 * valI * cvdf - (30.1789116511205 * valI * cvdg) - (18.832579607337 * valI * cvdh) - (0.127820393544145 * valI * cvdi) + 0.0158962980837018 * valI * amountB * cvda + 0.0099197844701652 * valI * amountB * cvdb + 6.7327513345842e-5 * valI * amountB * cvdc + 0.179356597011509 * valI * amountB * cvdd + 0.111924095552826 * valI * amountB * cvde + 0.00075965068189921 * valI * amountB * cvdf - (30.1789116511205 * valI * amountB * cvdg) - (18.832579607337 * valI * amountB * cvdh) - (0.127820393544145 * valI * amountB * cvdi))
    B3 = (-(0.333438511456865 * valG * cvda) - (0.313023512252006 * valG * cvdb) - (0.118752790069611 * valG * cvdc) + 0.53759333721415 * valG * cvdd + 0.50467882022026 * valG * cvde + 0.19146171339981 * valG * cvdf - (0.4808149232271 * valG * cvdg) - (0.45137670317124 * valG * cvdh) - (0.17124030871794 * valG * cvdi) - (0.333438511456865 * valG * amountB * cvda) - (0.313023512252006 * valG * amountB * cvdb) - (0.118752790069611 * valG * amountB * cvdc) + 0.53759333721415 * valG * amountB * cvdd + 0.50467882022026 * valG * amountB * cvde + 0.19146171339981 * valG * amountB * cvdf - (0.4808149232271 * valG * amountB * cvdg) - (0.45137670317124 * valG * amountB * cvdh) - (0.17124030871794 * valG * amountB * cvdi) + 0.042217296473225 * valH * cvda + 0.03963251383919 * valH * cvdb + 0.015035521012515 * valH * cvdc - (0.22252451302971 * valH * cvdd) - (0.208900298667924 * valH * cvde) - (0.079251213861594 * valH * cvdf) + 0.4680187473998 * valH * cvdg + 0.43936398189512 * valH * cvdh + 0.16668300195972 * valH * cvdi + 0.042217296473225 * valH * amountB * cvda + 0.03963251383919 * valH * amountB * cvdb + 0.015035521012515 * valH * amountB * cvdc - (0.22252451302971 * valH * amountB * cvdd) - (0.208900298667924 * valH * amountB * cvde) - (0.079251213861594 * valH * amountB * cvdf) + 0.4680187473998 * valH * amountB * cvdg + 0.43936398189512 * valH * amountB * cvdh + 0.16668300195972 * valH * amountB * cvdi + valI + 0.0015047859415503 * valI * cvda + 0.00141265440081732 * valI * cvdb + 0.00053592348477042 * valI * cvdc + 0.0169783734732515 * valI * cvdd + 0.0159388610322866 * valI * cvde + 0.0060467796955521 * valI * cvdf - (2.85681620618675 * valI * cvdg) - (2.6819056947317 * valI * cvdh) - (1.01744364716145 * valI * cvdi) + valI * amountB + 0.0015047859415503 * valI * amountB * cvda + 0.00141265440081732 * valI * amountB * cvdb + 0.00053592348477042 * valI * amountB * cvdc + 0.0169783734732515 * valI * amountB * cvdd + 0.0159388610322866 * valI * amountB * cvde + 0.0060467796955521 * valI * amountB * cvdf - (2.85681620618675 * valI * amountB * cvdg) - (2.6819056947317 * valI * amountB * cvdh) - (1.01744364716145 * valI * amountB * cvdi) + 1)

    # Color Matrix
    colorMatrix = [[R1, R2, R3, 0, 0],
                   [G1, G2, G3, 0, 0],
                   [B1, B2, B3, 0, 0],
                   [0, 0, 0, 1, 0]]

    return colorMatrix


def colorMatrixFilter(image, matrix, png_file):
    """
    Modifies the pixels of an image according to a color matrix.

    :param image: the directory where the image is saved.
    :param matrix: a color matrix.
    :param png_file: the file where the modified image will be saved.
    :return modified_image: the image modified.
    """

    im = Image.open(image)

    width = im.size[0]  # size in pixels
    height = im.size[1]
    imtype = imghdr.what(image)

    for x in range(width):
        for y in range(height):
            pixel_info = im.getpixel((x, y))  # return the state ( color_ RGB ) of the pixel
            r = pixel_info[0]
            g = pixel_info[1]
            b = pixel_info[2]

            # MODIFICATION : ( -50, -25, 0) = R'G'B'

            r2 = int((r * matrix[0][0]) + (g * matrix[0][1]) + (b * matrix[0][2]))
            g2 = int((r * matrix[1][0]) + (g * matrix[1][1]) + (b * matrix[1][2]))
            b2 = int((r * matrix[2][0]) + (g * matrix[2][1]) + (b * matrix[2][2]))

            im.putpixel((x, y), (r2, g2, b2))

    name = path_leaf(image)
    modified_name = (name.replace("." + imtype.lower(), "")) + '_m.' + (imtype.lower())  # name without the type
    directory = png_file + "\\" + modified_name
    im.save(directory)
    im.close()

    return modified_name


def change2pdf(png_file, jpeg_name, type_im):
    """
    Changes a the png ( jpeg_name ) in the file (png_file) into a pdf file.

    :param png_file: the directory where the image is saved ( exe : D:\Users\Images ).
    :param jpeg_name: name of the specific image to process ( exe : 'image1.png' ).
    :param type_im: the type of the image ( here it is '.png' ).
    :return pdf_name: the name of the PDF that has been created from the png.
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

    im.close()
    return pdf_name


def mergePDFFUll(pdf_file, png_file, dico_im_pdf):
    """
    Merges every PDF of a file into a single bigger PDF.

    :param pdf_file: the directory where the PDF is saved.
    :param png_file: the directory where the png from the PDF are saved.
    :param dico_im_pdf: a dictionary which contains all the name of the PDFs that needs to be merged.
    """

    pdf_m_name = str(path_leaf(pdf_file)).replace('.pdf', '_m.pdf')  # exe : PDF_delta.pdf --> PDF_delta_m.pdf
    merger = PdfFileMerger()

    for num in range(dico_im_pdf['nbr_pages']):
        if (dico_im_pdf[num] in os.listdir(png_file)) and ((dico_im_pdf[num]).endswith('.pdf')):

                merger.append(png_file + '\\' + dico_im_pdf[num])
                del dico_im_pdf[num]

    merger.write(pdf_m_name)
    merger.close()
    return


def mergePDFList(png_file, dico_im_pdf, page, merger):
    """
    Merges a PDF with another PDF.

    :param png_file: the directory where the png from the PDF are saved.
    :param dico_im_pdf: a dictionary which contains all the name of the PDFs that needs to be merged.
    :param page: the number of the page we will merge.
    :param merger: the merger object that allows the merging of PDFs.
    """

    if (dico_im_pdf[page] in os.listdir(png_file)) and ((dico_im_pdf[page]).endswith('.pdf')):
            merger.append(png_file + '\\' + dico_im_pdf[page])
            del dico_im_pdf[page]


def path_leaf(path):
    """
    Gives the name at the end of a directory.

    :param path: a directory ( exe : 'C\User\Program\Images\image1.png' ).
    :return tail : the tail of the path ( exe : 'image1.png' ).
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
    :param pdf_file: the directory of the source PDF.
    """

    pdf_name = str(path_leaf(pdf_file)).replace('.pdf', '_m.pdf')  # ( exe : PDF_delta.pdf --> PDF_delta_m.pdf )
    current_dir = os.getcwd() + '\\' + pdf_name                    # ( exe : current directory of the PDF_delta_m.pdf )
    final_dir = pdf_file.replace('.pdf', '_m.pdf')                 # ( exe : directory of PDF_delta.pdf )

    # print "current dir : ", current_dir
    # print "final dir : ", final_dir
    pathexists(current_dir)
    os.rename(current_dir, final_dir)
    pathexists(final_dir)
    return


def setup(pdf_file, png_file):
    """
    Deletes the PDF on the png_file path.

    :param pdf_file: the path where the pdf is stored.
    :param png_file: the path where the images and pdf will be manipulated by the program.
    """

    pdf_m_name = path_leaf(pdf_file).replace('.pdf', '_m.pdf')
    pdf_m_path = pdf_file.replace(path_leaf(pdf_file), '')

    if pdf_m_name in os.listdir(pdf_m_path):
        os.remove(pdf_m_path + '\\' + pdf_m_name)

    current_dir = os.getcwd()
    if pdf_m_name in os.listdir(current_dir):
        os.remove(current_dir + '\\' + pdf_m_name)

    for image in os.listdir(png_file):
        if image.endswith('.pdf') or image.endswith('.png'):
            os.remove(png_file + '\\' + image)
    return


def pathexists(path):
    """
    Checks if a path to a directory exists or not.

    :param path: the directory we want to check.
    :return: True if path exists, else False.
    """

    if not os.path.exists(path):
        raise Exception('NotExistingPathException')

    return True


def PDFProcess2PDF(png_file, page, dico_im_pdf, color_matrix):
    """
    Create a new pdf for a selected page of a src PDF ( ONLY ONE PAGE ).

    :param png_file: file where all the created .png will be saved.
    :param page: a page we want to process ( INTEGER ), ( exe :  page = 1 --> image-0.png ).
    :param dico_im_pdf: a dictionary that holds all pdf images name.
    :param color_matrix: a color_matrix used to modify the color of an image.
    :return dico_im_pdf: a dictionary that holds all the pdf images name.
    """

    # TEST IF IT IS A PNG OR NOT AND THEN CONVERT ITS COLOR

    liste_im_m = []  # list of modified images ( will be completed after the FOR )
    im_name = 'image-' + str(page-1) + '.png'
    num = page
    if im_name in os.listdir(png_file):
        if im_name.endswith('.png'):
            image = png_file + "\\" + str(im_name)
            liste_im_m.append(colorMatrixFilter(image, color_matrix, png_file))
            dico_im_pdf[num] = ''

    # CHANGES .png INTO .pdf

    image_m = 'image-' + str(page-1) + '_m.png'
    direct_name = png_file + '\\' + image_m
    type_im_m = imghdr.what(direct_name)
    dico_im_pdf[num] = (change2pdf(png_file, image_m, type_im_m))

    # DELETES THE .png SINCE WE DON'T NEED THEM ANYMORE

    png = 'image-' + str(page-1) + '.png'
    if png.endswith('.png'):
        os.remove(png_file + '\\' + png)

    return dico_im_pdf


def main(pdf_file, dpi, typeCVD, amountDalto, amountTransf, list_pages=None, png_file="C:\Users\gauth\PycharmProjects\untitled\pdf\SoManyColors\TraitementDir"):
    """
    VERSION 6.1:
    ----------
    Creates a new pdf from an entire pdf or a selection of pages. It applies a color-matrix on every page of the pdf to
    make it readable for a specific colorblind type.

    :param pdf_file: the directory of the pdf that you want to convert into .png.
    :param dpi: the dpi of each image.
    :param png_file: file where all the created .png will be saved.
    :param typeCVD: the type of colorblindness (typeCVD = "normal_vision", "protanope_vision",
    "deuteranope_vision", "tritanope_vision").
    :param amountDalto: the severity of colorblindness ( integer / float ).
    :param amountTransf: the severity of the transformation( integer / float ).
    :param list_pages: a list of pages (integer) to convert ( if list_pages == None, it means that all the PDF should
    be converted ).
    """
    print "<<<      DEBUT     >>>"
    # print pdf_file, dpi, typeCVD, amountDalto, amountTransf
    # print'ok'
    t1 = time.time()
    # print pdf_file
    pathexists(pdf_file)
    pathexists(png_file)

    # CLEANS THE DIRECTORY WHERE .png WILL BE MANIPULATED
    setup(pdf_file, png_file)

    # CREATES PNG OUT OF A PDF
    PDF2jpg(pdf_file, png_file, list_pages, dpi)

    # ----------------------------------------------------------
    # TEST IF IT IS A PNG OR NOT AND THEN CONVERT ITS COLOR:

    liste_im_m = []  # list of modified images ( will be completed after the FOR )
    dico_im_pdf = {}

    # CREATES COLOR_MATRIX WITH THE INFO GIVEN BY THE USER
    color_matrix = defineSVGMatrix(typeCVD, amountDalto, amountTransf)

    # ----------------------------------------------------------
    # CHANGES .png INTO .pdf:

    if list_pages is None:
        num = 0
        for element in os.listdir(png_file):
            if element.endswith('.png'):
                image = png_file + "\\" + str(element)
                liste_im_m.append(colorMatrixFilter(image, color_matrix, png_file))
                dico_im_pdf[num] = ''
                num = num + 1

        dico_im_pdf['nbr_pages'] = num

        for num in range(dico_im_pdf['nbr_pages']):
            image_m = 'image-' + str((num)) + '_m.png'
            direct_name = png_file + '\\' + image_m
            type_im_m = imghdr.what(direct_name)
            dico_im_pdf[num] = (change2pdf(png_file, image_m, type_im_m))

        # ----------------------------------------------------------
        # DELETES THE .png SINCE WE DON'T NEED THEM ANYMORE:

        for png in os.listdir(png_file):
            if png.endswith('.png'):
                os.remove(png_file + '\\' + png)

        mergePDFFUll(pdf_file, png_file, dico_im_pdf)

    else:
        for page in list_pages:
            dico_im_pdf = PDFProcess2PDF(png_file, page, dico_im_pdf, color_matrix)

        # ----------------------------------------------------------
        # DELETES THE .png SINCE WE DON'T NEED THEM ANYMORE:

        for png in os.listdir(png_file):
            if png.endswith('.png'):
                os.remove(png_file + '\\' + png)

        # MERGES THE PDF
        pdf_m_name = str(path_leaf(pdf_file)).replace('.pdf', '_m.pdf')  # exe : PDF_delta.pdf --> PDF_delta_m.pdf
        merger = PdfFileMerger()

        for page in list_pages:
            mergePDFList(png_file, dico_im_pdf, page, merger)

        merger.write(pdf_m_name)
        merger.close()

    # ----------------------------------------------------------
    # MERGES THE PDF:

    t2 = time.time()

    # ----------------------------------------------------------
    # MOVES THE NEW PDF IN THE PDF, THAT WE WANT TO MODIFY, DIRECTORY

    movePDF(pdf_file)
    newDirectory = pdf_file.replace(path_leaf(pdf_file), '') + str(path_leaf(pdf_file)).replace('.pdf', '_m.pdf')
    print "<<<      LE FICHIER SE TROUVE A : " + str(newDirectory) + "      >>>"
    return newDirectory






# pdf_file, dpi, typeCVD, amountDalto, amountTransf, list_pages=None, png_file

#pdfs = ['D:\PDF_File\PDF_beta.pdf', 'D:\PDF_File\PDF_charlie.pdf', 'D:\PDF_File\PDF_delta.pdf', 'D:\PDF_File\PDF_alpha.pdf']
#for e in pdfs:
#    main(e, 72, "protanope_vision", 3, 2)

# main("D:\PDF_File\PDF_delta.pdf", 72, "protanope_vision", 3, 2)