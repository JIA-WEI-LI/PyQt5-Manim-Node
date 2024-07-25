from typing import Union
from collections import OrderedDict

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy

from ..Serialization.node_Serializable import Serializable
# from ..BlenderStyleWidget import *
from BlenderWidget import *
from common import *
from common.icon import FluentIconBase

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
    
    def addLineEdit(self, placeholder_text:str="", **kwargs):
        lineEdit = LineEdit(**kwargs)
        lineEdit.setPlaceholderText(placeholder_text)
        self.vboxLayout.addWidget(lineEdit)
        self.node.graphicsNode.height += 30
        self.contentLists.append(
            ('lineEdit', {
                'placeholder_text': placeholder_text,
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
    
    def addPushButton(self, icon:Union[QIcon, FluentIcon]=None, text:str="", **kwargs):
        button = PushButton(icon=icon, text=text, **kwargs)
        self.vboxLayout.addWidget(button)
        self.node.graphicsNode.height += 30
        self.contentLists.append(
            ('pushButton', {
                'icon': icon._name_,
                'text': text,
                'tooltip': kwargs.get("tooltip", "")
            }))
        return button
    
    def addToggleButton(self, icon:Union[QIcon, FluentIcon]=None, text:str="", **kwargs):
        button = ToggleButton(icon=icon, text=text, **kwargs)
        self.vboxLayout.addWidget(button)
        self.node.graphicsNode.height += 30
        self.contentLists.append(
            ('toggleButton', {
                'icon': icon._name_,
                'text': text,
                'tooltip': kwargs.get("tooltip", "")
            }))
        return button

    def setEditingFlag(self, value):
        self.node.scene.nodeGraphicsScene.views()[0].editingFlag = value

    def deserialize_icon(self, icon_name):
        try:
            return FluentIcon[icon_name]
        except KeyError:
            print(f"\033[91m Icon not found: {icon_name} \033[0m")
            return FluentIcon.CLOSE

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
                    content_data['text'])
            elif content_type == 'lineEdit': 
                obj = self.addLineEdit(
                    placeholder_text=content_data['placeholder_text'])
                obj.setText(content_data['value'])
            elif content_type == 'outputLabel': 
                obj = self.addOutputLabel(
                    content_data['text'])
            elif content_type == 'pushButton':
                obj = self.addPushButton(
                    icon = self.deserialize_icon(content_data['icon']),
                    text=content_data['text'])
            elif content_type == 'toggleButton':
                obj = self.addToggleButton(
                    icon = self.deserialize_icon(content_data['icon']),
                    text=content_data['text'])
            else: print("\033[93m Wrong type: \033[0m", content_type)
        return True