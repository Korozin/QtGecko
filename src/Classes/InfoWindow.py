from PyQt5 import QtCore, QtGui, QtWidgets
import base64

class InfoWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.info_icon = "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"
        
        self.decoded_data = base64.b64decode(self.info_icon)
        
    def CreateWindow(self, WindowText, LabelText, x_size, y_size):
        self.setWindowTitle(WindowText)
        self.setFixedSize(x_size, y_size)
        self.setWindowIcon(QtGui.QIcon("info.png"))
        
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