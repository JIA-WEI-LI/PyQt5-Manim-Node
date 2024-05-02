from collections import OrderedDict

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy, QTextEdit, QPlainTextEdit, QGraphicsView, QGraphicsScene

from ..Serialization.node_Serializable import Serializable
from common.style_sheet import StyleSheet
from ..BlenderStyleWidget import *
from config.debug import DebugMode

SOCKET_SPACE = 30
DEBUG = DebugMode.NODE_NODE

class NodeContentWidget(QWidget, Serializable):
    '''自製標準內部元件構造'''
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.node = node
        self.socketSpace = SOCKET_SPACE-7
        self.contentLists = []
        
        self.initUI()
        
        self.setStyleSheet("background-color: transparent;")
        
    def initUI(self):
        self.vboxLayout = QVBoxLayout()
        self.vboxLayout.setContentsMargins(0, 0, 3, 0)
        self.setLayout(self.vboxLayout)
    
    @StyleSheet.apply(StyleSheet.NODE_CONTENT)
    def addCheckbox(self, text:str, **kwargs):
        '''新增二態複選框'''
        checkbox = CheckBox(text, debug=DEBUG, **kwargs)
        self.vboxLayout.addWidget(checkbox)
        self.contentLists.append(
            ('checkbox', {
                'text': text,
                'status': False,
                'tooltip': kwargs.get("tooltip", "")
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
                'list': items,
                'tooltip': kwargs.get("tooltip", "")
            }))
        return comboBox
    
    @StyleSheet.apply(StyleSheet.NODE_CONTENT)
    def addLabel(self, text:str, isOutput=False, **kwargs):
        '''新增文字標籤，並可根據輸入或輸出改變置左或置右'''
        label = Label(text, **kwargs)
        if isOutput: label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.vboxLayout.addWidget(label)
        self.contentLists.append(
            ('label', {
                'text': text,
                'isOutput': isOutput,
                'tooltip': kwargs.get("tooltip", "")
            }))
        return label
    
    @StyleSheet.apply(StyleSheet.NODE_CONTENT)
    def addLineEdit(self, text:str, **kwargs):
        '''新增單行文字輸入框'''
        lineEdit = LineEdit(text, self.width(), **kwargs)
        self.vboxLayout.addWidget(lineEdit)
        self.contentLists.append(
            ('lineEdit', {
                'text': text,
                'current_text': "",
                'tooltip': kwargs.get("tooltip", "")
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
                'value': 0.5,
                'tooltip': kwargs.get("tooltip", "")
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
                'status': False,
                'tooltip': kwargs.get("tooltip", "")
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

    def serialize(self):
        '''序列化資訊'''
        return False
    
    def deserialize(self, data, hashmap={}):
        for content in data:
            content_type = content['type']
            content_data = content['data']
            if DEBUG: print("Type: ", content_type, ", Data: ", content_data)
            if content_type == 'checkbox': 
                obj = self.addCheckbox(
                    content_data['text'], 
                    tooltip=content_data['tooltip'])
            elif content_type == 'comboBox': 
                obj = self.addComboBox(
                    content_data['list'], 
                    tooltip=content_data['tooltip'])
            elif content_type == 'label': 
                obj = self.addLabel(
                    content_data['text'], 
                    isOutput=content_data['isOutput'], 
                    tooltip=content_data['tooltip'])
            elif content_type == 'lineEdit': 
                obj = self.addLineEdit(
                    content_data['text'], 
                    tooltip=content_data['tooltip'])
            elif content_type == 'progressBar': 
                obj = self.addProgressBar(
                    content_data['label'], 
                    content_data['minium'],
                    content_data['maxium'], 
                    initial_percent=content_data['value'], 
                    tooltip=content_data['tooltip'])
            elif content_type == 'pushButton': 
                obj = self.addPushButton(
                    content_data['text'], 
                    tooltip=content_data['tooltip'])
            else: print("\033[93m Wrong type.\033[0m")
        return True