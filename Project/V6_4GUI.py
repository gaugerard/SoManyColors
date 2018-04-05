#!/usr/bin/env python
# -*- coding: utf-8 -*-

import V6_2ListPDFColorMatrix
import QueuePDF
import Tkinter as tk
import tkFileDialog
from PIL import Image, ImageTk
import ttk
import tkMessageBox
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from threading import Thread
import logging
import os
import ntpath

LARGE_FONT = ("Verdana", 12)


class globalBS():
    """
    An object from this class contains all the information about the state of the conversion.
    """

    def __init__(self):
        """
        - isFree = is used as a lock to allow only one thread at a time to convert.
        - progress = is the number of pdf already converted by the conversion process.
        - page_left = is the number of pages left to be converted.
        - abort = if True -> the process will be kill at the end of the current pdf conversion.
                  if False -> the process is running.
        - timeout = if True -> the process is waiting and is checking every 2 seconds if timeout = False to continue the
                               process.
                    if False -> the process is running and at the beginning of every conversion, check if timeout = True.
        - pdf = list of pdf that needs to be converted by the process.
        - log = list that contains information bout the ongoing conversion process.
        """

        self.iconfile = "image_gui\\"

        if self.checkFileExists("TraitDir.txt"):
            contenu_t = self.readTxt("TraitDir.txt")
            print contenu_t
            self.TraitementDirLoc = contenu_t

        if self.checkFileExists("ImMa_convert.txt"):
            contenu_I = self.readTxt("ImMa_convert.txt")
            print contenu_I
            self.ImageMagickExe = contenu_I

        self.isFree = True
        self.progress = 0
        self.page_left = 0
        self.abort = False  # to abort and delete all pdf in conversion
        self.timeout = False  # to timeout the conversion of the pdf
        self.pdf = []
        self.log = []

    def addLogMsg(self, msg):
        """
        Add a message ( msg ) to the log list and if the log list contains more than 25 elements, erase it and fills it
        again.

        :param msg: the message to be added to the log list. ( String )
        """

        if len(self.log) >= 25:
            self.log = []

        self.log.append(msg)

    def checkFileExists(self, filename):
        """
        Search if the file ( filename ) exists in the current directory, if not, create it.
        :param filename: the name of the file. ( String )
        """

        if not os.path.exists(str(filename)):
            print "does not exists"
            return False
        else:
            print "exists already"
            return True

    def readTxt(self, filename):
        """
        Read the text contained inside the filename.txt
        :param filename: the .txt file to read from.
        :return: the content from the filename.txt.
        """

        file = open(str(filename), "r")
        contenu = file.read()
        file.close()
        return contenu


class SoManyColorsapp(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, "SoManycolors")
        tk.Tk.wm_geometry(self, "900x900")

        # create and configure logger for the GUI
        LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
        logging.basicConfig(filename="GUI.Log",
                            level=logging.INFO,  # .DEBUG
                            format=LOG_FORMAT,
                            filemode='w')
        self.logger = logging.getLogger()

        self.logger.info("App is created.")

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Menu, Information):  # creates a dictionary of frame. ( add ,Menu_conversion to add another page )

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Menu)

    def show_frame(self, cont):  # raise a frame to the top.

        frame = self.frames[cont]
        frame.tkraise()

    def get_page(self, page_class):
        return self.frames[page_class]


class Menu(tk.Frame):  # create start page.
    """
    Represents the main screen of the application with the different buttons, images and labels that are present on it.
    """

    def __init__(self, parent, controller):
        """
        Initializes most of the variables ( simple variables and objects variables like Global and Queue ( see GlobalBS
        class and PDFQueue class ) ), the Option widgets, the Images widgets, the Button widgets, Label widgets and
        Scale widgets ( see TKinter ).
        """

        tk.Frame.__init__(self, parent)

        self.controller = controller
        controller.logger.info("Menu is created.")

        # VARIABLES

        self.dpiscale = tk.IntVar()
        self.pagescale = tk.IntVar()
        self.amountdscale = tk.IntVar()
        self.amounttscale = tk.IntVar()
        self.daltotype = tk.StringVar()

        self.dpiscale.set(72)
        self.pagescale.set(1)
        self.amountdscale.set(1)
        self.amounttscale.set(1)
        self.daltotype.set("normale")

        self.Queue = QueuePDF.PDFQueue()
        self.Global = globalBS()

        # OPTION WIDGET

        # self.daltotypes = ["normal_vision", "protanope_vision", "deuteranope_vision", "tritanope_vision"]
        self.daltotypes = ["normale", "protanopie", "deuteranopie", "tritanopie"]
        self.daltotypeoption = tk.OptionMenu(self, self.daltotype, *self.daltotypes)
        self.daltotypeoption.place(x=340, y=580)

        # IMAGES WIDGET

        self.imageconvertir = Image.open(self.Global.iconfile + "convert.png")
        self.photoconvertir = ImageTk.PhotoImage(self.imageconvertir)

        self.imageremovepdf = Image.open(self.Global.iconfile + "remove60-60.png")
        self.photoremovepdf = ImageTk.PhotoImage(self.imageremovepdf)

        self.imagepause = Image.open(self.Global.iconfile + "pause60-60.png")
        self.photopause = ImageTk.PhotoImage(self.imagepause)

        self.imagepdf = Image.open(self.Global.iconfile + "sign-add-icon.png2.png")
        self.photopdf = ImageTk.PhotoImage(self.imagepdf)

        self.imageconfig = Image.open(self.Global.iconfile + "check60-60.png")
        self.photoconfid = ImageTk.PhotoImage(self.imageconfig)

        self.imagechrono = Image.open(self.Global.iconfile + "chrono.png")
        self.photochrono = ImageTk.PhotoImage(self.imagechrono)

        self.imagetest = Image.open(self.Global.iconfile + "Webp.net-resizeimage.png")
        self.phototest = ImageTk.PhotoImage(self.imagetest)

        self.imagepdfadd = Image.open(self.Global.iconfile + "pdf150-150.png")
        self.photopdfadd = ImageTk.PhotoImage(self.imagepdfadd)

        # BUTTONS WIDGET and their LABEL

        self.button17 = ttk.Button(self, text="INFORMATION SUR LE LOGICIEL", command=lambda: self.CheckInfo())
        self.button17.place(x=600, y=30)

        self.button2 = ttk.Button(self, image=self.photoconvertir, command=lambda: self.lancerconversion())
        self.button2.place(x=30, y=340)

        self.labeldel = tk.Label(self, text="convertir:", font=("Verdana", 7, "bold"),
                                 fg="dark slate gray").place(x=37, y=410)

        self.abort_button = ttk.Button(self, image=self.photoremovepdf, command=lambda: self.abortconversion())
        self.abort_button.place(x=190, y=730)

        self.labeldel = tk.Label(self, text="annuler:", font=("Verdana", 7, "bold"),
                                 fg="dark slate gray").place(x=200, y=800)

        self.abort_button = ttk.Button(self, image=self.photopause, command=lambda: self.timeoutconversion())
        self.abort_button.place(x=110, y=730)

        self.labeldel = tk.Label(self, text="pause:", font=("Verdana", 7, "bold"),
                                 fg="dark slate gray").place(x=125, y=800)

        self.abort_button = ttk.Button(self, image=self.photoconvertir, command=lambda: self.restartconversion())
        self.abort_button.place(x=30, y=730)

        self.labeldel = tk.Label(self, text="continuer:", font=("Verdana", 7, "bold"),
                                 fg="dark slate gray").place(x=37, y=800)

        self.labeladd = tk.Label(self, text="ajouter:", font=("Verdana", 7, "bold"),
                                 fg="dark slate gray").place(x=192, y=240)

        self.pdf_button = ttk.Button(self, image=self.photopdf, command=lambda: self.addpdf())
        self.pdf_button.place(x=180, y=170)

        self.labeldel = tk.Label(self, text="supprimer:", font=("Verdana", 7, "bold"),
                               fg="dark slate gray").place(x=185, y=328)

        self.pdf_button = ttk.Button(self, image=self.photoremovepdf, command=lambda: self.reomvepdf())
        self.pdf_button.place(x=180, y=260)

        self.config_button = ttk.Button(self, image=self.photoconfid, command=lambda: self.showprogress())
        self.config_button.place(x=780, y=620)

        self.labeldel = tk.Label(self, text="progression:", font=("Verdana", 7, "bold"),
                                 fg="dark slate gray").place(x=780, y=690)

        self.button4 = ttk.Button(self, image=self.photochrono, command=lambda: self.calcultemps())
        self.button4.place(x=110, y=340)

        self.labeldel = tk.Label(self, text="chrono:", font=("Verdana", 7, "bold"),
                                 fg="dark slate gray").place(x=123, y=410)

        self.button3 = ttk.Button(self, text="LANCER LE TEST", command=lambda: self.lancertest())
        self.button3.place(x=210, y=430)

        # LABEL WIDGET

        self.label0 = tk.Label(self, text="Sélectionner un pdf :",font=("Verdana", 14, "bold"), fg="dark slate gray").place(x=30, y=130)

        self.label1 = tk.Label(self, text="Configuration :",font=("Verdana", 14, "bold"), fg="dark slate gray").place(x=30, y=430)

        self.label2 = tk.Label(self, text="Sélectionner votre type de daltonisme : ", font=("Verdana", 10, "bold"), fg="dark slate gray").place(x=40, y=580)

        self.label3 = tk.Label(self, text="Sévérité du daltonisme : ", font=("Verdana", 10, "bold"), fg="dark slate gray").place(x=40, y=490)

        self.label4 = tk.Label(self, text="Séverité de la conversion : ", font=("Verdana", 10, "bold"), fg="dark slate gray").place(x=40, y=540)

        self.label5 = tk.Label(self, text="Sélectionner les dpi : ", font=("Verdana", 10, "bold"), fg="dark slate gray").place(x=40, y=630)

        self.label6 = tk.Label(self, text="pdf en cours de conversion :", font=("Verdana", 14, "bold"), fg="dark slate gray").place(x=30, y=690)

        self.label7 = tk.Label(self, image=self.phototest).place(x=390, y=0)

        self.label8 = ttk.Label(self, image=self.photopdfadd).place(x=20, y=180)

        # SCALE WIDGET

        self.pagescale = tk.Scale(self, from_=20, to=1, orient="horizontal")
        self.pagescale.place(x=320, y=412)

        self.labeldel = tk.Label(self, text="page:", font=("Verdana", 7, "bold"),
                                 fg="dark slate gray").place(x=350, y=450)

        self.dpiscale = tk.Scale(self, from_=300, to=72, orient="horizontal")
        self.dpiscale.place(x=210, y=610)

        self.amountdscale = tk.Scale(self, from_=1, to=10, orient="horizontal")
        self.amountdscale.place(x=230, y=470)

        self.amounttscale = tk.Scale(self, from_=1, to=10, orient="horizontal")
        self.amounttscale.place(x=250, y=520)

    def abortconversion(self):
        """
        Demands the abort of the current conversion process.
        The process is cancelled at the end of the current pdf conversion.

        ex: conversion of ( pdf_1, pdf_2 ) and abort demanded during pdf_1 conversion.
            --> The process will be cancelled at the beginning of pdf_2.
        """

        self.controller.logger.info("abortconversion is called.")

        if len(self.Global.pdf) == 0:
            tkMessageBox.showinfo("ERROR", "Il n'y a pas de conversion en cours.")

        else:
            self.Global.abort = True
            self.Global.timeout = False
            self.Global.addLogMsg("DEMANDE D'ANNULATION")

            tkMessageBox.showinfo("INFO", "La conversion sera annulee entierement apres la conversion du pdf en cours.")

    def timeoutconversion(self):
        """
        Demands the timeout of the current conversion process.
        The process is stopped at the end of the current pdf conversion.

        ex: conversion of ( pdf_1, pdf_2 ) and timeout demanded during pdf_1 conversion.
            --> The process will be stopped at the beginning of pdf_2 and will wait until the play button ( which
                calls the restartconversion function ) is pressed.
        """

        self.controller.logger.info("timeoutconversion is called.")

        if len(self.Global.pdf) == 0:
            tkMessageBox.showinfo("ERROR", "Il n'y a pas de conversion en cours.")

        else:
            self.Global.timeout = True
            self.Global.addLogMsg("DEMANDE DE PAUSE")
            tkMessageBox.showinfo("INFO", "La conversion sera mise en pause apres la conversion du pdf en cours.")

    def restartconversion(self):
        """
        Demands the continuation of the current conversion process.
        The process will start again as soon as this function is called.

        ex: conversion of ( pdf_1, pdf_2 ) and timeout demanded during pdf_1 conversion. Then, after restart conversion
            is called.
            --> The process will start the conversion of pdf_2 and will continue until no more pdf are present.
        """

        self.controller.logger.info("restartconversion is called.")

        if len(self.Global.pdf) == 0:
            tkMessageBox.showinfo("ERROR", "Il n'y a pas de conversion en cours.")

        else:
            self.Global.timeout = False
            self.Global.addLogMsg("CONVERSION EN COURS")

    def reomvepdf(self):
        """
        Remove a pdf from the list of pdf to be converted.

        ( See Queue class )
        """

        self.controller.logger.info("removepdf is called.")

        if self.Queue.size > 0:

            self.Queue.remove_pdf()

            pdfs = ""
            for e in range(len(self.Queue.queue)):
                pdfs += str(self.Queue.queue[e]) + "\n"

            self.label9 = tk.Label(self, text=str(pdfs),  width=70, height=10, borderwidth=1, relief="groove", font=("Verdana", 8, "bold"), fg="dark slate gray").place(x=260, y=170)
            self.controller.logger.info("a pdf has been removed.")

        else:
            tkMessageBox.showinfo("ERROR", "Il n'y a pas de PDF.")
            self.controller.logger.info("no pdf in queue.")

    def addpdf(self):
        """
        Add a pdf to the list of pdf to be converted.

        ( See Queue class )
        """

        self.controller.logger.info("addpdf is called.")

        filename = tkFileDialog.askopenfilename(initialdir="/", title="Select file",filetypes=(("pdf files", "*.pdf"), ("all files", "*.*")))
        fp = open(str(filename), 'rb')
        parser = PDFParser(fp)
        document = PDFDocument(parser)
        num_pages = 0

        for page in PDFPage.create_pages(document):
            num_pages += 1

        parser.close()
        fp.close()

        self.Queue.add_pdf(filename, num_pages)

        pdfs = ""
        for e in range(len(self.Queue.queue)):
            pdfs += str(self.Queue.queue[e]) + "\n"

        self.label10 = tk.Label(self, text=str(pdfs), width=70, height=10, borderwidth=1, relief="groove", font=("Verdana", 8, "bold"), fg="dark slate gray").place(x=260, y=170)

        self.controller.logger.info("a pdf has been added.")

    def lancerconversion(self):
        """
        Starts the conversion of all the pdf stored in the Queue object.
        It checks if no conversion is going on and if pdf are present in the queue. If so, it calls converter(...).

        ( See converter(...) )

        """

        self.controller.logger.info("lancerconversion is called.")

        if not self.Global.isFree:
            self.controller.logger.info("conversion already ongoing.")
            tkMessageBox.showinfo("ERROR", "CONVERSION DEJA EN COURS.")
            return

        if self.Global.isFree:

            self.controller.logger.info("the convertor is free.")

            dpi = self.dpiscale.get()
            typecvd = self.daltoType()  # self.daltotype.get()
            amountdalto = self.amountdscale.get()
            amounttransf = self.amounttscale.get()

            if self.Queue.size > 0:
                self.controller.logger.info("conversion started.")
                self.Global.isFree = False
                self.Global.addLogMsg("CONVERSION EN COURS")
                self.converter(False, dpi, typecvd, amountdalto, amounttransf)

            else:

                self.controller.logger.info("no pdf to be converted.")
                tkMessageBox.showinfo("ERROR", "Il n'y a pas de PDF.")

    def lancertest(self):
        """
        Starts a test conversion of a specific page ( between 1 to 20 ) from the first pdf in the queue.

        /!\ possibility to choose the page ( 1 to 20 ) but not the choose the pdf.

        ( See converter(...) )
        """

        self.controller.logger.info("lancertest is called.")

        if not self.Global.isFree:
            self.controller.logger.info("conversion already ongoing.")
            tkMessageBox.showinfo("ERROR", "CONVERSION DEJA EN COURS.")

        if self.Global.isFree:

            self.controller.logger.info("the convertor is free.")

            dpi = self.dpiscale.get()
            typecvd = self.daltoType()  # self.daltotype.get()
            amountdalto = self.amountdscale.get()
            amounttransf = self.amounttscale.get()
            page = self.pagescale.get()

            if self.Queue.size > 0:
                self.controller.logger.info("test started.")
                self.Global.isFree = False
                self.converter(True, dpi, typecvd, amountdalto, amounttransf, page)

            else:

                self.controller.logger.info("no pdf to be converted.")
                tkMessageBox.showinfo("ERROR", "Il n'y a pas de PDF.")

    def converter(self, test, dpi, typecvd, amountdalto, amounttransf, page=None):
        """
        This function calls the V6_2ListPDFColorMatrix.main function. It gives it the correct arguments to perform the
        conversion and the conversion is done by an independent thread that will continue the conversion until it has
        finished or that the abort function is called.

        :param test: True if it is a test and False if it as a full conversion.
        :param dpi: Number of dpi for the conversion. It represents the quality of the image ( 72 dpi = minimal quality,
               300 = maximal quality ).
        :param typecvd: the type of colorblindness. (normal_vision, protanope_vision, deuteranope_vision, tritanope_vision).
        :param amountdalto: Amount of conversion of color to apply.
        :param amounttransf: Amount of transformation to apply.
        :param page: ( only meaningful if test is True ) the page to test the conversion on.
        """

        self.controller.logger.info("converter is called.")

        if page is None:

            self.controller.logger.info("this is a full conversion.")

            list_pdf = self.Queue.queue
            list_pages = self.Queue.queue_pdf_page
            self.Queue.full_remove()
            thread_conversion = Thread(target=V6_2ListPDFColorMatrix.main, args=(self.Global, test, list_pdf, list_pages, dpi, typecvd, amountdalto, amounttransf))
            thread_conversion.start()
            self.label = tk.Label(self, text="", width=70, height=10, borderwidth=1, relief="groove", font=("Verdana", 8, "bold"), fg="dark slate gray").place(x=260, y=170)

            pdfs = ""
            for e in range(len(list_pdf)):
                pdfs += str(list_pdf[e]) + "\n"
            self.label11 = tk.Label(self, text=str(pdfs), width=70, height=10, borderwidth=1, relief="groove", font=("Verdana", 8, "bold"), fg="dark slate gray").place(x=260, y=730)

        else:

            self.controller.logger.info("this is a test conversion.")

            list_pdf = []
            list_pdf.append(self.Queue.queue[0])
            list_pages = self.Queue.queue_pdf_page
            thread_conversion = Thread(target=V6_2ListPDFColorMatrix.main, args=(self.Global, test, list_pdf, list_pages, dpi, typecvd, amountdalto, amounttransf, page))
            thread_conversion.start()

    def calcultemps(self, nbr=None):
        """
        Computes the theoretical time needed to convert all the pdf present in the Queue. ( In second )
        :param nbr: the total number of pages form the PDF in the Queue.
        :return: the number of seconds needed to convert the PDFs.
        """

        self.controller.logger.info("calcultemps is called.")

        dpi = self.dpiscale.get()
        if dpi//72 == 1:
            nbrsecondperpage = 2

        if dpi//72 == 2:
            nbrsecondperpage = 8

        if dpi//72 == 3:
            nbrsecondperpage = 16

        if dpi//72 == 4:
            nbrsecondperpage = 32

        if nbr is None:
            averagetime = self.Queue.nbr_page * nbrsecondperpage
            print "TEMPS ESTIME : ", averagetime
            tkMessageBox.showinfo("INFO", "Temps de conversion estime : " + str(averagetime))

        else:
            return nbr*nbrsecondperpage

    def showprogress(self):
        """
        Displays the progress of the current conversion.

        Acts more or less like a logger for the user. It shows conversion related information so the user can know
        the progress of the conversion process.
        """

        self.controller.logger.info("showprogress is called.")

        progress = ""
        for e in range(len(self.Global.log)):
            progress += str(self.Global.log[e]) + "\n"

        progress += str(self.Global.progress) + "/" + str(len(self.Global.pdf)) + "\n"
        progress += "temps restant : " + str(self.calcultemps(self.Global.page_left))
        tkMessageBox.showinfo("PROGRESS", progress)

    def findall(self, name, path):
        """
        Find all the path leading to a certain file ( name ).

        :param name: the file searched.
        :param path: the path to start the search of name from.
        :return: a list of the different existing path leading to name.
        """

        result = []
        for root, dirs, files in os.walk(path):
            if name in files:
                result.append(os.path.join(root, name))
        return result

    def path_leaf(self, path):
        """
        Gives the name at the end of a directory.

        :param path: a directory ( exe : 'C\User\Program\Images\image1.png' ).
        :return tail : the tail of the path ( exe : 'image1.png' ).
        """

        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    def CheckInfo(self):
        """
        Shows the Information frame.
        """

        self.controller.show_frame(Information)

    def daltoType(self):
        """
        Translate the color blind type into the correct form.

        ex:
            type selected    =    protanope
                                     |
                                     |
                                     |
                                     V
            what program wants = protanope_vision

        :return: vision_type : the type of colorblind that the program can read. ( "normal_vision", "protanope_vision",
                "deuteranope_vision", "tritanope_vision" )
        """

        dico_vision_type = {"normale": "normal_vision", "protanopie": "protanope_vision", "deuteranopie": "deuteranope_vision", "tritanopie": "tritanope_vision"}
        vision_type = dico_vision_type[self.daltotype.get()]
        return vision_type



# HOW TO ADD ANOTHER PAGE TO THE APPLICATION.

class Information(tk.Frame):  # create page two.

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        mon_fichier = open("INFORMATION.txt", "r")
        contenu = mon_fichier.read()
        mon_fichier.close()

        self.label = tk.Label(self, text=contenu, anchor="w", justify="left", font=("Verdana", 10, "bold"), fg="dark slate gray").place(x=20, y=20)

        self.controller = controller
        self.path_ImageMagick = ""

        self.imageconfig = Image.open("image_gui\pdficon2.png")
        self.photoconfid = ImageTk.PhotoImage(self.imageconfig)
        self.config_button = ttk.Button(self, image=self.photoconfid, command=lambda: controller.show_frame(Menu))
        self.config_button.place(x=780, y=590)

        self.labeldel = tk.Label(self, text="retour menu:", font=("Verdana", 7, "bold"),
                                 fg="dark slate gray").place(x=780, y=665)


def main():

    app = SoManyColorsapp()
    app.mainloop()


if __name__ == '__main__':
    main()
