from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QGridLayout

class PdfPanel(QWidget):
    
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        layout_grid = QGridLayout()
        
        button_upload = QPushButton("Subir Pdf")
        button_previous = QPushButton("Anterior")
        button_next = QPushButton("Siguiente")
        
        self.pdf_view = QLabel()
        self.pdf_view.setMinimumSize(400, 500)
        self.pdf_view.setStyleSheet("border: 1px solid black;")
        
        label_pages = QLabel("Paginas")
        label_pages.setStyleSheet("qproperty-alignment: 'AlignCenter';")
        
        layout.addWidget(button_upload)
        layout.addWidget(self.pdf_view)
        layout_grid.addWidget(button_next, 0,0)
        layout_grid.addWidget(button_previous, 0,2)
        layout_grid.addWidget(label_pages, 0,1)
        layout.addLayout(layout_grid)
        
        self.setLayout(layout)
        
        
        
        