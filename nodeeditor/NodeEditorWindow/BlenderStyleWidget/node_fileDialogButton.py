import os
from PyQt5.QtWidgets import QSizePolicy, QFileDialog, QWidget, QLineEdit, QHBoxLayout, QPushButton
from PyQt5.QtGui import QIcon

from common.icon import FluentIcon
from .content_BaseSetting import ContentBaseSetting
from .node_pushButton import PushButton
from .node_lineEdit import LineEdit
    
class FileDialogWidget(QWidget, ContentBaseSetting):
    """ Custom FileDialog Widget

        Parameters :
        ---------
            icon (str): The icon displayed on the button.
            text (str): The text displayed on the button.
            parent (QWidget): The parent widget. Default is None.

        Attributes :
        ---------
            text (QLabel): The label displaying the current selection text.

        Usage :
        ---------
            widget = FileDialogWidget(text="Open Folder", filter="folder")
            widget = FileDialogWidget(text="Open File", filter=".mp4")
    """
    def __init__(self, icon:QIcon=None, text:str="Open File", filter="", parent=None, **kwargs):
        super().__init__(parent)
        self.icon = icon
        self.text = text
        self.filter = filter
        self.hBoxLayout = QHBoxLayout()

        self.hBoxLayout.setSpacing(1)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.fileDialogButton()
        self.setFixedHeight(self.content_height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setLayout(self.hBoxLayout)

        self.styles_set()

    def openFiles(self) -> tuple[list[str], str]:
        filePath , filterType = QFileDialog.getOpenFileName(filter=self.filter)
        if filePath: self.filePathEdit(filePath)
        if self.debug: print("node_FileDialogButton:: Open File: ", filePath , filterType)

        return filePath, filterType
    
    def openFolder(self) -> str:
        folderPath = QFileDialog.getExistingDirectory()
        if folderPath: self.filePathEdit(folderPath)
        if self.debug: print("node_FileDialogButton:: Open Folder: ",folderPath)

        return folderPath

    def fileDialogButton(self):
        self.removeWidgetInLayput()
        button = PushButton(icon=self.icon, text=self.text)
        # Use keyword to change different type
        if self.filter == "folder": button.clicked.connect(self.openFolder)
        else: button.clicked.connect(self.openFiles)

        self.hBoxLayout.addWidget(button)

    def filePathEdit(self, path):
        self.removeWidgetInLayput()
        self.lineEdit = LineEdit(isEmpty=False)
        self.openfolderButton = PushButton(icon=FluentIcon.FOLDER,text="")
        self.deletedButton = PushButton(icon=FluentIcon.CLOSE, text="")
        
        self.lineEdit.setText(str(path))
        self.openfolderButton.clicked.connect(self.openFolder)
        self.deletedButton.clicked.connect(self.fileDialogButton)
        
        self.hBoxLayout.addWidget(self.lineEdit, stretch=1)
        self.hBoxLayout.addWidget(self.openfolderButton)
        self.hBoxLayout.addWidget(self.deletedButton)

    def openFolder(self):
        path = self.lineEdit.text()
        if os.path.isfile(path):
            folder_path = os.path.dirname(path)
            os.startfile(folder_path)

    def removeWidgetInLayput(self):
        while self.hBoxLayout.count() > 0:
            item = self.hBoxLayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                del item