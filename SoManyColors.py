import v5_1PDFintoJPG, v5_2ChoosenPage2PDF, v5_3ListPages2PDF
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage

def page_pdf(pdf):

    fp = open(str(pdf), 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser)
    num_pages = 0

    for page in PDFPage.create_pages(document):
        num_pages += 1

    parser.close()
    fp.close()
    return num_pages


def main(pdf_file, png_file, page, color_blind_filter, dpi):

    print
    if page_pdf(pdf_file) == 1:

        if page == 0:
            page = 1

        v5_2ChoosenPage2PDF.main(pdf_file, png_file, page, color_blind_filter, dpi)
        return

    v5_1PDFintoJPG.main(pdf_file, color_blind_filter, dpi, png_file)
    return


