from PySide6.QtWidgets import QFileDialog
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
import fitz

def openPdf(self):
    archivo, _ = QFileDialog.getOpenFileName(self, "Selecciona un PDF", "", "PDF Files (*.pdf)")
    
    return archivo

def getPage(self, archivo):
    if not archivo:
        return

    if self.doc:
        self.doc.close()

    self.doc = fitz.open(archivo)
    self.archivo_actual = archivo
    self.pagina_actual = 0
    renderCurrentPage(self)

def renderCurrentPage(self):
    if not self.doc:
        return

    pagina = self.doc.load_page(self.pagina_actual)

    label_width = max(1, self.pdf_view.width())
    label_height = max(1, self.pdf_view.height())

    page_rect = pagina.rect
    zoom = min(label_width / page_rect.width, label_height / page_rect.height)
    matrix = fitz.Matrix(zoom, zoom)

    pix = pagina.get_pixmap(matrix=matrix, alpha=False)

    img = QImage(
        pix.samples,
        pix.width,
        pix.height,
        pix.stride,
        QImage.Format_RGB888
    ).copy()

    pixmap = QPixmap.fromImage(img).scaled(
        label_width,
        label_height,
        Qt.KeepAspectRatio,
        Qt.SmoothTransformation
    )
    self.pdf_view.setPixmap(pixmap)

def loadPageNext(self):
    if self.doc and self.pagina_actual < self.doc.page_count - 1:
        self.pagina_actual += 1
        renderCurrentPage(self)

def loadPagePrevious(self):
    if self.doc and self.pagina_actual > 0:
        self.pagina_actual -= 1
        renderCurrentPage(self)
        
def load_pdf(path):
    return fitz.open(path)


def extract_text(doc, limit=3000):
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()

    return texto[:limit]