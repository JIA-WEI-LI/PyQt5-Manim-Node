from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QPushButton, QSizePolicy, QProgressBar

from common.style_sheet import StyleSheet
from components.custom_checkbox import CheckBox
from components.custom_pushButton import PushButton
from components.custom_progressbar import ControlledProgressBar
from config.debug import DebugMode

SOCKET_SPACE = 30
DEBUG = DebugMode.NODE_NODE

class NodeContentWidget(QWidget):
    '''自製內部元件構造'''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.socketSpace = SOCKET_SPACE-7
        
        self.initUI()
        
        self.setStyleSheet("background-color: transparent;")
        
    def initUI(self):
        self.vboxLayout = QVBoxLayout()
        self.vboxLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vboxLayout)
        
    @StyleSheet.apply(StyleSheet.NODE_NODE)
    def addLabel(self, text:str, isOutput=False):
        '''新增文字標籤，並可根據輸入或輸出改變置左或置右'''
        label = QLabel(self)
        label.setObjectName("contentLabel")
        
        label.setText(text)
        label.setFixedHeight(self.socketSpace)
        if isOutput: label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.vboxLayout.addWidget(label)
        
        if DEBUG: label.setStyleSheet("color: white; border: 1px solid red;")
        
        return label
    
    def addPushButton(self, text:str):
        '''新增按紐'''
        button = PushButton(self)
        button.setObjectName("nodePushButton")
        button.setText(text)
        button.setFixedHeight(self.socketSpace)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.vboxLayout.addWidget(button)
        
        if DEBUG: button.setStyleSheet("color: white; border: 1px solid red;")
        
        return button
    
    def addCheckbox(self, text:str, isOutput:bool=False):
        '''新增二態複選框'''
        hLayoutBox = QHBoxLayout()
        checkbox = CheckBox()
        label = QLabel(text)
        label.setObjectName("nodeCheckboxLabel")
        
        checkbox.setFixedHeight(self.socketSpace)
        label.setFixedHeight(self.socketSpace)
        hLayoutBox.setContentsMargins(0, 0, 0, 0)
        hLayoutBox.addWidget(checkbox, stretch=1) if isOutput else hLayoutBox.addWidget(checkbox)
        hLayoutBox.addWidget(label) if isOutput else hLayoutBox.addWidget(label, stretch=1)
        self.vboxLayout.addLayout(hLayoutBox)
        
        if DEBUG: checkbox.setStyleSheet("border: 1px solid red;")
        if DEBUG: label.setStyleSheet("color: white; border: 1px solid red;")
        
        return checkbox, label
    
    def addProgressBar(self, minimum:int=0, maximum:int=10, initial_percent:float=0.5):
        '''新增可控制進度條'''
        progressBar = ControlledProgressBar(minimum=minimum, maximum=maximum, initial_percent=initial_percent)
        progressBar.setFixedHeight(self.socketSpace)
        progressBar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        progressBar.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.vboxLayout.addWidget(progressBar)

        return progressBar
    
    def setFixedHeightForAll(self):
        total_height = self.vboxLayout.sizeHint().height()  # 獲取 vBoxLayout 的總高度
        item_count = self.vboxLayout.count()  # 獲取 vBoxLayout 中元素的數量
        if item_count == 0:
            return
        avg_height = total_height // item_count  # 計算平均高度

        # 將每個元素的高度設置為平均高度
        for i in range(item_count):
            item_widget = self.vboxLayout.itemAt(i).widget()
            if item_widget is not None:
                item_widget.setFixedHeight(avg_height)