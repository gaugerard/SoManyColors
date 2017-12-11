import os
from PIL import Image
import imghdr
from PyPDF2 import PdfFileMerger
import ntpath
from subprocess import call
import os.path
import time

# Based on visionary-be/visionary-anderton
# https://github.com/visionary-be/visionary-anderton/blob/master/src/assets/js/contentscript/mutagen.js


def defineSVGMatrix(typeCVD, amountDalto, amountTransf):

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


def path_leaf(path):
    """
    :param path: a directory ( exe : 'C\User\Program\Images\image1.png' )
    :return tail : the tail of the path ( exe : 'image1.png' )
    """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def colorMatrixFilter(image, matrix, num):
    """
    Modifies the pixels of an image according to a color matrix.
    :param image: the directory where the image is saved.
    :param matrix: a color matrix.
    :return modified_image: the image modified.
    """
    im = Image.open(image)

    # INFORMATION :
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
    modified_name = (name.replace("." + imtype.lower(), "")) + '_m' + str(num) + '.' + (imtype.lower())  # name without the type
    directory = image.replace(name, modified_name)
    im.save(directory)
    im.close()

    return modified_name


def test(image, vision_type, amount1, amount2, num):
    matrix = defineSVGMatrix(vision_type, amount1, amount2)
    colorMatrixFilter(image, matrix, num)


type_vison = ["normal_vision", "protanope_vision", "deuteranope_vision", "tritanope_vision"]
num = 0
for vision in type_vison:
    test("D:\PDF_File\imagesPDF\Capture.png", vision, 10, 1, num)
    num += 1
    time.sleep(1)