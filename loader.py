from PyQt5.QtWidgets import QApplication, QWidget, QLabel,QTextEdit,QPushButton,QHBoxLayout
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import random



class overlay(QWidget):
    def __init__(self, parent=None):
        #print(wid)
        super(overlay, self).__init__(parent)
        layout=QHBoxLayout()
        self.setLayout(layout)
        self.label=QLabel()
        layout.addStretch()
        layout.addWidget(self.label)
        layout.addStretch()
        random_loader=random.randint(1,5)
        pix = QMovie("image/loading%s.gif"%random_loader) 
        self.label.setMovie(pix)
        pix.start()
        
        palette = QPalette(self.palette())
        palette.setColor(palette.Background, Qt.transparent)

        self.setPalette(palette)

    def paintEvent(self, event):
        
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), QBrush(QColor(0, 0, 0, 127)))

   