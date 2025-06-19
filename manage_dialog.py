from qgis.PyQt.QtWidgets import (
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QDialog,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
)
from qgis.PyQt.QtGui import QIcon

plus_icon = QIcon(':/qt-project.org/assistant/images/mac/plus.png')
minus_icon = QIcon(':/qt-project.org/assistant/images/mac/minus.png')


class ManageNotebooksDialog(QDialog):
    def __init__(self, curr_notebooks, curr_directory):
        super().__init__()
        self.curr_notebooks = curr_notebooks
        self.curr_directory = curr_directory
        self.success = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Manage Saved Notebooks')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.book_table = QTableWidget()
        self.book_table.setColumnCount(2)
        self.book_table.setHorizontalHeaderLabels(
            [
                'Nickname',
                'File Path',
            ]
        )
        for i in range(len(self.curr_notebooks) - 1):
            self.book_table.insertRow(i)
            name_item = QTableWidgetItem(self.curr_notebooks[i][0])
            self.book_table.setItem(i, 0, name_item)
            path_item = QTableWidgetItem(self.curr_notebooks[i][1])
            self.book_table.setItem(i, 1, path_item)
        self.layout.addWidget(self.book_table)
        self.top_button_layout = QHBoxLayout()
        self.plus_button = QPushButton(icon=plus_icon, text='', parent=self)
        self.minus_button = QPushButton(icon=minus_icon, text='', parent=self)
        self.plus_button.clicked.connect(self.findNotebook)
        self.minus_button.clicked.connect(self.removeNotebook)
        self.top_button_layout.addWidget(self.plus_button)
        self.top_button_layout.addWidget(self.minus_button)
        self.bottom_button_layout = QHBoxLayout()
        self.ok_button = QPushButton(text='Ok')
        self.ok_button.clicked.connect(self.submitValues)
        self.cancel_button = QPushButton(text='Cancel')
        self.cancel_button.clicked.connect(self.close)
        self.bottom_button_layout.addWidget(self.ok_button)
        self.bottom_button_layout.addWidget(self.cancel_button)
        self.layout.addLayout(self.top_button_layout)
        self.layout.addLayout(self.bottom_button_layout)

    def findNotebook(self):
        row = self.book_table.rowCount()
        new_notebook = QFileDialog.getOpenFileName(
            self,
            'Select Jupyter Notebook (.ipynb):',
            self.curr_directory,
            '*.ipynb',
            '',
            QFileDialog.Option.ReadOnly,
        )[0]
        self.book_table.insertRow(row)
        nickname_item = QTableWidgetItem('Nickname')
        self.book_table.setItem(row, 0, nickname_item)
        path_item = QTableWidgetItem(new_notebook)
        self.book_table.setItem(row, 1, path_item)

    def removeNotebook(self):
        selection = self.book_table.currentRow()
        if selection:
            self.book_table.removeRow(selection.row())

    def submitValues(self):
        self.saved_books = []
        for i in range(self.book_table.rowCount()):
            item = (self.book_table.item(i, 0).text(), self.book_table.item(i, 1).text())
            self.saved_books.append(item)
        self.success = True
        self.close()
