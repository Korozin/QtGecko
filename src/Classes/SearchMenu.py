if __name__ == "__main__":
    print("This is a module that is imported by 'QtGecko.py'. Don't run it directly.")
    exit()
else:
    import PyQt5

class SearchMenu(PyQt5.QtWidgets.QWidget):

    def __init__(self, checkboxes, scroll_area):
        super().__init__()

        self.checkboxes = checkboxes
        self.scroll_area = scroll_area

        self.setWindowTitle("Search Results")
        self.setMinimumSize(300, 250)

        # Add layout for search results
        results_layout = PyQt5.QtWidgets.QVBoxLayout()
        self.setLayout(results_layout)
        self.center_screen()

        # Create QLineEdit for filtering results
        filter_edit = PyQt5.QtWidgets.QLineEdit(self)
        results_layout.addWidget(filter_edit)

        # Create scroll area and layout for filtered results
        scroll_area = PyQt5.QtWidgets.QScrollArea(self)
        scroll_widget = PyQt5.QtWidgets.QWidget(self)
        filtered_layout = PyQt5.QtWidgets.QVBoxLayout(scroll_widget)
        scroll_widget.setLayout(filtered_layout)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        results_layout.addWidget(scroll_area)

        # Add a button for each checkbox
        buttons = []
        for checkbox in self.checkboxes:
            button_text = checkbox.text()
            button = PyQt5.QtWidgets.QPushButton(button_text, self)
            button.clicked.connect(lambda _, b=checkbox: self.check_box(b))
            buttons.append(button)
            filtered_layout.addWidget(button)

        # Connect QLineEdit's textEdited signal to filter_results function
        filter_edit.textEdited.connect(lambda text: self.filter_results(text, buttons))

    def center_screen(self):
        frame_geometry = self.frameGeometry()
        calculate_screen = PyQt5.QtWidgets.QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(calculate_screen)
        self.move(frame_geometry.topLeft())

    def check_box(self, checkbox):
        checkbox.setChecked(True)
        checkbox_pos = checkbox.geometry().topLeft()
        self.scroll_area.ensureVisible(checkbox_pos.x(), checkbox_pos.y())
        self.close()

    def filter_results(self, text, buttons):
        for button in buttons:
            if text.lower() in button.text().lower():
                button.show()
            else:
                button.hide()
