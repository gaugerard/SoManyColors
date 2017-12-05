from Tkinter import *
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
import tkMessageBox
import v5_1PDFintoJPG, v5_2ChoosenPage2PDF, SoManyColors

root = Tk()
root.title("SoManyColors")
root.geometry("840x640")

heading = Label(root, text="Welcome to PDF convert for colorblind", font=("arial", 15, 'bold'), fg="steelblue").pack()

label1 = Label(root, text="Enter your PDF directory : ", font=("arial", 10, "bold"), fg="black").place(x=10, y=200)
label2 = Label(root, text="Enter the process's directory : ", font=("arial", 10, "bold"), fg="black").place(x=10, y=220)
label3 = Label(root, text="Enter dpi value : ", font=("arial", 10, "bold"), fg="black").place(x=10, y=240)
label4 = Label(root, text="Enter RED value : ", font=("arial", 10, "bold"), fg="black").place(x=10, y=260)
label5 = Label(root, text="Enter GREEN value : ", font=("arial", 10, "bold"), fg="black").place(x=10, y=280)
label6 = Label(root, text="Enter BLUE value : ", font=("arial", 10, "bold"), fg="black").place(x=10, y=300)
label7 = Label(root, text="Enter test page : ", font=("arial", 10, "bold"), fg="black").place(x=10, y=320)

nameSrc = StringVar()
entry_box1 = Entry(root, textvariable=nameSrc, width=90, bg='lightgreen').place(x=225, y=200)
nameDest = StringVar()
entry_box2 = Entry(root, textvariable=nameDest, width=90, bg='lightgreen').place(x=225, y=220)

dpi = IntVar()
dpi_entry = Entry(root, textvariable=dpi, width=4, bg='lightgreen').place(x=225, y=240)
red = IntVar()
red_entry = Entry(root, textvariable=red, width=4, bg='lightgreen').place(x=225, y=260)
green = IntVar()
green_entry = Entry(root, textvariable=green, width=4, bg='lightgreen').place(x=225, y=280)
blue = IntVar()
blue_entry = Entry(root, textvariable=blue, width=4, bg='lightgreen').place(x=225, y=300)

numTest = IntVar()
numTest_entry = Entry(root, textvariable=numTest, width=4, bg='lightgreen').place(x=225, y=320)


def add_value():
    """
    Adds the given RBG value to the colorfilter
    :return tuple: the colorfilter with the givven RBG value ( ex: (0, 100, 255) )
    """

    tuple = (int(red.get()), int(green.get()), int(blue.get()))
    return tuple


def is_valid():
    """
    Shows if a path to a directory is valid or not.
    """

    if v5_1PDFintoJPG.pathexists(str(nameSrc.get())):
        print("VALID " + str(nameSrc.get()))

    if v5_1PDFintoJPG.pathexists(str(nameDest.get())):
        print("VALID" + str(nameDest.get()))


def convertFull():
    """
    Converts all the PDF into another PDF for colorblind.
    """

    tuple = add_value()
    page = int(numTest.get())
    SoManyColors.main(str(nameSrc.get()), str(nameDest.get()), page, tuple, dpi.get())


def convertTest():
    """
    Converts a page of the PDF to test the colorfiler.
    """

    tuple = add_value()
    page = int(numTest.get())
    v5_2ChoosenPage2PDF.main(str(nameSrc.get()), str(nameDest.get()), page, tuple, dpi.get())


def estimateTime():
    """
    IMPROVE THIS METHOD BY KNOWING THE PAGE SIZE
                            72dpi       150dpi      300dpi
    TIME for a page 4A :    1.6s        6.2s        23.2s
    TIME for smaller p :    0.5s        1.7s        7.1s
    TIME for larger p :     2.3s        14.2s       49.1s

                                -> x4 ->     -> x4 ->
    """

    fp = open(str(nameSrc.get()), 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser)
    num_pages = 0

    for page in PDFPage.create_pages(document):
        num_pages += 1

    averageT72dpi = (1.6 + 0.5 + 2.3)/3
    averageT150dpi = (6.2 + 1.4 + 14.2)/3
    averageT300dpi = (23.2 + 7.1 + 49.1)/3
    time72dpi = (num_pages * averageT72dpi)
    time150dpi = (num_pages * averageT150dpi)
    time300dpi = (num_pages * averageT300dpi)

    print "Estimate Time ( 72 dpi ) : ", time72dpi
    print "Estimate Time ( 150 dpi ) : ", time150dpi
    print "Estimate Time ( 300 dpi ) : ", time300dpi

    parser.close()
    fp.close()


def Manual():
   tkMessageBox.showinfo("MANUAL", "1) Choose your PDF by giving its directory.\n 2) Choose the directory where the modification will happen.\n 3) Select the quality of the images (72 = low, 300 = high).\n 4) Select the RGB values.\n 5) Select a page on wich we will test the color filter.")


test = Button(root, text="Test path", width=15, height=2, bg='lightblue', command=is_valid).place(x=60, y=350)

testFilter = Button(root, text="Test filter", width=15, height=2, bg='lightblue', command=convertTest).place(x=210, y=350)

convert = Button(root, text="Convert PDF", width=15, height=2, bg='lightblue', command=convertFull).place(x=360, y=350)

estTime = Button(root, text="Estimate time", width=15, height=2, bg='lightblue', command=estimateTime).place(x=510, y=350)

B1 = Button(root, text="SHOW MANUAL", width=15, height=2, command=Manual).place(x=360, y=100)

root.mainloop()

