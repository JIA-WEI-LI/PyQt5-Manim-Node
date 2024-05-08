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
        ''' 新增自定義勾選框
            ### Parameters:
                parent (QWidget): 父窗口部件，預設為None。
                text (str): 顯示勾選框右側文字內容。
                **tooltip (str): 自定義提示字框內容文字。

            ### Attributes:
                text (str): 顯示勾選框右側文字內容。

            ### Usage:
                self.content.addCheckBox(text="CheckBox")
        '''
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
    
    @StyleSheet.apply(StyleSheet.NODE_CONTENT)
    def addComboBox(self, items:list=["List 1", "List 2", "List 3"], **kwargs):
        ''' 新增自定義下拉式選單
            ### Parameters:
                parent (QWidget): 父窗口部件，預設為None。
                **tooltip (str): 自定義提示字框內容文字。

            ### Attributes:
                text_label (QLabel): 顯示當前選擇文本的標籤。

            ### Usage:
                self.content.addComboBox = ComboBox(["a", "b", "c"])
        '''
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
    
    @StyleSheet.apply(StyleSheet.NODE_CONTENT)
    def addInputLabel(self, text:str, **kwargs):
        ''' 新增自定義文字
            ### Parameters:
                parent (QWidget): 父窗口部件，預設為None。
                text (str): 顯示文字內容。
                **tooltip (str): 自定義提示字框內容文字。

            ### Attributes:
                text (str): 顯示文字內容。

            ### Usage:
                self.content.addLabel(text="mylabel")
        '''
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
    
    @StyleSheet.apply(StyleSheet.NODE_CONTENT)
    def addLineEdit(self, text:str, **kwargs):
        ''' 新增自定義單行文件輸入
            ### Parameters:
                text (str): QLineEdit部件的標籤文字。
                max_width (float): QLineEdit部件的最大寬度。
                **tooltip (str): 自定義提示字框內容文字。

            ### Attributes:
                text (str): QLineEdit部件的標籤文字。
                max_width (float): QLineEdit部件的最大寬度。

            ### Usage:
                self.content.addLineEdit(text="MyLineEdit", max_width=100)
        '''
        lineEdit = LineEdit(text, self.width(), **kwargs)
        self.vboxLayout.addWidget(lineEdit)
        self.node.graphicsNode.height += 30
        self.contentLists.append(
            ('lineEdit', {
                'text': text,
                'max_width': self.width(),
                'tooltip': kwargs.get("tooltip", "")
            }))
        return lineEdit
    
    @StyleSheet.apply(StyleSheet.NODE_CONTENT)
    def addProgressBar(self, label:str="Value", minimum:int=0, maximum:int=10, **kwargs):
        '''新增自定義進度條
            ### Parameters:
                label (str): 進度條的標籤，預設為"Value"。
                minimum (int): 進度條的最小值，預設為0。
                maximum (int): 進度條的最大值，預設為100。
                **initial_percent (float): 進度條的初始百分比，預設為0.5。
                **tooltip (str): 自定義提示字框內容文字。

            ### Attributes:
                label (str): 進度條的標籤。
                minimum (int): 進度條的最小值。
                maximum (int): 進度條的最大值。

            ### Raises:
                ValueError: 若initial_percent不在0~1的範圍內時，會引發此錯誤。

            ### Usage:
                progressBar = ControlledProgressBar(label="Progress", minimum=0, maximum=10, initial_percent=0.8)
        '''
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
    
    @StyleSheet.apply(StyleSheet.NODE_CONTENT)
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

    @StyleSheet.apply(StyleSheet.NODE_CONTENT)
    def addSpinBox(self, label:str="Value", minimum:int=0, maximum:int=100000, **kwargs):
        ''' 新增自定義 SpinBox
            ### Parameters:
                label (str): SpinBox的標籤，預設為"Value"。
                minimum (int): SpinBox的最小值，預設為0。
                maximum (int): SpinBox的最大值，預設為100。
                **initial_percent (float): SpinBox的初始百分比，預設為0.5。
                **tooltip (str): 自定義提示字框內容文字。

            ### Attributes:
                label (str): SpinBox的標籤。
                minimum (int): SpinBox的最小值。
                maximum (int): SpinBox的最大值。

            ### Raises:
                ValueError: 若initial_percent不在0~1的範圍內時，會引發此錯誤。

            ### Usage:
                self.content.addSpinBox(label="Value", minimum=0, maximum=10, initial_percent=0.8)
        '''
        spinBox = SpinBox(label=label, minimum=minimum, maximum=maximum, **kwargs)
        self.vboxLayout.addWidget(spinBox)
        self.node.graphicsNode.height += 30
        self.contentLists.append(
            ('spinBox', {
                'label': label,
                'minium': minimum,
                'maxium': maximum,
                'value': 1,
                'tooltip': kwargs.get("tooltip", "")
            }))
        return spinBox
    
    @StyleSheet.apply(StyleSheet.NODE_CONTENT)
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
    
    @StyleSheet.apply(StyleSheet.NODE_CONTENT)
    def addVectorSpinBox(self, degree:list=["x", "y", "z"], **kwargs):
        '''新增向量型數值框'''
        vector = VectorSpinBox(degree=degree, **kwargs)
        vector.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.vboxLayout.addWidget(vector)
        self.node.graphicsNode.height += len(degree)*30
        self.contentLists.append(
            ('outputLabel', {
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
                    content_data['max_width'],
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
            elif content_type == 'outputLabel': 
                obj = self.addOutputLabel(
                    content_data['text'], 
                    tooltip=content_data['tooltip'])
            else: print("\033[93m Wrong type: \033[0m", content_type)
        return True