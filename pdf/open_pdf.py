from PySide6.QtWidgets import QFileDialog
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
import fitz

def open_pdf_dialog(parent):
    archivo, _ = QFileDialog.getOpenFileName(parent, "Selecciona un PDF", "", "PDF Files (*.pdf)")
    return archivo


def load_document(panel, archivo):
    if not archivo:
        return

    if panel.doc:
        panel.doc.close()

    panel.doc = fitz.open(archivo)
    panel.archivo_actual = archivo
    panel.pagina_actual = 0
    render_current_page(panel)


def render_current_page(panel):
    if not panel.doc:
        return

    pagina = panel.doc.load_page(panel.pagina_actual)

    label_width = max(1, panel.pdf_view.width())
    label_height = max(1, panel.pdf_view.height())

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
    panel.pdf_view.setPixmap(pixmap)


def load_page_next(panel):
    if panel.doc and panel.pagina_actual < panel.doc.page_count - 1:
        panel.pagina_actual += 1
        render_current_page(panel)


def load_page_previous(panel):
    if panel.doc and panel.pagina_actual > 0:
        panel.pagina_actual -= 1
        render_current_page(panel)
        
def load_pdf(path):
    return fitz.open(path)


def extract_text(doc, limit=3000):
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()

    return texto[:limit]


# Backward-compatible aliases for previous API names.
def openPdf(parent):
    return open_pdf_dialog(parent)


def getPage(panel, archivo):
    return load_document(panel, archivo)


def renderCurrentPage(panel):
    return render_current_page(panel)


def loadPageNext(panel):
    return load_page_next(panel)


def loadPagePrevious(panel):
    return load_page_previous(panel)