from PyQt5 import QtCore, QtGui, QtWidgets
import base64

class ErrorWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.error_icon = "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"
        
        self.decoded_data = base64.b64decode(self.error_icon)
        
    def CreateWindow(self, WindowText, LabelText, x_size, y_size):
        self.setWindowTitle(WindowText)
        self.setFixedSize(x_size, y_size)
        
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
        hbox = QtWidgets.QHBoxLayout()
        vbox = QtWidgets.QVBoxLayout()
        main_layout = QtWidgets.QVBoxLayout()

        label = QtWidgets.QLabel(LabelText)
        label.setOpenExternalLinks(True)
        label.setWordWrap(True)
        
        filler_label = QtWidgets.QLabel()
        filler_label.setFixedWidth(10)

        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(self.decoded_data)
        pixmap = pixmap.scaled(50, 50)
        pixmap_label = QtWidgets.QLabel()
        pixmap_label.setFixedSize(50, 50)
        pixmap_label.setPixmap(pixmap)
        self.setWindowIcon(QtGui.QIcon(pixmap))
        
        button = QtWidgets.QPushButton("OK")
        button.clicked.connect(self.close)

        hbox.addWidget(pixmap_label)
        hbox.addWidget(filler_label)
        hbox.addWidget(label)
        vbox.addWidget(button)

        main_layout.addLayout(hbox)
        main_layout.addLayout(vbox)

        main_widget = QtWidgets.QWidget()
        main_widget.setLayout(main_layout)
        
        self.setCentralWidget(main_widget)