import os
from PyQt5.QtWidgets import QPushButton, QSizePolicy, QFileDialog
from PyQt5.QtGui import QIcon

from .content_BaseSetting import ContentBaseSetting

class FileDialogButton(QPushButton, ContentBaseSetting):
    """ Custom FileDialog PushButton

        Parameters :
        ---------
            text (str): The text displayed on the button label.
            parent (QWidget): The parent widget. Default is None.

        Attributes :
        ---------
            text (QLabel): The label displaying the current selection text.

        Usage :
        ---------
            label = FileDialogButton(text="Open Folder", filter="folder")
            label = FileDialogButton(text="Open File", filter=".mp4")
    """
    def __init__(self, icon:QIcon=None, text:str="Open File", filter="", parent=None, **kwargs):
        super().__init__(parent)
        self.filter = filter

        self.setText(text)
        self.setFixedHeight(self.content_height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        if isinstance(icon, str):
            if os.path.isfile(icon):
                self.setIcon(QIcon(icon))
        elif isinstance(icon, QIcon):
            self.setIcon(icon)

        if filter == "folder":
            self.clicked.connect(self.openFolder)
        else:
            self.clicked.connect(self.openFiles)

        self.setObjectName("fileDialogButton")
        self.styles_set()

    def openFiles(self) -> tuple[list[str], str]:
        filePath , filterType = QFileDialog.getOpenFileNames(filter=self.filter)
        if self.debug: print("node_FileDialogButton:: Open File: ", filePath , filterType)

        return filePath, filterType
    
    def openFolder(self) -> str:
        folderPath = QFileDialog.getExistingDirectory()
        if self.debug: print("node_FileDialogButton:: Open Folder: ",folderPath)

        return folderPath