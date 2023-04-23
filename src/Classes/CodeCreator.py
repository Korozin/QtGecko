if __name__ == "__main__":
    print("This is a module that is imported by 'QtGecko.py'. Don't run it directly.")
    exit()
else:
    from PyQt5 import QtCore, QtGui, QtWidgets
    from Classes.CodeTextWidget import Editor
    from Classes.ErrorWindow import ErrorWindow

class CodeCreator(QtWidgets.QMainWindow):
    def __init__(self, file_path):
        super().__init__()

        self.file_path = file_path

        self.InitUI()

    def InitUI(self):
        self.setGeometry(0, 0, 650, 550)
        self.setWindowTitle("Code Creator | KorOwOzin")

        # Create elements
        self.title_label = QtWidgets.QLabel("Title:", self)
        self.title_label.move(5, 5)
        
        self.title_edit = QtWidgets.QLineEdit(self)
        self.title_edit.resize(635, 18)
        self.title_edit.move(5, 30)
        
        self.author_label = QtWidgets.QLabel("Author(s):", self)
        self.author_label.move(5, 55)
        
        self.author_edit = QtWidgets.QLineEdit(self)
        self.author_edit.setText("")
        self.author_edit.resize(635, 18)
        self.author_edit.move(5, 85)
        
        self.code_label = QtWidgets.QLabel("Code:", self)
        self.code_label.move(5, 110)
        
        self.code_edit = Editor(self)
        self.code_edit.setPlainText("")
        self.code_edit.resize(350, 200)
        self.code_edit.move(5, 145)
        self.code_edit.textChanged.connect(self.is_code_valid)
        
        self.comment_label = QtWidgets.QLabel("Comment:", self)
        self.comment_label.move(360, 110)
        
        self.comment_edit = QtWidgets.QTextEdit(self)
        self.comment_edit.setText("")
        self.comment_edit.resize(285, 290)
        self.comment_edit.move(360, 145)

        self.format_button = QtWidgets.QPushButton("Format", self)
        self.format_button.resize(350, 30)
        self.format_button.move(5, 350)
        self.format_button.clicked.connect(self.format_code)
        
        self.raw_assembly_checkbox = QtWidgets.QCheckBox("RAW Machine Code", self)
        self.raw_assembly_checkbox.setEnabled(False)
        self.raw_assembly_checkbox.resize(160, 30)
        self.raw_assembly_checkbox.move(5, 380)
        
        self.assembly_ram_write_checkbox = QtWidgets.QCheckBox("Assembly RAM Write", self)
        self.assembly_ram_write_checkbox.setChecked(False)
        self.assembly_ram_write_checkbox.resize(175, 30)
        self.assembly_ram_write_checkbox.move(180, 380)
        
        self.total_lines_label = QtWidgets.QLabel("Total Lines: 0", self)
        self.total_lines_label.resize(175, 40)
        self.total_lines_label.move(5, 400)
        
        self.code_wizard_button = QtWidgets.QPushButton("Code Wizard", self)
        self.code_wizard_button.resize(350, 30)
        self.code_wizard_button.move(5, 435)
        self.code_wizard_button.clicked.connect(self.open_code_wizard)
        
        self.status_label = QtWidgets.QLabel("Status: OK!", self)
        self.status_label.resize(350, 40)
        self.status_label.move(5, 460)
        
        self.code_creator_ok_button = QtWidgets.QPushButton("OK", self)
        self.code_creator_ok_button.resize(635, 30)
        self.code_creator_ok_button.move(5, 500)
        self.code_creator_ok_button.clicked.connect(self.save_xml)
        
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.code_edit.setFocus()
        self.is_code_valid()
        
        
    def check_validity(self, input_string):
        lines = input_string.strip().split('\n')
        for line in lines:
            if '#' in line:
                if len(line.strip()) != 18:
                    return False
            else:
                if len(line.strip()) != 17:
                    return False
                parts = line.strip().split()
                if len(parts) != 2:
                    return False
                if len(parts[0]) != 8 or len(parts[1]) != 8:
                    return False
                if not all(c in '0123456789ABCDEFabcdef' for c in (parts[0]+parts[1])):
                    return False
        return True


    def is_code_valid(self):

        if self.check_validity(self.code_edit.toPlainText()):
            self.code_creator_ok_button.setEnabled(True)
            self.code_edit.setStyleSheet("background-color: #00FF00;")
            self.code_edit.verticalScrollBar().setStyleSheet("background-color: lightGray;")
            self.status_label.setText("Status: OK!")
        else:
            self.code_creator_ok_button.setEnabled(False)
            self.code_edit.setStyleSheet("background-color: red;")
            self.code_edit.verticalScrollBar().setStyleSheet("background-color: lightGray;")
            self.status_label.setText("Status: Incorrect number of spaces/line breaks!")
            

    def format_code(self):
        code = self.code_edit.toPlainText()
        input_string = code.replace(" ", "").replace("\n", "")
        output_string = ""
        i = 0
        while i < len(input_string):
            if input_string[i] == "#":
                output_string += "#" + input_string[i+1:i+17]
                i += 17
            else:
                output_string += input_string[i:i+17]
                i += 17

        new_output_string = ""
        i = 0
        while i < len(output_string):
            if output_string[i] == "#":
                new_output_string += "#" + output_string[i+1:i+9] + " " + output_string[i+9:i+17]
                i += 17
            else:
                new_output_string += output_string[i:i+8] + " " + output_string[i+8:i+16]
                i += 16
            if i < len(output_string):
                new_output_string += "\n"
        self.code_edit.setPlainText(new_output_string.upper())

                  
    def save_xml(self):
    
        # Create root element if file doesn't exist
        if self.file_path == "":
            self.file_path = "null.xml"
        else:
            pass
        
        entry_name = self.title_edit.text()

        edited_entry = f"""<entry name="{self.title_edit.text()}">
        <code>{self.code_edit.toPlainText()}</code>
        <codeInputType>Cheat Code</codeInputType>
        <authors>{self.author_edit.text()}</authors>
        <raw_assembly>{str(self.raw_assembly_checkbox.isChecked()).lower()}</raw_assembly>
        <assembly_ram_write>{str(self.assembly_ram_write_checkbox.isChecked()).lower()}</assembly_ram_write>
        <comment>{self.comment_edit.toPlainText()}</comment>
        <enabled>true</enabled>
    </entry>"""
    
        appended_entry = f"""    <entry name="{self.title_edit.text()}">
        <code>{self.code_edit.toPlainText()}</code>
        <codeInputType>Cheat Code</codeInputType>
        <authors>{self.author_edit.text()}</authors>
        <raw_assembly>{str(self.raw_assembly_checkbox.isChecked()).lower()}</raw_assembly>
        <assembly_ram_write>{str(self.assembly_ram_write_checkbox.isChecked()).lower()}</assembly_ram_write>
        <comment>{self.comment_edit.toPlainText()}</comment>
        <enabled>false</enabled>
    </entry>
"""

        with open(self.file_path, 'r') as f:
            content = f.read()

            start_index = content.find('<entry name="' + entry_name + '">')
            end_index = content.find('</entry>', start_index) + len('</entry>')

            if end_index == -1:
                print(f'[QtGecko]: Invalid XML Format!')
            elif start_index == -1:
                print(f'[QtGecko]: Entry: {entry_name} does not exist. Creating it.')
                new_content = content.replace('</codes>', appended_entry + '</codes>')
                with open(self.file_path, 'w') as f:
                    f.write(new_content)
            else:
                print(f'[QtGecko]: Edited entry: {entry_name}')
                new_content = content[:start_index] + edited_entry + content[end_index:]
                with open(self.file_path, 'w') as f:
                    f.write(new_content)

        self.close()
        
    def open_code_wizard(self):
            self.window = ErrorWindow()
            self.window.CreateWindow("Welp..", f"This feature doesn't exist yet..", 280, 150)
            self.window.show()
