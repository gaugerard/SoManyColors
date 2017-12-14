import V6_1PDFColorMatrix
import Tkinter as tk
import tkFileDialog
from PIL import Image, ImageTk
import ttk
import tkMessageBox
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage



LARGE_FONT = ("Verdana", 12)


class SoManyColorsapp(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)

        tk.Tk.wm_title(self, "SoManycolors")

        tk.Tk.wm_geometry(self, "800x600")


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
# ---------------------------------------------------
        self.dico = {"numPDF":0, "numPAGE":0, "testPAGE":1, "listePDF":[], "dpi":72, "typedalto": "normal", "amountDalto":1, "amountTransf":1}
# ---------------------------------------------------
        self.listpdf = tk.StringVar()
        self.pdffile = tk.StringVar()
        self.maxpage = tk.IntVar()
        self.widthpage = tk.IntVar()
        self.heightpage = tk.IntVar()



        # IMAGE
        self.imagetest = Image.open("C:\Users\gauth\PycharmProjects\untitled\pdf\SoManyColors\image_gui\Webp.net-resizeimage.png")
        self.phototest = ImageTk.PhotoImage(self.imagetest)
        self.label13 = tk.Label(self, image=self.phototest)
        self.label13.place(x=150, y=0)

        # BUTTONS
        self.imagepdf = Image.open("C:\Users\gauth\PycharmProjects\untitled\pdf\SoManyColors\image_gui\pdficon2.png")
        self.photopdf = ImageTk.PhotoImage(self.imagepdf)
        self.pdf_button = ttk.Button(self, image=self.photopdf, command=lambda: self.askpdf())
        self.pdf_button.place(x=170, y=190)

        self.imagepdfadd = Image.open("C:\Users\gauth\PycharmProjects\untitled\pdf\SoManyColors\image_gui\sign-add-icon.png2.png")
        self.photopdfadd = ImageTk.PhotoImage(self.imagepdfadd)
        self.addpdf_button = ttk.Button(self, image=self.photopdfadd, command=lambda: self.addpdf())
        self.addpdf_button.place(x=170, y=270)

        self.imageconversion = Image.open("C:\Users\gauth\PycharmProjects\untitled\pdf\SoManyColors\image_gui\process2.png")
        self.photoconversion = ImageTk.PhotoImage(self.imageconversion)
        self.config_button = ttk.Button(self, image=self.photoconversion,
                                        command=lambda: controller.show_frame(Menu_conversion))
        self.config_button.place(x=170, y=490)

        self.imageconvertir = Image.open("C:\Users\gauth\PycharmProjects\untitled\pdf\SoManyColors\image_gui\convert.png")
        self.photoconvertir = ImageTk.PhotoImage(self.imageconvertir)
        self.button2 = ttk.Button(self, image=self.photoconvertir, command=lambda: self.lancerconversion())
        self.button2.place(x=170, y=350)

        # LABELS
        self.label0 = tk.Label(self, text="Selectionner un pdf :",
                               font=("Verdana", 14, "bold"),
                               fg="dark slate gray").place(x=40, y=140)

        self.label1 = tk.Label(self, text="Configuration :",
                               font=("Verdana", 14, "bold"),
                               fg="dark slate gray").place(x=40, y=440)



    def askpdf(self):
        filename = tkFileDialog.askopenfilename(initialdir="/", title="Select file",
                                                     filetypes=(("pdf files", "*.pdf"), ("all files", "*.*")))



        self.pdffile.set(filename)
        # print filename

        fp = open(str(filename), 'rb')
        parser = PDFParser(fp)
        document = PDFDocument(parser)
        num_pages = 0

        for page in PDFPage.create_pages(document):
            num_pages += 1

        self.maxpage.set(num_pages)
        # print self.pdffile.get()
        # print self.maxpage.get()
        parser.close()
        fp.close()


# ---------------------------------------------------
        self.dico["listePDF"].append(filename)
        self.dico["numPDF"] += 1
        self.dico["numPAGE"] += num_pages
# ---------------------------------------------------



        self.listpdf.set(filename)

        self.label1 = tk.Label(self, text=self.pdffile.get(), width=70, borderwidth=1, relief="groove",
                               font=("Verdana", 8, "bold"),
                               fg="dark slate gray").place(x=250, y=230)

    def addpdf(self):
        filename = tkFileDialog.askopenfilename(initialdir="/", title="Select file",
                                                filetypes=(("pdf files", "*.pdf"), ("all files", "*.*")))

        listeactuel = str(self.listpdf.get()) + " " + str(filename)
        self.listpdf.set(listeactuel)

        self.label2 = tk.Label(self, text=self.listpdf.get(), width=70, borderwidth=1, relief="groove",
                               font=("Verdana", 8, "bold"),
                               fg="dark slate gray").place(x=250, y=270)

    def lancerconversion(self):

        for number in range(self.dico["numPDF"]):
            pdf_file = self.dico["listePDF"][number]
            dpi = self.dico["dpi"]
            typecvd = self.dico["typedalto"]
            amountdalto = self.dico["amountDalto"]
            amounttransf = self.dico["amountTransf"]

            newdirectory = V6_1PDFColorMatrix.main(pdf_file, dpi, typecvd, amountdalto, amounttransf)
            tkMessageBox.showinfo("CONVERSION", "Le PDF se trouve a : " + str(newdirectory))

        """
        menu = self.controller.get_page(Menu)
        pdf_list = menu.listpdf.get()
        typecvd = str(self.daltotype.get())
        dpi = int(self.dpiscale.get())
        amountdalto = int(self.amountdscale.get())
        amounttransf = int(self.amounttrans.get())

        print pdf_list

        numpdf = 0
        for letter in pdf_list:
            if letter == " ":
                numpdf += 1

        print numpdf

        index = 0
        pdf = ""
        for e in range(numpdf+1):

            if index < len(pdf_list):
                while index < len(pdf_list) and pdf_list[index] != " ":
                    pdf = pdf + pdf_list[index]
                    index += 1

            print "conversion du pdf : ", pdf
            pdf_file = str(pdf)

            newdirectory = V6_1PDFColorMatrix.main(pdf_file, dpi, typecvd, amountdalto, amounttransf)
            tkMessageBox.showinfo("CONVERSION", "L'image teste se trouve a : " + str(newdirectory))
            index += 1
            pdf = ""
            """

class Menu_conversion(tk.Frame):  # create page two.

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        menu = self.controller.get_page(Menu)

        # VARIABLES
        self.nbrpage = menu.maxpage.get()
        self.listepdf = menu.listpdf.get()
        self.choosenpage = tk.IntVar()
        self.pdf = menu.pdffile.get()
        self.dpi = tk.IntVar()
        self.daltotype = tk.StringVar()
        self.daltotypes = ["normal_vision", "protanope_vision", "deuteranope_vision", "tritanope_vision"]
        self.amountdalto = tk.StringVar()
        self.amounttrans = tk.StringVar()

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
        self.datlotypeoption = tk.OptionMenu(self, self.daltotype, *self.daltotypes)
        self.datlotypeoption.place(x=320, y=400)
        menu.dico["typedalto"] = self.daltotype.get()

        # BUTTONS
        self.button1 = ttk.Button(self, text="retour Menu", command=lambda: controller.show_frame(Menu))
        self.button1.pack()



        self.button3 = ttk.Button(self, text="LANCER LE TESTE", command=lambda: self.lancertest())
        self.button3.place(x=330, y=550)

        self.imagechrono = Image.open("C:\Users\gauth\PycharmProjects\untitled\pdf\SoManyColors\image_gui\chrono.png")
        self.photochrono = ImageTk.PhotoImage(self.imagechrono)
        self.button4 = ttk.Button(self, image=self.photochrono, command=lambda: self.calcultemps())
        self.button4.place(x=150, y=500)

        # LABELS
        self.label1 = tk.Label(self, text="Menu_conversion", font=LARGE_FONT)
        self.label1.pack(pady=10, padx=10)
        self.label2 = tk.Label(self, text="Selectionner une page pour le teste : ", font=("arial", 10, "bold"),
                               fg="dark slate gray").place(x=20, y=150)
        self.label3 = tk.Label(self, text=self.pdf, font=LARGE_FONT)
        self.label3.pack(pady=10, padx=10)

        # UNAMUR
        self.imagetest = Image.open("C:\Users\gauth\PycharmProjects\untitled\pdf\SoManyColors\image_gui\Webp.net-resizeimage.png")
        self.phototest = ImageTk.PhotoImage(self.imagetest)
        self.label13 = tk.Label(self, image=self.phototest)
        self.label13.place(x=150, y=0)

        menu = self.controller.get_page(Menu)
        self.nbrpage = menu.maxpage.get()
        self.pdf = menu.pdffile.get()

        # self.dico = {"numPDF":0, "numPAGE":0, "listePDF":[], "dpi":72, "typedalto": "normal", "amountDalto":1, "amountTransf":1}
        # SCALE
        self.pagescale = tk.Scale(self, from_=20, to=1)
        self.pagescale.place(x=258, y=150)
        menu.dico["testPAGE"] = self.pagescale.get()
        # self.choosenpage.set(self.pagescale.get())

        self.dpiscale = tk.Scale(self, from_=300, to=72)
        self.dpiscale.place(x=252, y=260)
        menu.dico["dpi"] = self.dpiscale.get()
        # self.dpi.set(self.dpiscale.get())

        self.amountdscale = tk.Scale(self, from_=1, to=10)
        self.amountdscale.place(x=542, y=150)
        menu.dico["amountDalto"] = self.amountdscale.get()
        # self.amountdalto.set(self.amountdscale.get())

        self.amounttscale = tk.Scale(self, from_=1, to=10)
        self.amounttscale.place(x=542, y=260)
        menu.dico["amountTransf"] = self.amounttscale.get()
        # self.amounttrans.set(self.amounttscale.get())


    def lancertest(self):




        menu = self.controller.get_page(Menu)
        """
        pdf_file = str(menu.pdffile.get())
        typecvd = str(self.daltotype.get())
        dpi = int(self.dpi.get())
        page = [int(self.choosenpage.get())]
        amountdalto = int(self.amountdscale.get())
        amounttransf = int(self.amounttrans.get())
        """

        # self.dico = {"numPDF":0, "numPAGE":0, "listePDF":[], "dpi":72, "typedalto": "normal", "amountDalto":1, "amountTransf":1}
        pdf_file = menu.dico["listePDF"][0]
        typecvd = menu.dico["typedalto"]
        dpi = menu.dico["dpi"]
        page = menu.dico["testPAGE"]
        amountdalto = menu.dico["amountDalto"]
        amounttransf = menu.dico["amountTransf"]

        print "teste sur le  pdf : ", pdf_file
        print pdf_file, dpi, typecvd, page, amountdalto, amounttransf

        # pdf_file, dpi, typeCVD, amountDalto, amountTransf, list_pages=None, png_file
        newdirectory = V6_1PDFColorMatrix.main(pdf_file, dpi, typecvd, amountdalto, amounttransf, page)
        tkMessageBox.showinfo("TESTE", "L'image teste se trouve a : " + str(newdirectory))



    def calcultemps(self):
        menu = self.controller.get_page(Menu)
        nbrpage = int(menu.maxpage.get())
        dpi = int(self.dpiscale.get())
        if dpi//72 == 1:
            nbrsecondperpage = 1.6

        if dpi//72 == 2:
            nbrsecondperpage = 6.4

        if dpi//72 == 3:
            nbrsecondperpage = 12.8

        if dpi//72 == 4:
            nbrsecondperpage = 25.6

        averagetime = nbrpage*nbrsecondperpage
        tkMessageBox.showinfo("TEMPS ESTIME", "Temps estime : " + str(averagetime))



app = SoManyColorsapp()
app.mainloop()