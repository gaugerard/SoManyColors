import threading
import V6_2ListPDFColorMatrix
#from thread import start_new_thread, allocate_lock
# self.lock = allocate_lock()


class PDFQueue():

    def __init__(self):
        self.queue = []
        self.queue_pdf_page = []
        self.size = 0
        self.nbr_page = 0
        self.last_page_added = 0
        self.QLock = threading.Lock()

    def add_pdf(self, element, pages):
        self.QLock.acquire()
        self.queue.append(element)
        self.queue_pdf_page.append(pages)
        self.size += 1
        self.nbr_page += pages
        self.last_page_added = pages
        self.QLock.release()

    def remove_pdf(self):
        self.QLock.acquire()
        if self.size > 0:
            del self.queue[self.size - 1]
            del self.queue_pdf_page[self.size -1]
            self.size -= 1
            self.nbr_page -= self.last_page_added
        self.QLock.release()

    def process_pdf(self, dpi, typecvd, amountdalto, amounttransf, page=None):
        self.QLock.acquire()
        while self.size > 0:
            index = self.size - 1
            element = self.queue[index]
            V6_2ListPDFColorMatrix.main(self.queue, self.queue_pdf_page, dpi, typecvd, amountdalto, amounttransf, page)
            del self.queue[index]
            del self.queue_pdf_page[index]
            self.size -= 1
        self.last_page_added = 0
        self.nbr_page = 0
        self.QLock.release()

    def process_one_pdf(self, Global, dpi, typecvd, amountdalto, amounttransf):
        self.QLock.acquire()
        V6_2ListPDFColorMatrix.main(Global, self.queue[0], self.queue_pdf_page[0], dpi, typecvd, amountdalto, amounttransf)
        self.size -= 1
        self.nbr_page -= self.queue_pdf_page[0]
        del self.queue[0]
        del self.queue_pdf_page[0]
        self.QLock.release()

    def queue_state(self):
        self.QLock.acquire()
        if self.size > 0:
            result = self.queue
        else:
            result = []
        self.QLock.release()
        return result

    def full_remove(self):
        self.QLock.acquire()
        self.queue = []
        self.queue_pdf_page = []
        self.size = 0
        self.last_page_added = 0
        self.nbr_page = 0
        self.QLock.release()

