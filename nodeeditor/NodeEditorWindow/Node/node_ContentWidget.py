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
    
    def addCheckbox(self, text:str, **kwargs):
        '''新增二態複選框'''
        checkbox = CheckBox(text, debug=DEBUG, **kwargs)
        self.vboxLayout.addWidget(checkbox)
        self.node.graphicsNode.height += 30
        self.contentLists.append(
            ('checkbox', {
                'text': text,
                'status': False,
                'tooltip': kwargs.get("tooltip", "")
            }))
        return checkbox
    
    def addColorPickerButton(self, **kwargs):
        '''新增顏色選擇按鈕'''
        colorPickerButton = ColorPickerButton(**kwargs)
        self.vboxLayout.addWidget(colorPickerButton)
        self.node.graphicsNode.height += 30
        # TODO:新增預設顏色序列化儲存 / 新增調整後顏色再次開啟之預設顏色
        self.contentLists.append(
            ('colorPickerButton', {
                'tooltip': kwargs.get("tooltip", "")
            }))
        return colorPickerButton
    
    def addComboBox(self, items:list=["List 1", "List 2", "List 3"], **kwargs):
        '''新增下拉式選單'''
        comboBox = ComboBox(**kwargs)
        comboBox.addItems(items)
        self.vboxLayout.addWidget(comboBox)
        self.node.graphicsNode.height += 30
        self.contentLists.append(
            ('comboBox', {
                'list': items,
                'tooltip': kwargs.get("tooltip", "")
            }))
        return comboBox
    
    def addInputLabel(self, text:str, **kwargs):
        '''新增輸入文字標籤'''
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
    
    def addLineEdit(self, text:str, **kwargs):
        '''新增單行文字輸入框'''
        lineEdit = LineEdit(text, self.width(), **kwargs)
        self.vboxLayout.addWidget(lineEdit)
        self.node.graphicsNode.height += 30
        self.contentLists.append(
            ('lineEdit', {
                'text': text,
                'current_text': "",
                'tooltip': kwargs.get("tooltip", "")
            }))
        return lineEdit
    
    def addProgressBar(self, label:str="Value", minimum:int=0, maximum:int=10, **kwargs):
        '''新增可控制進度條'''
        progressBar = ControlledProgressBar(label=label, minimum=minimum, maximum=maximum, **kwargs)
        self.vboxLayout.addWidget(progressBar)
        self.node.graphicsNode.height += 30
        self.contentLists.append(
            ('progressBar', {
                'label': label,
                'minium': minimum,
                'maxium': maximum,
                'value': 0.5,
                'tooltip': kwargs.get("tooltip", "")
            }))
        return progressBar
    
    def addPushButton(self, text:str, **kwargs):
        '''新增按紐'''
        button = PushButton(text, **kwargs)
        self.vboxLayout.addWidget(button)
        self.node.graphicsNode.height += 30
        self.contentLists.append(
            ('pushButton', {
                'text': text,
                'status': False,
                'tooltip': kwargs.get("tooltip", "")
            }))
        return button

    def addSpinBox(self, label:str="Value", minimum:int=0, maximum:int=100000, initial_value:int=1, **kwargs):
        '''新增可控制數值調整器'''
        spinBox = SpinBox(label=label, minimum=minimum, maximum=maximum, **kwargs)
        self.vboxLayout.addWidget(spinBox)
        self.node.graphicsNode.height += 30
        self.contentLists.append(
            ('spinBox', {
                'label': label,
                'minium': minimum,
                'maxium': maximum,
                'value': initial_value,
                'tooltip': kwargs.get("tooltip", "")
            }))
        return spinBox
    
    def addOutputLabel(self, text:str, **kwargs):
        '''新增輸出文字標籤'''
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
    
    def addVectorSpinBox(self, degree:list=["x", "y", "z"], **kwargs):
        '''新增向量型數值框'''
        vector = VectorSpinBox(degree=degree, **kwargs)
        vector.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.vboxLayout.addWidget(vector)
        self.node.graphicsNode.height += len(degree)*30
        self.contentLists.append(
            ('vectorSpinBox', {
                'degree': degree,
                'tooltip': kwargs.get("tooltip", "")
            }))
        return vector

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
            elif content_type == 'inputLabel': 
                obj = self.addInputLabel(
                    content_data['text'], 
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
            elif content_type == 'spinBox': 
                obj = self.addSpinBox(
                    content_data['label'],
                    content_data['minium'],
                    content_data['maxium'], 
                    initial_value=content_data['value'],
                    tooltip=content_data['tooltip'])
            elif content_type == 'outputLabel': 
                obj = self.addOutputLabel(
                    content_data['text'], 
                    tooltip=content_data['tooltip'])
            elif content_type == 'vectorSpinBox': 
                obj = self.addVectorSpinBox(
                    content_data['degree'],
                    tooltip=content_data['tooltip'])
            else: print("\033[93m Wrong type: \033[0m", content_type)
        return True