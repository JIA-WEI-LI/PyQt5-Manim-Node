from typing import Union
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
        self.vboxLayout.setContentsMargins(0, 0, 3, 0)
        self.setLayout(self.vboxLayout)
    
    def addCheckbox(self, text:str, status:bool=False, **kwargs):
        """ Adds a custom checkbox to the layout.

            Parameters :
            ---------
                text ( str ) : The text displayed on the right side of the checkbox.

            Returns :
            ---------
                CheckBox: The created checkbox widget.

            Usage :
            ---------
                checkbox = self.content.addCheckbox(text="Checkbox")
        """
        checkbox = CheckBox(text, status=status, **kwargs)
        self.vboxLayout.addWidget(checkbox)
        self.node.graphicsNode.height += 30
        self.contentLists.append(
            ('checkbox', {
                'text': text,
                'status': status,
                'tooltip': kwargs.get("tooltip", "")
            }))
        return checkbox
    
    def addColorPickerButton(self, show_text:bool=False, **kwargs):
        """ Adds a custom colorpicker button to the layout.

            Returns :
            ---------
                colorPickerButton: The created colorPickerButton widget.

            Usage :
            ---------
                color_picker_button = self.content.addColorPickerButton()
        """
        colorPickerButton = ColorPickerButton(show_text=show_text, **kwargs)
        self.vboxLayout.addWidget(colorPickerButton)
        self.node.graphicsNode.height += 30
        # TODO:新增預設顏色序列化儲存 / 新增調整後顏色再次開啟之預設顏色
        self.contentLists.append(
            ('colorPickerButton', {
                'show_text': show_text,
                'selected_color_name': colorPickerButton.selected_color_name,
                'tooltip': kwargs.get("tooltip", "")
            }))
        return colorPickerButton
    
    def addComboBox(self, items:list=["List 1", "List 2", "List 3"], **kwargs):
        """Adds a custom combobox to the layout.

            Parameters :
            ---------
                items ( List[str] ) : A list of items to populate the combobox.

            Returns :
            ---------
                comboBox: The created comboBox widget.

            Usage :
            ---------
                combo_box = self.content.addComboBox(items=["List 1", "List 2", "List 3"], parent)
        """
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
    
    def addInputLabel(self, text:str="Input Label", **kwargs):
        """Adds a input label to the left side of layout.

            Parameters :
            ---------
                text ( str ) : The text displayed on the label.

            Returns :
            ---------
                label: The created Label widget.

            Usage :
            ---------
                input_label = self.content.addInputLabel(text="Input Label")
        """
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
        """Adds a LineEdit to the layout.

            Parameters :
            ---------
                label ( str ) : The label text of the QLineEdit widget.

            Returns :
            ---------
                lineEdit: The created lineEdit widget.

            Usage :
            ---------
                line_edit = self.content.addLineEdit(label="")
        """
        lineEdit = LineEdit(label, **kwargs)
        self.vboxLayout.addWidget(lineEdit)
        self.node.graphicsNode.height += 30
        self.contentLists.append(
            ('lineEdit', {
                'label': label,
                'current_text': "",
                'tooltip': kwargs.get("tooltip", "")
            }))
        return lineEdit
    
    def addProgressBar(self, label:str="Value", minimum:int=0, maximum:int=100, initial_value:Union[float, int]=0.5, **kwargs):
        """Adds a ProgressBar to the layout.

            Parameters :
            ---------
                label (str): The label text of the ProgressBar widget.
                minimum (int): The minimum value of the ProgressBar. Default is 0.
                maximum (int): The maximum value of the ProgressBar. Default is 100.
                initial_value (Union[float, int]): The initial value of the ProgressBar. Default is 0.5.

            Returns :
            ---------
                progressBar: The created progressBar widget.

            Usage :
            ---------
                progress_bar = self.content.addProgressBar(label="", minimum=0, maximum=10, initial_value=0.5)
        """
        progressBar = ControlledProgressBar(label=label, minimum=minimum, maximum=maximum, initial_value=initial_value, **kwargs)
        self.vboxLayout.addWidget(progressBar)
        self.node.graphicsNode.height += 30
        current_value = progressBar.value()
        self.contentLists.append(
            ('progressBar', {
                'label': label,
                'minium': minimum,
                'maxium': maximum,
                'initial_value': current_value,
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
        """Adds a SpinBox to the layout.

            Parameters :
            ---------
                label (str): The label text of the SpinBox widget.
                minimum (int): The minimum value of the SpinBox. Default is 0.
                maximum (int): The maximum value of the SpinBox. Default is 1000000.
                initial_value (int): The initial value of the SpinBox. Default is 1.

            Returns :
            ---------
                spinBox: The created spinBox widget.

            Usage :
            ---------
                spin_box = self.content.addSpinBox(label="SpinBox", minimum=0, maximum=1000000, initial_value=1)
        """
        spinBox = SpinBox(label=label, minimum=minimum, maximum=maximum, **kwargs)
        self.vboxLayout.addWidget(spinBox)
        self.node.graphicsNode.height += 30
        self.contentLists.append(
            ('spinBox', {
                'label': label,
                'minium': minimum,
                'maxium': maximum,
                'initial_value': initial_value,
                'tooltip': kwargs.get("tooltip", "")
            }))
        return spinBox
    
    def addOutputLabel(self, text:str="Output Label", **kwargs):
        """Adds a output label to the right side of layout.

            Parameters :
            ---------
                text ( str ) : The text displayed on the label.

            Returns :
            ---------
                label: The created Label widget.

            Usage :
            ---------
                output_label = self.content.addOutputLabel(text="Output Label")
        """
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
                    status=content_data['status'],
                    tooltip=content_data['tooltip'])
            elif content_type == 'colorPickerButton':
                obj = self.addColorPickerButton(
                    selected_color_name=content_data['selected_color_name'],
                    show_text=content_data['show_text'],
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
                    content_data['label'], 
                    tooltip=content_data['tooltip'])
            elif content_type == 'progressBar': 
                obj = self.addProgressBar(
                    content_data['label'], 
                    content_data['minium'],
                    content_data['maxium'], 
                    initial_value=content_data['initial_value'], 
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
                    initial_value=content_data['initial_value'],
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