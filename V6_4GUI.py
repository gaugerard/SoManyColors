import V6_2ListPDFColorMatrix
import Tkinter as tk
import tkFileDialog
from PIL import Image, ImageTk
import ttk
import tkMessageBox
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from threading import Thread
import QueuePDF

LARGE_FONT = ("Verdana", 12)

class SoManyColorsapp(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, "SoManycolors")
        tk.Tk.wm_geometry(self, "900x900")


        container = tk.Frame(self)
        container.config(bg="white")

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Menu, Menu_conversion):  # creates a dictionary of frame.

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

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        # VARIABLES
        self.dpiscale = tk.IntVar()
        self.pagescale = tk.IntVar()
        self.amountdscale = tk.IntVar()
        self.amounttscale = tk.IntVar()
        self.daltotype = tk.StringVar()
        self.Queue = QueuePDF.PDFQueue()

        self.dpiscale.set(72)
        self.pagescale.set(1)
        self.amountdscale.set(1)
        self.amounttscale.set(1)
        self.daltotype.set("normal_vision")

        # OPTION
        self.daltotypes = ["normal_vision", "protanope_vision", "deuteranope_vision", "tritanope_vision"]
        self.daltotypeoption = tk.OptionMenu(self, self.daltotype, *self.daltotypes)
        self.daltotypeoption.place(x=340, y=590)

        # BUTTONS + IMAGE_BUTTONS
        self.imagepdf = Image.open("C:\Users\gauth\PycharmProjects\untitled\pdf\SoManyColors\image_gui\sign-add-icon.png2.png")
        self.photopdf = ImageTk.PhotoImage(self.imagepdf)
        self.pdf_button = ttk.Button(self, image=self.photopdf, command=lambda: self.addpdf())
        self.pdf_button.place(x=180, y=190)

        self.imageremovepdf = Image.open("C:\Users\gauth\PycharmProjects\untitled\pdf\SoManyColors\image_gui\\remove60-60.png")
        self.photoremovepdf = ImageTk.PhotoImage(self.imageremovepdf)
        self.pdf_button = ttk.Button(self, image=self.photoremovepdf, command=lambda: self.reomvepdf())
        self.pdf_button.place(x=180, y=270)

        self.imageconvertir = Image.open("C:\Users\gauth\PycharmProjects\untitled\pdf\SoManyColors\image_gui\convert.png")
        self.photoconvertir = ImageTk.PhotoImage(self.imageconvertir)
        self.button2 = ttk.Button(self, image=self.photoconvertir, command=lambda: self.lancerconversion())
        self.button2.place(x=30, y=350)

        self.imageconfig = Image.open("C:\Users\gauth\PycharmProjects\untitled\pdf\SoManyColors\image_gui\process2.png")
        self.photoconfid = ImageTk.PhotoImage(self.imageconfig)
        self.config_button = ttk.Button(self, image=self.photoconfid,command=lambda: controller.show_frame(Menu_conversion))
        self.config_button.place(x=780, y=590)

        self.imagechrono = Image.open("C:\Users\gauth\PycharmProjects\untitled\pdf\SoManyColors\image_gui\chrono.png")
        self.photochrono = ImageTk.PhotoImage(self.imagechrono)
        self.button4 = ttk.Button(self, image=self.photochrono, command=lambda: self.calcultemps())
        self.button4.place(x=110, y=350)

        self.button3 = ttk.Button(self, text="LANCER LE TESTE", command=lambda: self.lancertest())
        self.button3.place(x=210, y=440)

        # LABELS
        self.label0 = tk.Label(self, text="Selectionner un pdf :",font=("Verdana", 14, "bold"), fg="dark slate gray").place(x=30, y=140)

        self.label1 = tk.Label(self, text="Configuration :",font=("Verdana", 14, "bold"), fg="dark slate gray").place(x=30, y=440)

        self.label3 = tk.Label(self, text="Severite du daltonisme : ", font=("Verdana", 10, "bold"), fg="dark slate gray").place(x=40, y=500)

        self.label4 = tk.Label(self, text="Severite de la conversion : ", font=("Verdana", 10, "bold"), fg="dark slate gray").place(x=40, y=550)

        self.label2 = tk.Label(self, text="Selectionner votre type de daltonisme : ", font=("Verdana", 10, "bold"), fg="dark slate gray").place(x=40, y=590)

        self.label2 = tk.Label(self, text="Selectionner les dpi : ", font=("Verdana", 10, "bold"), fg="dark slate gray").place(x=40, y=640)

        self.label1 = tk.Label(self, text="pdf en cours de conversion :", font=("Verdana", 14, "bold"), fg="dark slate gray").place(x=30, y=700)

        # IMAGES
        self.imagetest = Image.open("C:\Users\gauth\PycharmProjects\untitled\pdf\SoManyColors\image_gui\Webp.net-resizeimage.png")
        self.phototest = ImageTk.PhotoImage(self.imagetest)
        self.label13 = tk.Label(self, image=self.phototest)
        self.label13.place(x=150, y=0)

        self.imagepdfadd = Image.open("C:\Users\gauth\PycharmProjects\untitled\pdf\SoManyColors\image_gui\pdf150-150.png")
        self.photopdfadd = ImageTk.PhotoImage(self.imagepdfadd)
        self.labeladdpdf_button = ttk.Label(self, image=self.photopdfadd)
        self.labeladdpdf_button.place(x=20, y=190)

        # SCALES
        self.pagescale = tk.Scale(self, from_=20, to=1, orient="horizontal")
        self.pagescale.place(x=550, y=430)

        self.dpiscale = tk.Scale(self, from_=300, to=72, orient="horizontal")
        self.dpiscale.place(x=210, y=620)

        self.amountdscale = tk.Scale(self, from_=1, to=10, orient="horizontal")
        self.amountdscale.place(x=230, y=480)

        self.amounttscale = tk.Scale(self, from_=1, to=10, orient="horizontal")
        self.amounttscale.place(x=250, y=530)

    def reomvepdf(self):

        if self.Queue.size > 0:

            self.Queue.remove_pdf()
            # print self.Queue.queue

            pdfs = ""
            for e in range(len(self.Queue.queue)):
                pdfs += str(self.Queue.queue[e]) + "\n"

            self.label = tk.Label(self, text=str(pdfs),  width=70,height=10, borderwidth=1, relief="groove",font=("Verdana", 8, "bold"), fg="dark slate gray").place(x=260, y=180)

        else:
            tkMessageBox.showinfo("ERROR", "Il n'y a pas de PDF")

    def addpdf(self):
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
        # print self.Queue.queue

        pdfs = ""
        for e in range(len(self.Queue.queue)):
            pdfs += str(self.Queue.queue[e]) + "\n"

        self.label = tk.Label(self, text=str(pdfs), width=70,height=10, borderwidth=1, relief="groove", font=("Verdana", 8, "bold"), fg="dark slate gray").place(x=260, y=180)

    def lancerconversion(self):

        dpi = self.dpiscale.get()
        typecvd = self.daltotype.get()
        amountdalto = self.amountdscale.get()
        amounttransf = self.amounttscale.get()

        if self.Queue.size > 0:
            self.converter(dpi, typecvd, amountdalto, amounttransf)

        else:

            tkMessageBox.showinfo("ERROR", "Il n'y a pas de PDF")

    def lancertest(self):

        dpi = self.dpiscale.get()
        typecvd = self.daltotype.get()
        amountdalto = self.amountdscale.get()
        amounttransf = self.amounttscale.get()
        page = []
        page.append(self.pagescale.get())

        if self.Queue.size > 0:
            self.converter(dpi, typecvd, amountdalto, amounttransf, page)

        else:

            tkMessageBox.showinfo("ERROR", "Il n'y a pas de PDF")

    def converter(self, dpi, typecvd, amountdalto, amounttransf, page=None):

        if page is None:
            list_pdf = self.Queue.queue
            list_pages = self.Queue.queue_pdf_page
            print "converter ",list_pdf
            self.Queue.full_remove()
            thread_conversion = Thread(target=V6_2ListPDFColorMatrix.main, args=(list_pdf, list_pages, dpi, typecvd, amountdalto, amounttransf))
            thread_conversion.start()
            self.label = tk.Label(self, text="", width=70, height=10, borderwidth=1, relief="groove",font=("Verdana", 8, "bold"), fg="dark slate gray").place(x=260, y=180)
            self.calcultemps()

            pdfs = ""
            for e in range(len(list_pdf)):
                pdfs += str(list_pdf[e]) + "\n"
            self.label = tk.Label(self, text=str(pdfs), width=90, height=6, borderwidth=1, relief="groove",font=("Verdana", 8, "bold"), fg="dark slate gray").place(x=100, y=740)

        else :
            list_pdf = []
            list_pdf.append(self.Queue.queue[0])
            print "contest ", list_pdf
            list_pages = self.Queue.queue_pdf_page
            # print list_pdf
            thread_conversion = Thread(target=V6_2ListPDFColorMatrix.main, args=(list_pdf, list_pages, dpi, typecvd, amountdalto, amounttransf, page))
            thread_conversion.start()

    def calcultemps(self):

        dpi = self.dpiscale.get()
        if dpi//72 == 1:
            nbrsecondperpage = 2

        if dpi//72 == 2:
            nbrsecondperpage = 8

        if dpi//72 == 3:
            nbrsecondperpage = 16

        if dpi//72 == 4:
            nbrsecondperpage = 32

        averagetime = self.Queue.nbr_page * nbrsecondperpage
        print "TEMPS ESTIME : ", averagetime


class Menu_conversion(tk.Frame):  # create page two.

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller


def main():
    app = SoManyColorsapp()
    app.mainloop()



if __name__ == '__main__':
    main()