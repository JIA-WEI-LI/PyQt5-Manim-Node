from collections import OrderedDict

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy, QTextEdit, QPlainTextEdit, QGraphicsView, QGraphicsScene

from ..Serialization.node_Serializable import Serializable
from common.style_sheet import StyleSheet
from components import *
from config.debug import DebugMode

SOCKET_SPACE = 30
DEBUG = DebugMode.NODE_NODE

class NodeContentWidget(QWidget, Serializable):
    '''自製標準內部元件構造'''
    def __init__(self, node, parent=None):
        # super().__init__(parent)
        self.node = node
        super().__init__(parent)
        self.socketSpace = SOCKET_SPACE-7
        
        self.initUI()
        
        self.setStyleSheet("background-color: transparent;")
        
    def initUI(self):
        self.vboxLayout = QVBoxLayout()
        self.vboxLayout.setContentsMargins(0, 0, 3, 0)
        self.setLayout(self.vboxLayout)
    
    @StyleSheet.apply(StyleSheet.NODE_CONTENT)
    def addCheckbox(self, text:str, **kwargs):
        '''新增二態複選框'''
        checkbox = CheckBox(text, **kwargs)

        checkbox.setFixedHeight(self.socketSpace)
        checkbox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.vboxLayout.addWidget(checkbox)
        
        if DEBUG: checkbox.setStyleSheet("border: 1px solid red;")
        
        return checkbox
    
    @StyleSheet.apply(StyleSheet.NODE_CONTENT)
    def addComboBox(self, items:list=["List 1", "List 2", "List 3"], **kwargs):
        '''新增下拉式選單'''
        comboBox = ComboBox(**kwargs)
        comboBox.setFixedHeight(self.socketSpace)
        comboBox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        comboBox.addItems(items)

        self.vboxLayout.addWidget(comboBox)
        if DEBUG: comboBox.setStyleSheet("border: 1px solid red;")

        return comboBox
    
    @StyleSheet.apply(StyleSheet.NODE_CONTENT)
    def addLabel(self, text:str, isOutput=False, **kwargs):
        '''新增文字標籤，並可根據輸入或輸出改變置左或置右'''
        tooltip = kwargs.get("tooltip", "")
        
        label = QLabel(self)
        label.setObjectName("contentLabel")
        
        label.setText(text)
        label.setFixedHeight(self.socketSpace)
        if isOutput: label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.vboxLayout.addWidget(label)

        self.setToolTip(text) if tooltip=="" else self.setToolTip(tooltip)
        
        if DEBUG: label.setStyleSheet("color: white; border: 1px solid red;")
        
        return label
    
    @StyleSheet.apply(StyleSheet.NODE_CONTENT)
    def addLineEdit(self, text:str, **kwargs):
        lineEdit = LineEdit(text, self.width(), **kwargs)
        lineEdit.setFixedHeight(self.socketSpace)
        self.vboxLayout.addWidget(lineEdit)

        if DEBUG: lineEdit.setStyleSheet("border: 1px solid red;")
        return lineEdit
    
    @StyleSheet.apply(StyleSheet.NODE_CONTENT)
    def addProgressBar(self, label:str="Value", minimum:int=0, maximum:int=10, **kwargs):
        '''新增可控制進度條'''
        progressBar = ControlledProgressBar(label=label, minimum=minimum, maximum=maximum, **kwargs)
        progressBar.setFixedHeight(self.socketSpace)
        progressBar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        progressBar.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.vboxLayout.addWidget(progressBar)

        return progressBar
    
    @StyleSheet.apply(StyleSheet.NODE_CONTENT)
    def addPushButton(self, text:str, **kwargs):
        '''新增按紐'''
        button = PushButton(text, **kwargs)
        button.setFixedHeight(self.socketSpace-1)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.vboxLayout.addWidget(button)
        
        if DEBUG: button.setStyleSheet("color: white; border: 1px solid red;")
        
        return button

    @StyleSheet.apply(StyleSheet.NODE_CONTENT)
    def addSpinBox(self, label:str="Value", **kwargs):
        '''新增可控制數值調整器'''
        spinBox = SpinBox(label=label, **kwargs)
        spinBox.setFixedHeight(self.socketSpace)
        spinBox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        spinBox.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.vboxLayout.addWidget(spinBox)

        return spinBox

    def setEditingFlag(self, value):
        self.node.scene.nodeGraphicsScene.views()[0].editingFlag = value

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

    def serialize(self):
        '''序列化資訊'''
        return OrderedDict([
            
        ])
    
    def deserialize(self, data, hashmap={}):
        raise False
    
class NodeContentWidgetDefault(QWidget):
    '''預設文字介紹'''
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.initUI()
        
    def initUI(self):
        self.vboxLayout = QVBoxLayout()
        self.vboxLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vboxLayout)
        
        self.label = QLabel("Some Title")
        self.vboxLayout.addWidget(self.label)
        self.vboxLayout.addWidget(QTextEdit("foo"))