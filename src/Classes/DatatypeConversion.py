import sys, struct
from PyQt5 import QtWidgets, QtCore, QtGui

class DatatypeConversion(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the Title to "Datatype Conversion | KorOwOzin"
        self.setWindowTitle("Datatype Conversion | KorOwOzin")

        # Create QFont instance, and set font size to 10
        font = QtGui.QFont()
        font.setPointSize(10)

        # Create the input label
        input_label = QtWidgets.QLabel("Input:", self)

        # Create the input text edit
        self.input_text = QtWidgets.QTextEdit(self)
        self.input_text.setFixedHeight(86)
        #self.input_text.setFixedWidth(430)
        self.input_text.setFont(font)

        # Create the output label
        output_label = QtWidgets.QLabel("Converted:", self)

        # Create the output text browser
        self.output_text = QtWidgets.QTextBrowser(self)
        self.output_text.setReadOnly(True)
        self.output_text.setFixedHeight(86)
        #self.output_text.setFixedWidth(430)
        self.output_text.setStyleSheet("background-color: #00FF00;")
        self.output_text.setFont(font)
        
        # Create the output indication label
        self.indicator_label = QtWidgets.QLabel("Result: OK!\n", self)
        
        # Create Conversion Type Label
        conversion_type_label = QtWidgets.QLabel('Conversion Type:', self)
        
        # Create the Drop-down Menu
        self.conversion_type_menu = QtWidgets.QComboBox(self)
        self.conversion_type_menu.addItems([' UTF-8', ' Decimal', ' Float'])
        self.conversion_type_menu.setCurrentIndex(1)
        self.conversion_type_menu.setFixedHeight(28)
        self.conversion_type_menu.setFixedWidth(315)
        self.conversion_type_menu.setToolTip("The conversion type to use")
        
        # Create the Check-Box for "Unicode"
        self.unicode_checkbox = QtWidgets.QCheckBox('Unicode', self)
        self.unicode_checkbox.setToolTip("Whether to convert to unicode or UTF-8")
        self.unicode_checkbox.setEnabled(True)
        
        # Create the Check-Box for "From Hexadecimal"
        self.hexadecimal_checkbox = QtWidgets.QCheckBox('From Hexadecimal', self)
        self.hexadecimal_checkbox.setToolTip("Whether to convert from or to hexadecimal")

        # Create the copy button
        self.copy_button = QtWidgets.QPushButton("Copy Result", self)
        self.copy_button.setFixedHeight(28)
        self.copy_button.clicked.connect(self.copy_result)

        # Add Input Label and Input Text to Vertical Layout
        input_layout = QtWidgets.QVBoxLayout()
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_text)

        # Add Output Label and Output Text to Vertical Layout
        output_layout = QtWidgets.QVBoxLayout()
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_text)
        output_layout.addWidget(self.indicator_label)
        
        # Add Conversion Type Label and Dropdwon Menu to Horizontal Layout
        conv_type_layout = QtWidgets.QHBoxLayout()
        conv_type_layout.addWidget(conversion_type_label)
        conv_type_layout.addWidget(self.conversion_type_menu)
        
        # Add Unicode and From Hex Checkbox to Horizontal Layout
        checkbox_layout = QtWidgets.QHBoxLayout()
        checkbox_layout.addWidget(self.unicode_checkbox)
        checkbox_layout.addWidget(self.hexadecimal_checkbox)

        # Add Copy and Copy Button to Horizontal Layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.copy_button)

        # Add all Widgets to a Main Vertical Layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)
        main_layout.addLayout(conv_type_layout)
        main_layout.addLayout(checkbox_layout)
        main_layout.addLayout(button_layout)

        # Create a central widget
        central_widget = QtWidgets.QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Always start centered on-screen
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
        # Tie Dropdown Menu items to function to update Function and Output
        self.conversion_type_menu.currentIndexChanged.connect(self.update_unicode_state)
        
        # Make sure anytime Text is input that it updates according to settings set
        self.input_text.textChanged.connect(self.update_unicode_state)
      
        # Make sure that Checkboxes will update output according to settings set
        self.unicode_checkbox.stateChanged.connect(self.update_unicode_state)
        self.hexadecimal_checkbox.stateChanged.connect(self.update_unicode_state)
        self.update_unicode_state()
        
    # Function to change settings and set output
    def update_unicode_state(self):
        # Only allow Unicode to be selectable when on Mode : UTF-8
        if self.conversion_type_menu.currentText() == ' UTF-8':
            self.unicode_checkbox.setEnabled(True)
        else:
            self.unicode_checkbox.setEnabled(False)
    
        # If on UTF-8 and neither Unicode or From Hex is checked, convert UTF-8 to Hex
        if self.conversion_type_menu.currentText() == " UTF-8" and not self.unicode_checkbox.isChecked() and not self.hexadecimal_checkbox.isChecked():
            self.input_text.textChanged.connect(self.function1)
            self.function1()

        # If on UTF-8 and Unicode is NOT checked but From Hex IS, convert Hex to UTF-8
        elif self.conversion_type_menu.currentText() == " UTF-8" and not self.unicode_checkbox.isChecked() and self.hexadecimal_checkbox.isChecked():
            self.input_text.textChanged.connect(self.function2)
            self.function2()

        # If on UTF-8 and Unicode IS checked but From Hex is NOT, convert Hex to UTF-16
        elif self.conversion_type_menu.currentText() == " UTF-8" and self.unicode_checkbox.isChecked() and not self.hexadecimal_checkbox.isChecked():
            self.input_text.textChanged.connect(self.function3)
            self.function3()

        # If on UTF-8 and BOTH Unicode and From Hex is checked, convert UTF-16 to Hex
        elif self.conversion_type_menu.currentText() == " UTF-8" and self.unicode_checkbox.isChecked() and self.hexadecimal_checkbox.isChecked():
            self.input_text.textChanged.connect(self.function4)
            self.function4()

        # If on Decimal and From Hex is NOT checked, convert Decimal to Hex
        elif self.conversion_type_menu.currentText() == " Decimal" and not self.hexadecimal_checkbox.isChecked():
            self.input_text.textChanged.connect(self.function5)
            self.function5()

        # If on Decimal and From Hex IS checked, convert Hex to Decimal
        elif self.conversion_type_menu.currentText() == " Decimal" and self.hexadecimal_checkbox.isChecked():
            self.input_text.textChanged.connect(self.function6)
            self.function6()

        # If on Float and From Hex is NOT checked, convert Floating Point to Hex
        elif self.conversion_type_menu.currentText() == " Float" and not self.hexadecimal_checkbox.isChecked():
            self.input_text.textChanged.connect(self.function7)
            self.function7()

        # If on Float and From Hex IS checked, convert Hex to Floating Point
        elif self.conversion_type_menu.currentText() == " Float" and self.hexadecimal_checkbox.isChecked():
            self.input_text.textChanged.connect(self.function8)
            self.function8()
        
        # No idea how you would even get this error message, but it exists I guess.
        else:
            self.output_text.setText("Unknown Error!")
            
    # Function to convert FloatPoint to Hex MUCH easier, and allow for OverFlow handling
    def float_to_hex(self, f):
        try:
            return format(struct.pack('!f', f).hex().zfill(8)).upper()
        except OverflowError:
            f_str = str(f)
            if "-" in f_str:
                return "FF800000"
            else:
                return "7F800000"
                
    # Function to convert Hex to Floatpoint MUCH easier
    def hex_to_float(self, hex_str):
        hex_int = int(hex_str, 16)
        try:
            float_val = struct.unpack('!f', struct.pack('!i', hex_int))[0]
            return float_val
        except:
            pass
            
    # Function to convert UTF-8 to Hex
    def function1(self):
        input_str = self.input_text.toPlainText()
        try:
            hex_str = "".join("{:02X}".format(ord(c)) for c in input_str)
            self.output_text.setStyleSheet("background-color: #00FF00;")
            self.output_text.verticalScrollBar().setStyleSheet("background-color: #999999;")
            self.output_text.setText(hex_str)
            self.indicator_label.setText("Result: OK!\n")
            self.copy_button.setEnabled(True)
        except:
            self.output_text.setStyleSheet("background-color: red;")
            self.output_text.setText("")
            self.indicator_label.setText("Result: Invalid!\n")
            self.copy_button.setEnabled(False)
        if input_str == '':
            self.output_text.setStyleSheet("background-color: #00FF00;")
            self.output_text.setText("")
            self.indicator_label.setText("Result: OK!\n")
            self.copy_button.setEnabled(True)
        
    # Function to convert Hex to UTF-8
    def function2(self):
        input_str = self.input_text.toPlainText()
        try:
            hex_bytes = bytes.fromhex(input_str)
            hex_str = hex_bytes.decode("utf-8")
            self.output_text.setStyleSheet("background-color: #00FF00;")
            self.output_text.verticalScrollBar().setStyleSheet("background-color: #999999;")
            self.output_text.setText(hex_str)
            self.indicator_label.setText("Result: OK!\n")
            self.copy_button.setEnabled(True)
        except:
            self.output_text.setStyleSheet("background-color: red;")
            self.output_text.setText("")
            self.indicator_label.setText(f"Result: Invalid input (begin 0, end {len(input_str)}, length {len(input_str)})\n")
            self.copy_button.setEnabled(False)
        if input_str == '':
            self.output_text.setStyleSheet("background-color: #00FF00;")
            self.output_text.setText("")
            self.indicator_label.setText("Result: OK!\n")
            self.copy_button.setEnabled(True)
        
    # Function to convert UTF-16 to Hex
    def function3(self):
        input_str = self.input_text.toPlainText()
        try:
            hex_str = "".join("{:04X}".format(ord(c)) for c in input_str)
            self.output_text.setStyleSheet("background-color: #00FF00;")
            self.output_text.verticalScrollBar().setStyleSheet("background-color: #999999;")
            self.output_text.setText(hex_str)
            self.indicator_label.setText("Result: OK!\n")
            self.copy_button.setEnabled(True)
        except:
            self.output_text.setStyleSheet("background-color: red;")
            self.output_text.setText("")
            self.indicator_label.setText("Result: Invalid!\n")
            self.copy_button.setEnabled(False)
        if input_str == '':
            self.output_text.setStyleSheet("background-color: #00FF00;")
            self.output_text.setText("")
            self.indicator_label.setText("Result: OK!\n")
            self.copy_button.setEnabled(True)
        
    # Function to convert Hex to UTF-16
    def function4(self):
        input_str = self.input_text.toPlainText()
        try:
            hex_pairs = [input_str[i:i+4] for i in range(0, len(input_str), 4)]
            hex_pairs = [p[2:] + p[:2] for p in hex_pairs]
            hex_str = bytearray.fromhex("".join(hex_pairs)).decode('utf-16')
            self.output_text.setStyleSheet("background-color: #00FF00;")
            self.output_text.verticalScrollBar().setStyleSheet("background-color: #999999;")
            self.output_text.setText(hex_str)
            self.indicator_label.setText("Result: OK!\n")
            self.copy_button.setEnabled(True)
        except:
            self.output_text.setStyleSheet("background-color: red;")
            self.output_text.setText("")
            label_str = input_str
            if len(input_str) > 4:
                label_str = input_str[0:4] + "..."
            self.indicator_label.setText(f'Result: Invalid input (for input string: "{label_str}")\n')
            self.copy_button.setEnabled(False)
        if input_str == '':
            self.output_text.setStyleSheet("background-color: #00FF00;")
            self.output_text.setText("")
            self.indicator_label.setText("Result: OK!\n")
            self.copy_button.setEnabled(True)
        
    # Function to convert Decimal to Hex
    def function5(self):
        input_str = self.input_text.toPlainText()
        try:
            input_int = int(input_str)
            hex_str = format(input_int, 'X')
            self.output_text.setStyleSheet("background-color: #00FF00;")
            self.output_text.verticalScrollBar().setStyleSheet("background-color: #999999;")
            self.output_text.setText(hex_str)
            self.indicator_label.setText("Result: OK!\n")
            self.copy_button.setEnabled(True)
        except:
            self.output_text.setStyleSheet("background-color: red;")
            self.output_text.setText("")
            label_str = input_str
            if len(input_str) > 9:
                label_str = input_str[:9] + "..."
            self.indicator_label.setText(f'Result: Invalid input (for input string: "{label_str}")\n')
            self.copy_button.setEnabled(False)
        if input_str == '':
            self.output_text.setStyleSheet("background-color: red;")
            self.output_text.setText("")
            self.indicator_label.setText("Result: Invalid input (Zero length Bitinteger)\n")
            self.copy_button.setEnabled(False)
        
    # Function to convert Hex to Decimal
    def function6(self):
        input_str = self.input_text.toPlainText()
        try:
            hex_str = int(input_str, 16)
            self.output_text.setStyleSheet("background-color: #00FF00;")
            self.output_text.verticalScrollBar().setStyleSheet("background-color: #999999;")
            self.output_text.setText(str(hex_str))
            self.indicator_label.setText("Result: OK!\n")
            self.copy_button.setEnabled(True)
        except ValueError:
            self.output_text.setStyleSheet("background-color: red;")
            self.output_text.setText("")
            label_str = input_str
            if len(input_str) > 7:
                label_str = input_str[:7] + "..."
            self.indicator_label.setText(f'Result: Invalid input (for input string: "{label_str}")\n')
            self.copy_button.setEnabled(False)
        if input_str == '':
            self.output_text.setStyleSheet("background-color: red;")
            self.output_text.setText("")
            self.indicator_label.setText("Result: Invalid input (Zero length Bitinteger)\n")
            self.copy_button.setEnabled(False)
        
    # Function to convert Float Point to Hex
    def function7(self):
        input_str = self.input_text.toPlainText()
        try:
            input_float = float(input_str)
            hex_str = self.float_to_hex(input_float)
            self.output_text.setStyleSheet("background-color: #00FF00;")
            self.output_text.verticalScrollBar().setStyleSheet("background-color: #999999;")
            self.output_text.setText(hex_str)
            self.indicator_label.setText("Result: OK!\n")
            self.copy_button.setEnabled(True)
        except ValueError:
            self.output_text.setStyleSheet("background-color: red;")
            self.output_text.setText("")
            label_str = input_str
            if len(input_str) > 9:
                label_str = input_str[0:9] + "..."
            self.indicator_label.setText(f'Result: Invalid input (for input string: "{label_str}")\n')
            self.copy_button.setEnabled(False)
        if input_str == '':
            self.output_text.setStyleSheet("background-color: red;")
            self.output_text.setText("")
            self.indicator_label.setText("Result: Invalid input (empty String)\n")
            self.copy_button.setEnabled(False)
        
    # Function to convert Hex to Float Point
    def function8(self):
        input_str = self.input_text.toPlainText()
        try:
            hex_str = self.hex_to_float(input_str)
            self.output_text.setStyleSheet("background-color: #00FF00;")
            self.output_text.verticalScrollBar().setStyleSheet("background-color: #999999;")
            self.output_text.setText(str(hex_str).replace(".0", ""))
            self.indicator_label.setText("Result: OK!\n")
            self.copy_button.setEnabled(True)
        except ValueError:
            self.output_text.setStyleSheet("background-color: red;")
            self.output_text.setText("")
            label_str = input_str
            if len(input_str) > 9:
                label_str = input_str[0:9] + "..."
            self.indicator_label.setText(f'Result: Invalid input (For input string: "{label_str}")\n')
            self.copy_button.setEnabled(False)
        if input_str == '':
            self.output_text.setStyleSheet("background-color: red;")
            self.output_text.setText("")
            self.indicator_label.setText("Result: Invalid input (For input string: '')\n")
            self.copy_button.setEnabled(False)
        if self.output_text.toPlainText() == "None":
            self.output_text.setStyleSheet("background-color: red;")
            self.output_text.setText("")
            self.indicator_label.setText("Result: Invalid input (For type: 'None')\n")
            self.copy_button.setEnabled(False)

    # Function to copy Output to Clipboard
    def copy_result(self):
        clip = QtWidgets.QApplication.clipboard()
        clip.setText(self.output_text.toPlainText())
        clip.setText(self.output_text.toPlainText())