from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QGridLayout
from pdf.open_pdf import openPdf, getPage, loadPageNext, loadPagePrevious

class PdfPanel(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.doc = None
        self.pagina_actual = 0
        self.archivo_actual = None
        
        layout = QVBoxLayout()
        layout_grid = QGridLayout()
        
        self.button_upload = QPushButton("Subir Pdf")
        self.clickButton()
        self.button_previous = QPushButton("Anterior")
        self.button_next = QPushButton("Siguiente")
        
        self.pdf_view = QLabel()
        self.pdf_view.setMinimumSize(400, 500)
        self.pdf_view.setStyleSheet("border: 1px solid black;")
        
        self.label_pages = QLabel("Pagina 0 de 0")
        self.label_pages.setStyleSheet("qproperty-alignment: 'AlignCenter';")
        
        layout.addWidget(self.button_upload)
        layout.addWidget(self.pdf_view)
        layout_grid.addWidget(self.button_next, 0,2)
        self.clickNextPage()
        layout_grid.addWidget(self.button_previous, 0,0)
        self.clickPreviousPage()
        layout_grid.addWidget(self.label_pages, 0,1)
        layout.addLayout(layout_grid)
        
        self.setLayout(layout)
        self.updatePageLabel()
    
    def clickButton(self):
        self.button_upload.clicked.connect(self.handleUploadPdf)

    def clickNextPage(self):
        self.button_next.clicked.connect(self.handleNextPage)
    
    def clickPreviousPage(self):
        self.button_previous.clicked.connect(self.handlePreviousPage)

    def handleNextPage(self):
        loadPageNext(self)
        self.updatePageLabel()
    
    def handlePreviousPage(self):
        loadPagePrevious(self)
        self.updatePageLabel()

    def handleUploadPdf(self):
        archivo = openPdf(self)
        getPage(self,archivo)
        self.updatePageLabel()

    def updatePageLabel(self):
        if self.doc:
            total_paginas = self.doc.page_count
            pagina_mostrada = self.pagina_actual + 1
            self.label_pages.setText(f"Pagina {pagina_mostrada} de {total_paginas}")
        else:
            self.label_pages.setText("Pagina 0 de 0")
       
        
        
        