#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tkinter as tk
import tkFileDialog
import ttk
import os
import ntpath


class Configurateur(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, "Configurateur SMC")
        tk.Tk.wm_geometry(self, "290x150")

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = Menu(container, self)
        self.frames[Menu] = frame
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
        class and PDFQueue class ) ), the Option fidgets, the Images fidgets, the Button fidgets, Label fidgets and
        Scale fidgets ( see TKinter ).
        """

        tk.Frame.__init__(self, parent)

        self.controller = controller

        # VARIABLES

        self.importantFiles = [["DossierInstall.txt", "\exe.win-amd64-2.7"], ["TraitDir.txt", "\exe.win-amd64-2.7"], ["ImMa_convert.txt", "\exe.win-amd64-2.7"]]

        # LABEL

        self.labeladd = tk.Label(self, text="Logiciels requis pour la configuration :\n"
                                            "----------------------------------------\n"
                                            " - Ghostscript\n"
                                            " - ImageMagick\n"
                                            "\n Ces logiciels se trouvent dans le build.", anchor="w", justify="left", font=("Verdana", 7, "bold"),
                                 fg="dark slate gray").place(x=10, y=10)

        # BUTTON

        self.button17 = ttk.Button(self, text="INITIALISATION DE L'APPLICATION",
                                   command=lambda: self.ChechImageMagick())
        self.button17.place(x=40, y=100)

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

    def chechFileExists(self, filename):
        """
        Search if the file ( filename ) exists in the current directory, if not, create it.

        :param filename: the name of the file. ( String )
        :return: True if filename exists, False otherwise.
        """

        if not os.path.exists(str(filename)):
            print "does not exists"
            return False
        else:
            print "exists already"
            return True

    def writeTxt(self, filename, txt):
        """
        Creates and writes txt in filename.txt.

        :param filename: the name given to the .txt file that will be created.
        :param txt: The text that will be written in the filename.txt.
        """

        file = open(str(filename), "w")
        file.write(txt)
        file.close()

    def ChechImageMagick(self):
        """
        Configure the file .txt "TraitDir.txt" and "ImMa_convert.txt", telling the program where to find
        convert.exe from ImageMagick and TraitementDir from the build.
        """

        # ASK DIRECTORY OF THE BUILD

        self.importantFiles = [["TraitDir.txt", "\exe.win-amd64-2.7"],
                               ["ImMa_convert.txt", "\exe.win-amd64-2.7"]]

        filename = tkFileDialog.askdirectory(initialdir="/", title="Selectionner le dossier 'build'")

        for txt in self.importantFiles:

            result = self.findall(str(txt[0]), filename)

            if txt[0] == "TraitDir.txt":

                location_txt = filename + txt[1] + "\\" + txt[0]
                print location_txt
                dossier = filename + txt[1] + "\TraitementDir"
                print dossier

                try:
                    os.remove(location_txt)
                    self.writeTxt(location_txt, str(dossier))

                except:
                    self.writeTxt(location_txt, str(dossier))

            if txt[0] == "ImMa_convert.txt":

                file_ImMa = tkFileDialog.askdirectory(initialdir="/", title="Selectionner le dossier 'ImageMagick")

                location_txt = filename + txt[1] + "\\" + txt[0]
                print location_txt
                exe = self.findall("convert.exe", file_ImMa)
                print exe

                try:
                    os.remove(location_txt)
                    self.writeTxt(location_txt, str(exe[0]))

                except:
                    self.writeTxt(location_txt, str(exe[0]))


def main():

    config = Configurateur()
    config.mainloop()


if __name__ == '__main__':
    main()
