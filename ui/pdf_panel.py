from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QGridLayout
from PySide6.QtCore import Signal, Qt
from pdf.open_pdf import open_pdf_dialog, load_document, load_page_next, load_page_previous, extract_text

class PdfPanel(QWidget):
    texto_extraido = Signal(str)
    
    def __init__(self):
        super().__init__()
        
        self.doc = None
        self.pagina_actual = 0
        self.archivo_actual = None
        
        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        layout_grid = QGridLayout()
        layout_grid.setContentsMargins(0, 0, 0, 0)
        layout_grid.setHorizontalSpacing(8)
        
        self.button_upload = QPushButton("Subir PDF")
        self.button_upload.setMinimumHeight(38)
        self.connect_upload_button()
        self.button_previous = QPushButton("Anterior")
        self.button_next = QPushButton("Siguiente")
        self.button_previous.setMinimumHeight(34)
        self.button_next.setMinimumHeight(34)
        
        self.pdf_view = QLabel()
        self.pdf_view.setObjectName("PdfCanvas")
        self.pdf_view.setMinimumSize(400, 500)
        self.pdf_view.setAlignment(Qt.AlignCenter)
        
        self.label_pages = QLabel("Pagina 0 de 0")
        self.label_pages.setObjectName("StatusLabel")
        self.label_pages.setStyleSheet("qproperty-alignment: 'AlignCenter';")
        
        layout.addWidget(self.button_upload)
        layout.addWidget(self.pdf_view)
        layout_grid.addWidget(self.button_next, 0,2)
        self.connect_next_page_button()
        layout_grid.addWidget(self.button_previous, 0,0)
        self.connect_previous_page_button()
        layout_grid.addWidget(self.label_pages, 0,1)
        layout.addLayout(layout_grid)
        
        self.setLayout(layout)
        self.updatePageLabel()
        self.update_navigation_buttons()
    
    def connect_upload_button(self):
        self.button_upload.clicked.connect(self.handleUploadPdf)

    def connect_next_page_button(self):
        self.button_next.clicked.connect(self.handleNextPage)
    
    def connect_previous_page_button(self):
        self.button_previous.clicked.connect(self.handlePreviousPage)

    def handleNextPage(self):
        load_page_next(self)
        self.updatePageLabel()
        self.update_navigation_buttons()
    
    def handlePreviousPage(self):
        load_page_previous(self)
        self.updatePageLabel()
        self.update_navigation_buttons()

    def handleUploadPdf(self):
        archivo = open_pdf_dialog(self)
        load_document(self, archivo)
        if self.doc:
            texto = extract_text(self.doc)
            self.texto_extraido.emit(texto)
        self.updatePageLabel()
        self.update_navigation_buttons()

    def update_navigation_buttons(self):
        if not self.doc:
            self.button_previous.setEnabled(False)
            self.button_next.setEnabled(False)
            return

        self.button_previous.setEnabled(self.pagina_actual > 0)
        self.button_next.setEnabled(self.pagina_actual < self.doc.page_count - 1)

    def updatePageLabel(self):
        if self.doc:
            total_paginas = self.doc.page_count
            pagina_mostrada = self.pagina_actual + 1
            self.label_pages.setText(f"Pagina {pagina_mostrada} de {total_paginas}")
        else:
            self.label_pages.setText("Pagina 0 de 0")
       
        
        
        