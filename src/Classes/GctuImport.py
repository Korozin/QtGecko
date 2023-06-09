if __name__ == "__main__":
    print("This is a module that is imported by 'QtGecko.py'. Don't run it directly.")
    exit()
else:
    import sys, re, webbrowser, \
           os, PyQt5

class ImportGCTUWindow(PyQt5.QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.xml_path = "null.xml"
        self.setWindowTitle('Import GCTU')
        self.setFixedSize(600, 100)
        
        main_layout = PyQt5.QtWidgets.QVBoxLayout(self)
        row1_layout = PyQt5.QtWidgets.QHBoxLayout()
        row2_layout = PyQt5.QtWidgets.QHBoxLayout()
        
        self.center_screen()
        
        file_name_label = PyQt5.QtWidgets.QLabel("File Name:")
        self.file_name_line_edit = PyQt5.QtWidgets.QLineEdit()
        self.file_name_line_edit.textChanged.connect(self.check_validity)
        self.browse_file_button = PyQt5.QtWidgets.QPushButton("...")
        self.browse_file_button.clicked.connect(self.browse_gctu_file)
        row1_layout.addWidget(file_name_label)
        row1_layout.addWidget(self.file_name_line_edit)
        row1_layout.addWidget(self.browse_file_button)
        
        self.confirm_button = PyQt5.QtWidgets.QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.on_confirm)
        row2_layout.addWidget(self.confirm_button)
        
        main_layout.addLayout(row1_layout)
        main_layout.addLayout(row2_layout)
        
        self.check_validity("")
        
    def center_screen(self):
        frame_geometry = self.frameGeometry()
        calculate_screen = PyQt5.QtWidgets.QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(calculate_screen)
        self.move(frame_geometry.topLeft())
        
    def on_confirm(self):
    
        file_name = self.file_name_line_edit.text()
    
        # Open the .gctu file
        with open(file_name,'rb') as f:
            output_string = f.read()
            f.close()

        # Read the file as upper-case Hex
        output_string = output_string.hex().upper()

        # Format the .gctu Contents into proper Code format
        new_output_string = ""
        for i in range(0, len(output_string), 16):
            new_output_string += output_string[i:i+8] + " " + output_string[i+8:i+16] + "\n"

        # Print the output string without an extra line break at the end
        new_output_string = new_output_string.strip("\n")
    
        new_entry = f"""    <entry name="Imported GCTU Codes">
        <code>{new_output_string}</code>
        <codeInputType>Cheat Code</codeInputType>
        <authors>QtGecko</authors>
        <raw_assembly>false</raw_assembly>
        <assembly_ram_write>false</assembly_ram_write>
        <comment>All codes imported from a GCTU file</comment>
        <enabled>false</enabled>
    </entry>
"""
        appended_entry = f"""<entry name="Imported GCTU Codes">
        <code>{new_output_string}</code>
        <codeInputType>Cheat Code</codeInputType>
        <authors>QtGecko</authors>
        <raw_assembly>false</raw_assembly>
        <assembly_ram_write>false</assembly_ram_write>
        <comment>All codes imported from a GCTU file</comment>
        <enabled>false</enabled>
    </entry>"""
        
        entry_name = "Imported GCTU Codes"

        with open(self.xml_path, 'r') as f:
            content = f.read()

            start_index = content.find('<entry name="' + entry_name + '">')
            end_index = content.find('</entry>', start_index) + len('</entry>')

            if end_index == -1:
                print(f'{colorama.Fore.MAGENTA}[QtGecko]: {colorama.Fore.RESET}Invalid XML Format!')
            elif start_index == -1:
                print(f'{colorama.Fore.MAGENTA}[QtGecko]: {colorama.Fore.RESET}Entry: {colorama.Fore.YELLOW}\'{entry_name}\' {colorama.Fore.RESET}does not exist. Creating it.')
                new_content = content.replace('</codes>', new_entry + '</codes>')
                with open(self.xml_path, 'w') as f:
                    f.write(new_content)
            else:
                print(f'{colorama.Fore.MAGENTA}[QtGecko]: {colorama.Fore.RESET}Edited entry: {colorama.Fore.YELLOW}\'{entry_name}\'{colorama.Fore.RESET}')
                new_content = content[:start_index] + appended_entry + content[end_index:]
                with open(self.xml_path, 'w') as f:
                    f.write(new_content)
                    
            self.close()
        
    def browse_gctu_file(self):
        dialog = PyQt5.QtWidgets.QFileDialog(self)
        dialog.setFileMode(PyQt5.QtWidgets.QFileDialog.ExistingFile)
        dialog.setOption(PyQt5.QtWidgets.QFileDialog.DontUseNativeDialog, False)
        
        # Add filters for XML and All files
        filters = ["GCTU Files (*.gctu)", "All Files (*.*)"]
        dialog.setNameFilters(filters)
        dialog.selectNameFilter(filters[0])
        
        # Sets the XML File Path if successfully selected, if not leave path empty
        if dialog.exec_():
            file_name = dialog.selectedFiles()[0]
            self.file_name_line_edit.setText(file_name)
        
    def check_file_exists(self, filepath):
        return os.path.exists(filepath)
        
    def check_validity(self, file_name):
        if self.check_file_exists(file_name):
            self.confirm_button.setEnabled(True)
            self.file_name_line_edit.setStyleSheet("background-color: #00FF00;")
        else:
            self.confirm_button.setEnabled(False)
            self.file_name_line_edit.setStyleSheet("background-color: red;")
