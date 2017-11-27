from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage


def remove_pic(pdf_file):
    # Set parameters for analysis.
    laparams = LAParams()
    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in doc.get_pages():
        interpreter.process_page(page)
        # receive the LTPage object for the page.
        layout = device.get_result()

# dans chaque LTPage, checker si il y a des LTImage, si oui, prendre leur bbox ( la position ) et la retirer.
# layout = LTPage ( je pense )


def parse_layout(layout):
    """Function to recursively parse the layout tree."""
    for lt_obj in layout:

        if lt_obj.__class__.__name__ == "LTImage":
            # print the type of the object ( here we are interested in LTImage ) <------
            print(lt_obj.__class__.__name__)
            # gives the location of start and end (x,y) of the object ( we want LTImage) <------
            print(lt_obj.bbox)

        # if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
            # Print the text stuff
            # print(lt_obj.get_text())

        elif isinstance(lt_obj, LTFigure):
            parse_layout(lt_obj)  # Recursive


def test():
    fp = open('D:\PDF_File\PDF_charlie.pdf', 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument(parser)

    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)
        layout = device.get_result()
        parse_layout(layout)


test()
