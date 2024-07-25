from typing import Union
from collections import OrderedDict

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy

from ..Serialization.node_Serializable import Serializable
# from ..BlenderStyleWidget import *
from BlenderWidget import *
from common import *

SOCKET_SPACE = 30
DEBUG = DebugMode.NODE_NODE

class NodeContentWidget(QWidget, Serializable):
    '''自製標準內部元件構造'''
    # TODO: 未來改使用 QToolBox 方便新增與調用 
    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)
        self.socketSpace = SOCKET_SPACE-7
        self.contentLists = []
        
        self.initUI()
        
        self.setStyleSheet("background-color: transparent;")
        
    def initUI(self):
        self.vboxLayout = QVBoxLayout()
        self.vboxLayout.setContentsMargins(0, 3, 3, 0)
        self.setLayout(self.vboxLayout)

    def addPushButton(self, icon:QIcon=None, text:str="", **kwargs):
        button = PushButton(icon=icon, text=text, **kwargs)
        self.vboxLayout.addWidget(button)
        self.node.graphicsNode.height += 30
        self.contentLists.append(
            ('pushButton', {
                'icon': icon,
                'text': text,
                'tooltip': kwargs.get("tooltip", "")
            }))
        return button
    
    def addInputLabel(self, text:str="Input Label", **kwargs):
        label = Label(text, **kwargs)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.vboxLayout.addWidget(label)
        self.node.graphicsNode.height += 30
        self.contentLists.append(
            ('inputLabel', {
                'text': text,
                'tooltip': kwargs.get("tooltip", "")
            }))
        return label
    
    def addLineEdit(self, label:str="", **kwargs):
        lineEdit = LineEdit(**kwargs)
        self.vboxLayout.addWidget(lineEdit)
        self.node.graphicsNode.height += 30
        self.contentLists.append(
            ('lineEdit', {
                'label': label,
                'value': lineEdit.text(),
                'tooltip': kwargs.get("tooltip", "")
            }))
        return lineEdit
    
    def addOutputLabel(self, text:str="Output Label", **kwargs):
        label = Label(text, **kwargs)
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.vboxLayout.addWidget(label)
        self.node.graphicsNode.height += 30
        self.contentLists.append(
            ('outputLabel', {
                'text': text,
                'tooltip': kwargs.get("tooltip", "")
            }))
        return label
    
    def addToggleButton(self, icon:QIcon=None, text:str="", **kwargs):
        button = ToggleButton(icon=icon, text=text, **kwargs)
        self.vboxLayout.addWidget(button)
        self.node.graphicsNode.height += 30
        self.contentLists.append(
            ('pushButton', {
                'icon': icon,
                'text': text,
                'tooltip': kwargs.get("tooltip", "")
            }))
        return button

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
            elif content_type == 'inputLabel': 
                obj = self.addInputLabel(
                    content_data['text'], 
                    tooltip=content_data['tooltip'])
            elif content_type == 'lineEdit': 
                obj = self.addLineEdit(
                    content_data['label'], 
                    tooltip=content_data['tooltip'])
                obj.setText(content_data['value'])
            elif content_type == 'outputLabel': 
                obj = self.addOutputLabel(
                    content_data['text'], 
                    tooltip=content_data['tooltip'])
            else: print("\033[93m Wrong type: \033[0m", content_type)
        return True