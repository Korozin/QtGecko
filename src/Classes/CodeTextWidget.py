from PyQt5 import QtCore, QtGui, QtWidgets

class LineNumberArea(QtWidgets.QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.setAutoFillBackground(True)

    def sizeHint(self):
        return QtCore.QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        palette = QtWidgets.QApplication.palette()  # use the application's palette instead of the editor's palette
        painter = QtGui.QPainter(self)
        color = palette.color(QtGui.QPalette.Window)
        painter.fillRect(event.rect(), color)

        fontMetrics = painter.fontMetrics()
        currentBlock = self.editor.firstVisibleBlock()
        top = self.editor.blockBoundingGeometry(currentBlock).translated(self.editor.contentOffset()).top()
        bottom = top + self.editor.blockBoundingRect(currentBlock).height()
        lineNumber = currentBlock.blockNumber() + 1

        while currentBlock.isValid() and top <= event.rect().bottom():
            if bottom >= event.rect().top():
                # Draw the line number
                lineNumberText = str(lineNumber)
                lineNumberRect = QtCore.QRect(0, int(top), self.width() - 6, fontMetrics.height())
                painter.drawText(lineNumberRect, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, lineNumberText)

            currentBlock = currentBlock.next()
            top = bottom
            bottom = top + self.editor.blockBoundingRect(currentBlock).height()
            lineNumber += 1


class Editor(QtWidgets.QPlainTextEdit, object):
    def __init__(self, parent=None):
        super(Editor, self).__init__(parent)
        self.lineNumberArea = LineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)

        # Highlight the current line immediately
        self.highlightCurrentLine()
        

    def lineNumberAreaWidth(self):
        digits = len(str(self.blockCount()))
        count = max(1, self.blockCount())
        space = 20 + self.fontMetrics().horizontalAdvance('10') + 10
        return space

    def updateLineNumberAreaWidth(self, newBlockCount):
        width = self.lineNumberAreaWidth()
        self.setViewportMargins(width, 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super(Editor, self).resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QtCore.QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QtWidgets.QTextEdit.ExtraSelection()
            lineColor = QtGui.QColor(QtCore.Qt.yellow).lighter(160)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)
