from collections import OrderedDict

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy, QTextEdit, QPlainTextEdit, QGraphicsView, QGraphicsScene

from ..Serialization.node_Serializable import Serializable
from common.style_sheet import StyleSheet
from BlenderStyleWidget import *
from config.debug import DebugMode

SOCKET_SPACE = 30
DEBUG = DebugMode.NODE_NODE

class NodeContentWidget(QWidget, Serializable):
    '''自製標準內部元件構造'''
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.node = node
        # super().__init__(parent)
        self.socketSpace = SOCKET_SPACE-7
        self.contentLists = []
        
        self.initUI()
        
        self.setStyleSheet("background-color: transparent;")
        
    def initUI(self):
        self.vboxLayout = QVBoxLayout()
        self.vboxLayout.setContentsMargins(0, 1, 3, 0)
        self.setLayout(self.vboxLayout)
    
    @StyleSheet.apply(StyleSheet.NODE_CONTENT)
    def addCheckbox(self, text:str, **kwargs):
        '''新增二態複選框'''
        checkbox = CheckBox(text, debug=DEBUG, **kwargs)
        self.vboxLayout.addWidget(checkbox)
        self.contentLists.append(
            ('checkbox', {
                'text': text,
                'status': False
            }))
        return checkbox
    
    @StyleSheet.apply(StyleSheet.NODE_CONTENT)
    def addComboBox(self, items:list=["List 1", "List 2", "List 3"], **kwargs):
        '''新增下拉式選單'''
        comboBox = ComboBox(**kwargs)
        comboBox.addItems(items)
        self.vboxLayout.addWidget(comboBox)
        self.contentLists.append(
            ('comboBox', {
                'items': items,
            }))
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
        self.contentLists.append(
            ('label', {
                'text': text,
                'isOutput': isOutput
            }))
        if DEBUG: label.setStyleSheet("color: white; border: 1px solid red;")
        return label
    
    @StyleSheet.apply(StyleSheet.NODE_CONTENT)
    def addLineEdit(self, text:str, **kwargs):
        lineEdit = LineEdit(text, self.width(), **kwargs)
        self.vboxLayout.addWidget(lineEdit)
        self.contentLists.append(
            ('lineEdit', {
                'text': text,
                'current_text': ""
            }))
        return lineEdit
    
    @StyleSheet.apply(StyleSheet.NODE_CONTENT)
    def addProgressBar(self, label:str="Value", minimum:int=0, maximum:int=10, **kwargs):
        '''新增可控制進度條'''
        progressBar = ControlledProgressBar(label=label, minimum=minimum, maximum=maximum, **kwargs)
        self.vboxLayout.addWidget(progressBar)
        self.contentLists.append(
            ('progressBar', {
                'label': label,
                'minium': minimum,
                'maxium': maximum,
                'value': 0.5
            }))
        return progressBar
    
    @StyleSheet.apply(StyleSheet.NODE_CONTENT)
    def addPushButton(self, text:str, **kwargs):
        '''新增按紐'''
        button = PushButton(text, **kwargs)
        self.vboxLayout.addWidget(button)
        self.contentLists.append(
            ('pushButton', {
                'text': text,
                'status': False
            }))
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

    # def setFixedHeightForAll(self):
    #     total_height = self.vboxLayout.sizeHint().height()  # 獲取 vBoxLayout 的總高度
    #     item_count = self.vboxLayout.count()  # 獲取 vBoxLayout 中元素的數量
    #     if item_count == 0:
    #         return
    #     avg_height = total_height // item_count  # 計算平均高度

    #     # 將每個元素的高度設置為平均高度
    #     for i in range(item_count):
    #         item_widget = self.vboxLayout.itemAt(i).widget()
    #         if item_widget is not None:
    #             item_widget.setFixedHeight(avg_height)

    def serialize(self):
        '''序列化資訊'''
        return False
    
    def deserialize(self, data, hashmap={}):
        self.vboxLayout.setContentsMargins(0, 3, 3, 0)
        for content in data:
            content_type = content['type']
            content_data = content['data']
            print("Type: ", content_type, ", Data: ", content_data)
            if content_type == 'checkbox': self.addCheckbox(content_data['text'])
            elif content_type == 'comboBox': self.addComboBox(content_data)
            elif content_type == 'label': self.addLabel(content_data['text'])
            elif content_type == 'lineEdit': self.addLineEdit(content_data['text'])
            elif content_type == 'progressBar': self.addProgressBar(content_data['label'], content_data['minium'], content_data['maxium'])
            elif content_type == 'pushButton': self.addPushButton(content_data['text'])
            else: print("\033[93m Wrong type.\033[0m")
        return True
    
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