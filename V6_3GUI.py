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

LARGE_FONT = ("Verdana", 12)

class SoManyColorsapp(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, "SoManycolors")
        tk.Tk.wm_geometry(self, "900x700")


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

        self.dpiscale.set(72)
        self.pagescale.set(1)
        self.amountdscale.set(1)
        self.amounttscale.set(1)
        self.daltotype.set("normal_vision")
# ---------------------------------------------------
        self.dico = {"numPDF":0, "numPAGE":0, 'lastnumpageadded':0, "listePDF":[]}
# ---------------------------------------------------

        # IMAGE
        self.imagetest = Image.open("C:\Users\gauth\PycharmProjects\untitled\pdf\SoManyColors\image_gui\Webp.net-resizeimage.png")
        self.phototest = ImageTk.PhotoImage(self.imagetest)
        self.label13 = tk.Label(self, image=self.phototest)
        self.label13.place(x=150, y=0)

        # BUTTONS
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
        self.label0 = tk.Label(self, text="Selectionner un pdf :",font=("Verdana", 14, "bold"),fg="dark slate gray").place(x=30, y=140)

        self.label1 = tk.Label(self, text="Configuration :",font=("Verdana", 14, "bold"),fg="dark slate gray").place(x=30, y=440)

        self.imagepdfadd = Image.open("C:\Users\gauth\PycharmProjects\untitled\pdf\SoManyColors\image_gui\pdf150-150.png")
        self.photopdfadd = ImageTk.PhotoImage(self.imagepdfadd)
        self.labeladdpdf_button = ttk.Label(self, image=self.photopdfadd)
        self.labeladdpdf_button.place(x=20, y=190)

        self.daltotypes = ["normal_vision", "protanope_vision", "deuteranope_vision", "tritanope_vision"]

        # LABELS

        self.label3 = tk.Label(self, text="Severite du daltonisme : ", font=("Verdana", 10, "bold"),fg="dark slate gray").place(x=40, y=500)

        self.label4 = tk.Label(self, text="Severite de la conversion : ", font=("Verdana", 10, "bold"),fg="dark slate gray").place(x=40, y=550)

        self.label2 = tk.Label(self, text="Selectionner votre type de daltonisme : ", font=("Verdana", 10, "bold"),fg="dark slate gray").place(x=40, y=590)

        self.label2 = tk.Label(self, text="Selectionner les dpi : ", font=("Verdana", 10, "bold"),fg="dark slate gray").place(x=40, y=640)

        # SCALE
        self.pagescale = tk.Scale(self, from_=20, to=1, orient="horizontal")
        self.pagescale.place(x=550, y=430)

        self.dpiscale = tk.Scale(self, from_=300, to=72, orient="horizontal")
        self.dpiscale.place(x=210, y=620)

        self.amountdscale = tk.Scale(self, from_=1, to=10, orient="horizontal")
        self.amountdscale.place(x=230, y=480)

        self.amounttscale = tk.Scale(self, from_=1, to=10, orient="horizontal")
        self.amounttscale.place(x=250, y=530)

        # OPTION

        self.daltotypeoption = tk.OptionMenu(self, self.daltotype, *self.daltotypes)
        self.daltotypeoption.place(x=340, y=590)
        self.dico["typedalto"] = self.daltotype.get()

    def reomvepdf(self):

        if len(self.dico["listePDF"]) >= 1:
            liste_pdf = self.dico["listePDF"]
            lastpdf = liste_pdf[-1]
            del liste_pdf[-1]


            self.dico["listePDF"] = liste_pdf
            self.dico["numPDF"] -= 1
            self.dico["numPAGE"] -= lastpdf[1]

            if len(self.dico["listePDF"]) == 0:
                self.dico["listePDF"] = []

            pdfs = ""
            for e in range(self.dico["numPDF"]):
                pdfs += "\n" + str(self.dico["listePDF"][e][0])

            self.label = tk.Label(self, text=str(pdfs),  width=70,height=10, borderwidth=1, relief="groove",font=("Verdana", 8, "bold"), fg="dark slate gray").place(x=260, y=180)

        else:
            tkMessageBox.showinfo("ERROR", "Il n'y a pas de PDF")

        # print self.dico
        # print self.dpiscale.get(), self.pagescale.get(), self.amountdscale.get(), self.amounttscale.get(), self.daltotype.get()

    def addpdf(self):
        filename = tkFileDialog.askopenfilename(initialdir="/", title="Select file",filetypes=(("pdf files", "*.pdf"), ("all files", "*.*")))

        # print filename

        fp = open(str(filename), 'rb')
        parser = PDFParser(fp)
        document = PDFDocument(parser)
        num_pages = 0

        for page in PDFPage.create_pages(document):
            num_pages += 1

        parser.close()
        fp.close()


# ---------------------------------------------------
        self.dico["listePDF"].append([filename, num_pages])
        self.dico["numPDF"] += 1
        self.dico["numPAGE"] += num_pages
        self.dico["lastnumpageadded"] = num_pages



# ---------------------------------------------------
        pdfs = ""
        for e in range(len(self.dico["listePDF"])):
            pdfs += "\n" + str(self.dico["listePDF"][e][0])

        self.label = tk.Label(self, text=str(pdfs), width=70,height=10, borderwidth=1, relief="groove",font=("Verdana", 8, "bold"),fg="dark slate gray").place(x=260, y=180)

        # print self.dico
        # print self.dpiscale.get(), self.pagescale.get(), self.amountdscale.get(), self.amounttscale.get(), self.daltotype.get()

    def lancerconversion(self):

        dpi = self.dpiscale.get()
        typecvd = self.daltotype.get()
        amountdalto = self.amountdscale.get()
        amounttransf = self.amounttscale.get()

        list_pdf = []
        for number in range(self.dico["numPDF"]):
            list_pdf.append(self.dico["listePDF"][number])

        self.converter(list_pdf, dpi, typecvd, amountdalto, amounttransf)

    def lancertest(self):

        dpi = self.dpiscale.get()
        typecvd = self.daltotype.get()
        amountdalto = self.amountdscale.get()
        amounttransf = self.amounttscale.get()
        page = []
        page.append(self.pagescale.get())
        list_pdf = []
        list_pdf.append(self.dico["listePDF"][0])

        # print self.dico
        # print self.dpiscale.get(), self.pagescale.get(), self.amountdscale.get(), self.amounttscale.get(), self.daltotype.get()

        # pdf_file, dpi, typeCVD, amountDalto, amountTransf, list_pages=None, png_file
        newdirectory = V6_2ListPDFColorMatrix.main(list_pdf, dpi, typecvd, amountdalto, amounttransf, page)

    def converter(self, list_pdf, dpi, typecvd, amountdalto, amounttransf):

        thread_conversion = Thread(target=V6_2ListPDFColorMatrix.main, args=(list_pdf, dpi, typecvd, amountdalto, amounttransf))
        thread_conversion.start()

        self.calcultemps()
        # thread_progress_bar = Thread() <-------------------------------------------------------------
        # thread_progress_bar.daemon = True

    def calcultemps(self):
        nbrpage = self.dico["numPAGE"]
        dpi = self.dpiscale.get()
        if dpi//72 == 1:
            nbrsecondperpage = 2

        if dpi//72 == 2:
            nbrsecondperpage = 8

        if dpi//72 == 3:
            nbrsecondperpage = 16

        if dpi//72 == 4:
            nbrsecondperpage = 32

        self.averagetime = nbrpage*nbrsecondperpage
        tkMessageBox.showinfo("TEMPS ESTIME", "Temps estime : " + str(self.averagetime))

        # print self.dico
        # print self.dpiscale.get(), self.pagescale.get(), self.amountdscale.get(), self.amounttscale.get(), self.daltotype.get()




class Menu_conversion(tk.Frame):  # create page two.

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        menu = self.controller.get_page(Menu)

        # VARIABLES
        self.daltotypes = ["normal_vision", "protanope_vision", "deuteranope_vision", "tritanope_vision"]

        # LABELS

        self.label2 = tk.Label(self, text="Selectionner les dpi : ", font=("Verdana", 10, "bold"), fg="dark slate gray").place(x=20,
                                                                                                                   y=260)
        self.label2 = tk.Label(self, text="Selectionner votre type de daltonisme : ", font=("Verdana", 10, "bold"),
                               fg="dark slate gray").place(x=20, y=400)

        self.label3 = tk.Label(self, text="Severite du daltonisme : ", font=("Verdana", 10, "bold"),
                               fg="dark slate gray").place(x=350, y=150)

        self.label4 = tk.Label(self, text="Severite de la conversion : ", font=("Verdana", 10, "bold"),
                               fg="dark slate gray").place(x=350, y=260)


        # OPTION

        self.var = tk.StringVar()
        self.var.set("normal_vision")
        self.daltotypeoption = tk.OptionMenu(self, self.var, *self.daltotypes)
        self.daltotypeoption.place(x=320, y=400)
        menu.dico["typedalto"] = self.var.get()

        # BUTTONS
        self.button1 = ttk.Button(self, text="retour Menu", command=lambda: controller.show_frame(Menu))
        self.button1.pack()

        self.button3 = ttk.Button(self, text="LANCER LE TESTE", command=lambda: self.lancertest())
        self.button3.place(x=330, y=550)

        # LABELS
        self.label1 = tk.Label(self, text="Menu_conversion", font=LARGE_FONT)
        self.label1.pack(pady=10, padx=10)
        self.label2 = tk.Label(self, text="Selectionner une page pour le teste : ", font=("arial", 10, "bold"), fg="dark slate gray").place(x=20, y=150)

        # UNAMUR
        self.imagetest = Image.open("C:\Users\gauth\PycharmProjects\untitled\pdf\SoManyColors\image_gui\Webp.net-resizeimage.png")
        self.phototest = ImageTk.PhotoImage(self.imagetest)
        self.label13 = tk.Label(self, image=self.phototest)
        self.label13.place(x=150, y=0)

        menu = self.controller.get_page(Menu)

        # SCALE
        self.pagescale = tk.Scale(self, from_=20, to=1)
        self.pagescale.place(x=258, y=150)
        menu.dico["testPAGE"] = self.pagescale.get()

        self.dpiscale = tk.Scale(self, from_=300, to=72)
        self.dpiscale.place(x=252, y=260)
        menu.dico["dpi"] = self.dpiscale.get()

        self.amountdscale = tk.Scale(self, from_=1, to=10)
        self.amountdscale.place(x=542, y=150)
        menu.dico["amountDalto"] = self.amountdscale.get()

        self.amounttscale = tk.Scale(self, from_=1, to=10)
        self.amounttscale.place(x=542, y=260)
        menu.dico["amountTransf"] = self.amounttscale.get()

    def lancertest(self):

        menu = self.controller.get_page(Menu)

        pdf_file = menu.dico["listePDF"][0]
        typecvd = self.var.get()
        dpi = menu.dico["dpi"]
        page = []
        page.append(menu.dico["testPAGE"])
        amountdalto = menu.dico["amountDalto"]
        amounttransf = menu.dico["amountTransf"]
        print page
        # pdf_file, dpi, typeCVD, amountDalto, amountTransf, list_pages=None, png_file
        newdirectory = V6_1PDFColorMatrix.main(pdf_file, dpi, typecvd, amountdalto, amounttransf, page)
        tkMessageBox.showinfo("TESTE", "L'image teste se trouve a : " + str(newdirectory))


def main():
    app = SoManyColorsapp()
    app.mainloop()


if __name__ == '__main__':
    main()