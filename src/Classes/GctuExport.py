if __name__ == "__main__":
    print("This is a module that is imported by 'QtGecko.py'. Don't run it directly.")
    exit()
else:
    import sys, re, webbrowser, \
           PyQt5

class ExportGCTUWindow(PyQt5.QtWidgets.QWidget):
    def __init__(self, input_string, parent=None):
        super().__init__(parent)
        
        self.input_string = input_string
        self.setWindowTitle('Export GCTU')
        self.setFixedSize(600, 100)
        self.center_screen()
        
        main_layout = PyQt5.QtWidgets.QVBoxLayout(self)
        row1_layout = PyQt5.QtWidgets.QHBoxLayout()
        row2_layout = PyQt5.QtWidgets.QHBoxLayout()
        
        header_label = PyQt5.QtWidgets.QLabel("Specify the (dashed) Title-ID")
        main_layout.addWidget(header_label)
        
        title_id_label = PyQt5.QtWidgets.QLabel("Title ID:")
        self.title_id_line_edit = PyQt5.QtWidgets.QLineEdit()
        self.title_id_line_edit.textChanged.connect(self.gctu_update)
        row1_layout.addWidget(title_id_label)
        row1_layout.addWidget(self.title_id_line_edit)
        
        self.confirm_button = PyQt5.QtWidgets.QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.on_confirm)
        self.title_database = PyQt5.QtWidgets.QPushButton("Wii U Title Database")
        self.title_database.clicked.connect(self.open_title_database)
        row2_layout.addWidget(self.confirm_button)
        row2_layout.addWidget(self.title_database)
        
        main_layout.addLayout(row1_layout)
        main_layout.addLayout(row2_layout)
        self.gctu_update()
        
    def center_screen(self):
        frame_geometry = self.frameGeometry()
        calculate_screen = PyQt5.QtWidgets.QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(calculate_screen)
        self.move(frame_geometry.topLeft())
        
    def gctu_update(self):
    
        def is_valid_hex_address(address):
            pattern = re.compile(r"^([0-9a-fA-F]{8}-[0-9a-fA-F]{8})$")
            match = pattern.search(address)
            return match is not None
    
        # Set PyQt5.QtWidgets.QLineEdit style based on IPv4 Validity
        if is_valid_hex_address(self.title_id_line_edit.text()):
            self.title_id_line_edit.setStyleSheet("background-color: #00FF00;")
            self.confirm_button.setEnabled(True)
        else:
            self.title_id_line_edit.setStyleSheet("background-color: red;")
            self.confirm_button.setEnabled(False)
        
    def on_confirm(self):
        # Conver tthe input string be a straight string like "3000000010A0A624D0000000DEADCAFE"
        input_str = self.input_string.replace(" ", "").replace("\n", "")
        output_str = ""
        for i in range(0, len(self.input_string), 17):
            output_str += self.input_string[i:i+17]

        # Convert the forammted string to binary data
        binary_data = bytes.fromhex(output_str)

        # Write the binary data to a file
        file_name = self.title_id_line_edit.text().upper().replace("-", "") + ".gctu"
        with open(file_name, 'wb') as f:
            f.write(binary_data)
        
    def open_title_database(self):
        webbrowser.open("https://korozin.github.io/titlekey")
