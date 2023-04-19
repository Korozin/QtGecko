import os, sys, math, base64, socket, webbrowser
from PyQt5 import QtWidgets, QtCore, QtGui
from functools import partial

# -------------------------------------- #
from Classes.uGecko import uGecko
from Classes.MainWindow import QtGecko_GUI
from Classes.ReadXML import read_names, see_enabled_codes, read_codes, read_ram_writes_only, read_cafe_codes_only, remove_extra_lines, read_code_comments, read_code_authors
from Classes.Verification import IP_Verification
from Classes.ConfigManager import ConfigManager
from Classes.ErrorWindow import ErrorWindow
from Classes.InfoWindow import InfoWindow
from Classes.CodeDocs import html_content, HTMLViewer
from Classes.SearchMenu import SearchMenu
from Classes.CodeCreator import CodeCreator
from Classes.GctuExport import ExportGCTUWindow
from Classes.GctuImport import ImportGCTUWindow
from Classes.DatatypeConversion import DatatypeConversion
from Classes.GeckoIcon import GeckoIcon
# -------------------------------------- #


class Main(QtWidgets.QMainWindow, QtGecko_GUI):
    def __init__(self, file_path):
        super(Main, self).__init__()
        
        # Set needed vars
        self.restore = 0
        self.file_path = file_path
        self.connection_timeout_timer = QtCore.QTimer()
        self.InfoWindow = InfoWindow()
        self.ErrorWindow = ErrorWindow()
        self.DatatypeConversion = DatatypeConversion()
        
        if not os.path.exists(self.file_path):
            os.makedirs("codes", exist_ok=True)
            with open(self.file_path, "w") as f:
                f.write('<codes>\n</codes>')
            print("[QtGecko]: Template XML created")

        # Config operations
        self.config_path = "config.ini"
        self.config_manager = ConfigManager(self.config_path)
        self.config_manager.print_config_values()
        self.set_theme = self.config_manager.theme_option
        
        # Set up GUI
        self.setupUi(self)
        self.center_screen()
        self.populate_codes_area()
        
        '''Connect function slots to graphical interface(s)'''
        
        # MainWindow interface #
        self.Connection_Bar.textChanged.connect(self.set_IPv4_validity)
        self.Connection_Bar.setText(self.config_manager.last_used_ipv4)
        self.Connect_Button.clicked.connect(self.connect)
        self.Disconnect_Button.clicked.connect(self.disconnect)
        self.Help_Button.clicked.connect(self.help)

        # Code(s) tab  #
        self.AddCode_Button.clicked.connect(self.open_code_creator)
        self.UntickAll_Button.clicked.connect(self.untick_all)
        self.ExportCodeList_Button.clicked.connect(self.export_code_list)
        self.SendCodes_Button.clicked.connect(self.send_all_codes)
        self.DisableCodes_Button.clicked.connect(self.disable_all_codes)
        self.LoadCodeList_Button.clicked.connect(self.load_code_list)
        self.CodeTypesDoc_Button.clicked.connect(self.open_code_docs)
        self.CodeTitleSearch_Button.clicked.connect(self.open_search_menu)
        self.ExportGCTU_Button.clicked.connect(self.export_gctu_process)
        self.ImportGCTU_Button.clicked.connect(self.import_gctu_process)
        self.DownloadCodes_Button.clicked.connect(self.download_codes_button_fun)

        # Miscellaneous tab  #
        self.WiiUFirmware_Button.clicked.connect(self.get_wiiu_firmware)
        self.GeckoServerVersion_Button.clicked.connect(self.get_tcp_server_version)
        self.LocalIP_Button.clicked.connect(self.show_local_ip)
        self.BuildDate_Button.clicked.connect(self.show_build_date)
        self.BugTracker_Button.clicked.connect(self.open_bug_tracker)
        self.DataTypeConversion_Button.clicked.connect(self.open_datatype_conversion)
        self.ConnectionTimeout_Checkbox.stateChanged.connect(self.connection_timeout_changed)
        
        '''Configure Theme ComboBox'''
        self.SetTheme_ComboBox.addItems(QtWidgets.QStyleFactory.keys())
        self.SetTheme_ComboBox.setCurrentText(self.config_manager.theme_option)
        self.SetTheme_ComboBox.currentIndexChanged.connect(self.change_theme)
        
        # Set Connection Timeout Checkbox based on Config
        if str(self.config_manager.connection_timeout_option) == "True":
            self.ConnectionTimeout_Checkbox.setChecked(True)
        elif str(self.config_manager.connection_timeout_option) == "False":
            self.ConnectionTimeout_Checkbox.setChecked(False)

        # External Tools Tab #
        self.TCPGeckoInstaller_Button.clicked.connect(self.download_tcp_gecko)
        
    ### MainWindow functions start ###
    def center_screen(self):
        frame_geometry = self.frameGeometry()
        calculate_screen = QtWidgets.QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(calculate_screen)
        self.move(frame_geometry.topLeft())
        
    def set_IPv4_validity(self):
        # Set QtWidgets.QLineEdit style based on IPv4 Validity
        if IP_Verification(self.Connection_Bar.text()):
            self.Connection_Bar.setStyleSheet("background-color: #00FF00;")
            self.Connect_Button.setEnabled(True)
        else:
            self.Connection_Bar.setStyleSheet("background-color: red;")
            self.Connect_Button.setEnabled(False)
            
    def connect(self):
        # Write user's IPv4 to config
        self.config_manager.write_ipv4(self.Connection_Bar.text())

        try:
            #self.tcp_con = TCPGecko(self.Connection_Bar.text())
            self.tcp_con = uGecko(self.Connection_Bar.text())
            self.tcp_con.connect()
            
            # Determine whether or not to call the timeout function based on checkbox status
            if self.config_manager.connection_timeout_option == "False":
                pass
            elif self.config_manager.connection_timeout_option == "True":
                self.connection_timeout_timer.start(1800000) # 30 minute time-frame
                self.connection_timeout_timer.timeout.connect(self.disconnect)
            else:
                print("[QtGecko]: How the hell did you even get this error?")
                pass

            # Set proper GUI elements based on connectivity
            self.SendCodes_Button.setEnabled(True)
            self.Disconnect_Button.setEnabled(True)
            self.DisableCodes_Button.setEnabled(True)
            self.WiiUFirmware_Button.setEnabled(True)
            self.Connect_Button.setEnabled(False)
            self.Connection_Bar.deselect()

            self.MainWindow.setWindowTitle(f"QtGecko | {self.tcp_con.getTitleID()}")

            self.InfoWindow.CreateWindow("Connection Success!", f"Connected successfully!.", 300, 150)
            self.InfoWindow.show()

        except Exception as e:
            self.ErrorWindow.CreateWindow("Connection Error!", f"<b></b>Used IPv4: {self.Connection_Bar.text()}<br/>Error: {e}.<br/><br/>If you're unable to connect, then submit an issue on <a href='https://github.com/Korozin/QtGecko/issues'>GitHub</a>, or consult the <a href='https://github.com/Korozin/QtGecko/blob/main/SETUP-GUIDE.md'>Setup Guide</a>.", 500, 200)
            self.ErrorWindow.show()

            print("[uGecko]: Connection attempt failed.. :(")

    def disconnect(self):
        try:
            self.tcp_con.disconnect()

            self.SendCodes_Button.setEnabled(False)
            self.Disconnect_Button.setEnabled(False)
            self.DisableCodes_Button.setEnabled(False)
            self.WiiUFirmware_Button.setEnabled(False)
            self.Connect_Button.setEnabled(True)
            self.Connection_Bar.deselect()
        except Exception as e:
            self.window = ErrorWindow()
            self.window.CreateWindow("Error!", f"<b></b>Used IPv4: {self.Connection_Bar.text()}<br/>Error: {e}.", 500, 200)
            self.window.show()

    def help(self):
        self.InfoWindow.CreateWindow("Help", "If you can't connect, then make sure to follow the <a href='https://github.com/Korozin/QtGecko/blob/main/SETUP-GUIDE.md'>setup guide</a>.<br/><br/>If you're still having issues then please submit an issue on <a href='https://github.com/Korozin/QtGecko/issues'>GitHub</a>.", 500, 200)
        self.InfoWindow.show()
    ### MainWindow functions end ###
    
    ### Codes Tab functions start ###
    def open_code_creator(self):
        self.Code_Creator_Window = CodeCreator(self.file_path)
        self.Code_Creator_Window.show()
        self.Code_Creator_Window.code_creator_ok_button.clicked.connect(self.refresh_gui)
        
    def populate_codes_area(self):
        # Read the names from the XML file and create a checkbox for each entry
        names = read_names(self.file_path)
        enabled_list = see_enabled_codes(self.file_path)
        self.checkbox_widget = QtWidgets.QWidget(self.Checkbox_ScrollArea)
        self.checkbox_layout = QtWidgets.QVBoxLayout(self.checkbox_widget)
        self.Checkbox_ScrollArea.setWidget(self.checkbox_widget)
        self.checkboxes = []
        for name, enabled in zip(names, enabled_list):
            self.checkbox = QtWidgets.QCheckBox(f"{name}", self)
            if enabled == "true":
                enabled = True
            else:
                enabled = False
            self.checkbox.setChecked(enabled)
            self.checkbox_layout.addWidget(self.checkbox)
            self.checkboxes.append(self.checkbox)
            
        self.TotalCodes_Label.setText(f"Total Code Count: {len(self.checkboxes)}")
        
        # Connect the checkboxes to the function to update the text edit
        for i, self.checkbox in enumerate(self.checkboxes):
            self.checkbox.stateChanged.connect(partial(self.update_code_text_fields, i))
            
            if self.checkbox.isChecked():
                self.update_code_text_fields(i)
                
    def refresh_gui(self):
        for checkbox in self.checkboxes:
            checkbox.deleteLater()
        names = read_names(self.file_path)
        enabled_list = see_enabled_codes(self.file_path)
        self.checkboxes = []
        for name, enabled in zip(names, enabled_list):
            self.checkbox = QtWidgets.QCheckBox(f"{name}", self)
            if enabled == "true":
                enabled = True
            else:
                enabled = False
            self.checkbox.setChecked(enabled)
            self.checkbox_layout.addWidget(self.checkbox)
            self.checkboxes.append(self.checkbox)
            
        self.TotalCodes_Label.setText(f"Total Code Count: {len(self.checkboxes)}")
            
        # Connect the checkboxes to the function to update the text edit
        for i, self.checkbox in enumerate(self.checkboxes):
            self.checkbox.stateChanged.connect(partial(self.update_code_text_fields, i))
            
            if self.checkbox.isChecked():
                self.update_code_text_fields(i)
                
    # Function to update the text edit with the code of the selected entry
    def update_code_text_fields(self, index):
        try:
            name = self.checkboxes[index].text()
            codes = read_codes(self.file_path, name)
            comments = read_code_comments(self.file_path, name)
            authors = read_code_authors(self.file_path, name)
            arw = read_ram_writes_only(self.file_path, name)

            if codes:
                code_str = "\n".join(codes)
                comment_str = "\n".join(comments)
                author_str = "\n".join(authors)
                arw_str = "\n".join(arw)
                self.SelectedCode_Text.setPlainText(code_str)
                self.SelectedCodeComment_Text.setText(comment_str)
            
            checked_checkboxes = self.get_checked_checkboxes(self.Checkbox_ScrollArea)
            selected_codes = []
            for checkbox in checked_checkboxes:
                codes = read_codes(self.file_path, checkbox)
                code_str = "\n".join(codes)
                selected_codes.append(code_str)
            code_str = "\n".join(selected_codes)
            code_str = len(code_str.split("\n"))
            self.ActiveCodeLines_Label.setText(f"Active Code Lines: {code_str}")
            self.ActiveCodes_Label.setText(f"Active Codes: {len(selected_codes)}")
            self.WhichCode_Label.setText(f"Code Name: {name}")

            if author_str == "":
                self.Author_Label.setText(f"Code Author: None")
            else:
                self.Author_Label.setText(f"Code Author: {author_str}")

            if arw_str == "":
                self.ARW_Label.setText("Is Assembly RAM Write? : False")
            else:
                self.ARW_Label.setText("Is Assembly RAM Write? : True")
        except Exception as e:
            pass
            
    def untick_all(self):
        for checkbox in self.checkboxes:
            checkbox.setChecked(False)
            
    def export_code_list(self):
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "", "XML Files (*.xml)", options=options)
        
        if file_name:
            with open(self.file_path, 'r') as f:
                contents = f.read()

            with open(file_name, 'w') as f:
                f.write(contents)

    def send_ram_writes(self):
        checked_checkboxes = self.get_checked_checkboxes(self.Checkbox_ScrollArea)
        codes = [read_ram_writes_only(self.file_path, checkbox) 
                for checkbox in checked_checkboxes]
        code_str = remove_extra_lines('\n'.join('\n'.join(c for c in code) for code in codes))

        if codes == [[]] or codes == []:
            pass
        else:
            for line in code_str.split("\n"):
                if "#" not in line:
                    addr, value = line.split()
                    addr = int(addr, 16)
                    value = int(value, 16)
                    self.tcp_con.kernelWrite(addr, value)

    def send_cafe_codes(self):
        checked_checkboxes = self.get_checked_checkboxes(self.Checkbox_ScrollArea)
        selected_codes = ['\n'.join(read_cafe_codes_only(self.file_path, checkbox)) for checkbox in checked_checkboxes]
        
        if selected_codes == [''] or selected_codes == []:
            pass
        else:
            cafe_code = [line.replace(' ', '') for line in ''.join(selected_codes).split('\n') if '#' not in line]
            cafe_code = ''.join(cafe_code)
    
            hex_bytes = [bytes.fromhex(hexstr) for hexstr in ['03', '03']]
            for x in range(self.restore):
                hex_bytes += [bytes.fromhex(f'0{0x1133000+x*4:X}00000000')] * 2
    
            for i, chunk in enumerate([cafe_code[x*8:x*8+8] for x in range(math.floor(len(cafe_code)/8))]):
                hex_bytes += [bytes.fromhex(f'0{0x1133000+i*4:X}{chunk}'), bytes.fromhex('03')]
    
            hex_bytes += [bytes.fromhex('10014CFC00000001')]
            self.restore = i
    
            for hex_bytes_item in hex_bytes:
                self.tcp_con.__socket.send(hex_bytes_item)

    def send_all_codes(self):
        try:
            self.send_ram_writes()
            self.send_cafe_codes()
        except Exception as e:
            self.window = ErrorWindow()
            self.window.CreateWindow("Code Error!", f"<b></b>Used IPv4: {self.Connection_Bar.text()}<br/>Error: {e}.", 500, 200)
            self.window.show()

    def disable_ram_writes(self):
        checked_checkboxes = self.get_checked_checkboxes(self.Checkbox_ScrollArea)
        codes = [read_ram_writes_only(self.file_path, checkbox) 
                for checkbox in checked_checkboxes]
        code_str = remove_extra_lines('\n'.join('\n'.join(c for c in code) for code in codes))

        if codes == [[]] or codes == []:
            pass
        else:
            for line in code_str.split("\n"):
                if "#" in line:
                    line = line.replace("#", "")
                    addr, value = line.split()
                    addr = int(addr, 16)
                    value = int(value, 16)
                    self.tcp_con.kernelWrite(addr, value)

    def disable_cafe_codes(self):
        checked_checkboxes = self.get_checked_checkboxes(self.Checkbox_ScrollArea)
        codes = [read_cafe_codes_only(self.file_path, checkbox) 
                for checkbox in checked_checkboxes]
        code_str = remove_extra_lines('\n'.join('\n'.join(c for c in code) for code in codes))

        if codes == [''] or codes == []:
            pass
        else:
            for line in code_str.split("\n"):
                if "#" in line:
                    line = line.replace("#", "")
                    addr, value = line.split()
                    addr = int(addr, 16)
                    value = int(value, 16)
                    self.tcp_con.kernelWrite(addr, value)

            self.tcp_con.__socket.send(bytes.fromhex('03'))
            for x in range(self.restore):
                self.tcp_con.__socket.send(bytes.fromhex('03'))
                self.tcp_con.__socket.send(bytes.fromhex('0'+format(0x1133000+x*4,'X')+'00000000'))
            self.tcp_con.__socket.send(bytes.fromhex('03'))
            self.tcp_con.__socket.send(bytes.fromhex('10014CFC00000001'))

    def disable_all_codes(self):
        try:
            self.disable_ram_writes()
            self.disable_cafe_codes()
        except Exception as e:
            self.window = ErrorWindow()
            self.window.CreateWindow("Code Error!", f"<b></b>Used IPv4: {self.Connection_Bar.text()}<br/>Error: {e}.", 500, 200)
            self.window.show()
                
    def load_code_list(self):
        # Create a dialog to allow the user to select their file
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        dialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, False)

        # Add filters for XML and All files
        filters = ["XML Files (*.xml)", "All Files (*.*)"]
        dialog.setNameFilters(filters)
        dialog.selectNameFilter(filters[0])

        # Sets the XML File Path if successfully selected, if not leave path empty
        if dialog.exec_():
            self.file_path = dialog.selectedFiles()[0]
        else:
            self.file_path = "./codes/null.xml"
            
        self.refresh_gui()
        
    def open_code_docs(self):
        '''If you'd rather open the link in your browser, then uncomment this line, and comment the 2 class lines'''
        #webbrowser.open("http://web.archive.org/web/20171108014746/http://cosmocortney.ddns.net:80/enzy/cafe_code_types_en.php")
        self.CodeDocsViewer = HTMLViewer(html_content)
        self.CodeDocsViewer.show()
        
    def open_search_menu(self):
        # Create instance of SearchMenu class and show it
        self.search_menu = SearchMenu(self.checkboxes, self.Checkbox_ScrollArea)
        self.search_menu.show()
        
    def get_checked_checkboxes(self, scroll_area):
        checked_checkboxes = []
        checked_checkboxes_text = []

        for widget in scroll_area.widget().children():
            if isinstance(widget, QtWidgets.QCheckBox) and widget.isChecked():
                checked_checkboxes.append(widget)
                checked_checkboxes_text.append(widget.text())

        return checked_checkboxes_text
        
    def export_gctu_process(self):
        checked_checkboxes = self.get_checked_checkboxes(self.Checkbox_ScrollArea)
        selected_codes = []
        for checkbox in checked_checkboxes:
            codes = read_codes(self.file_path, checkbox)
            code_str = "\n".join(codes)
            selected_codes.append(code_str)
        code_str = "\n".join(selected_codes)
        
        self.ExportGCTUWindow = ExportGCTUWindow(code_str)
        self.ExportGCTUWindow.show()
        
    def import_gctu_process(self):
        self.ImportGCTUWindow = ImportGCTUWindow()
        self.ImportGCTUWindow.show()
        self.ImportGCTUWindow.confirm_button.clicked.connect(self.refresh_gui)
        
    def download_codes_button_fun(self):
        webbrowser.open("https://github.com/MinecraftWiiUCodes/MinecraftWiiUPlaza")
    ### Codes Tab functions end ###

    ### Miscellaneous Tab functions ###
    def get_wiiu_firmware(self):
        self.InfoWindow.CreateWindow("Wii U Firmware Version", f"Firmware Version: {self.tcp_con.getOsVersion()}", 320, 150)
        self.InfoWindow.show()

    def show_local_ip(self):
        self.InfoWindow.CreateWindow("Local IPv4", f"Host name: {socket.gethostname()}<br/>Host IPv4: {socket.gethostbyname(socket.gethostname())}", 320, 150)
        self.InfoWindow.show()

    def get_tcp_server_version(self):
        self.InfoWindow.CreateWindow("Server Version", f"TCPGecko Server Version: {self.tcp_con.getServerVersion()}", 320, 150)
        self.InfoWindow.show()

    def show_build_date(self):
        self.InfoWindow.CreateWindow("Build Date", "April 19, 2023, 02:44:35 PM", 280, 150)
        self.InfoWindow.show()

    def open_bug_tracker(self):
        webbrowser.open("https://github.com/Korozin/QtGecko/issues")

    def open_datatype_conversion(self):
        self.DatatypeConversion.show()
        self.DatatypeConversion.copy_button.clicked.connect(self.DatatypeConversion.close)
        
    def connection_timeout_changed(self):
        if self.ConnectionTimeout_Checkbox.isChecked():
            self.config_manager.write_timeout_true()
        elif not self.ConnectionTimeout_Checkbox.isChecked():
            self.config_manager.write_timeout_false()
        else:
            print("[QtGecko]: How the hell did you even get this error?")
            pass

    def change_theme(self, index):
        theme_name = self.SetTheme_ComboBox.currentText()
        QtWidgets.QApplication.setStyle(theme_name)
        print(f"[QtGecko]: Theme changed to: {theme_name}")
        self.config_manager.write_theme(theme_name)
    ### Miscellaneous Tab functions end ###

    ### External Tools tab functions ###
    def download_tcp_gecko(self):
        webbrowser.open("https://github.com/BullyWiiPlaza/tcpgecko/archive/master.zip")
    ### External Tools tab functions end ###

def set_icon(QApp):
    decoded_data = base64.b64decode(GeckoIcon)
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(decoded_data)
    QApp.setWindowIcon(QtGui.QIcon(pixmap))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    set_icon(app)
    window = Main("./codes/null.xml")
    app.setStyle(window.set_theme)
    window.show()
    sys.exit(app.exec_())
