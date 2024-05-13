from PyQt5.QtWidgets import QPushButton, QSizePolicy, QDialog, QColorDialog, QLabel, QWidget, QSpinBox, QLineEdit

from .content_BaseSetting import ContentBaseSetting
from common.style_sheet import StyleSheet

class ColorPickerButton(QPushButton, ContentBaseSetting):
    """ Custom Color Picker Button
        
        Parameters:
        ---------
            text (str): The text displayed on the button. Default is empty.
            parent (QWidget): The parent widget. Default is None.

        Attributes:
        ---------
            text (str): The text displayed on the button.

        Usage:
        ---------
            color_picker = ColorPicker(text="Select Color")
    """
    def __init__(self, text: str="", parent=None, **kwargs):
        super().__init__(text, parent)
        tooltip = kwargs.get("tooltip", "")
        debug = kwargs.get("debug", False)

        self.setText(text)
        self.clicked.connect(self.pickColor)
        self.setFixedHeight(self.content_height)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setToolTip(text) if tooltip=="" else self.setToolTip(tooltip)
        StyleSheet.applyStyle("node_content", self)

        if debug: self.setStyleSheet("border: 1px solid red;")

    def pickColor(self):
        # 創建顏色選擇器對話框
        colorPickerDialog = ColorDialog()
        color = colorPickerDialog.exec_()
        
        if color == QDialog.Accepted:
            selected_color = colorPickerDialog.selectedColor()
            button_style = f"background-color: {selected_color.name()}; border-radius: 3px;"
            self.setStyleSheet(button_style)
            return selected_color
        return

class ColorDialog(QColorDialog):
    '''
    自定義的顏色選擇對話框
    '''
    def __init__(self, parent=None):
        super().__init__(parent)

    # @StyleSheet.apply(StyleSheet.NODE_CONTENT)
    def showEvent(self, event):
        super().showEvent(event)
        self.setStyleSheet("background-color: #222;")

        labels = self.findChildren(QLabel)
        for label in labels:
            label.setFixedHeight(23)
            label.setStyleSheet("background-color: transparent; color: white; font-family: Arial, Helvetica, sans-serif ;")


        buttons = self.findChildren(QPushButton)
        for button in buttons:
            button.setFixedHeight(23)
            button.setMinimumWidth(60)
            button.setStyleSheet("color: white; background-color: #545454; border-radius: 3px;")

            button_style = """
                QPushButton { color: white; background-color: #545454; border-radius: 3px; font-family: Arial, Helvetica, sans-serif ; }
                QPushButton:hover { background-color: #656565; }
                QPushButton:pressed { background-color: #222; }
            """
            button.setStyleSheet(button_style)

        spinBoxs = self.findChildren(QSpinBox)
        for spinBox in spinBoxs:
            spinBox.setFixedHeight(23)
            
            spinBox_style = """
                QSpinBox {
                    color: white; 
                    background-color:  #545454; 
                    border-radius: 3px;
                    qproperty-alignment: AlignCenter;
                    font-family: Arial, Helvetica, sans-serif ;
                }

                QSpinBox::up-button {
                    subcontrol-origin: none;
                    width: 0;
                    height: 0;
                }

                QSpinBox::up-button:hover { 
                    background-color: #656565; 
                }

                QSpinBox::down-button {
                    subcontrol-origin: none;
                    width: 0;
                    height: 0;
                }

                QSpinBox::down-button:hover { 
                    background-color: #656565; 
                }
            """
            spinBox.setStyleSheet(spinBox_style)

        lineEdits = self.findChildren(QLineEdit)
        for lineEdit in lineEdits:
            lineEdit.setFixedHeight(23)

            lineEdit_style = """
                QLineEdit { 
                    color: white; 
                    background-color:  #545454; 
                    border-radius: 3px;
                    font-family: Arial, Helvetica, sans-serif ; }
                QLineEdit:hover { background-color: #656565; }
            """
            lineEdit.setStyleSheet(lineEdit_style)

        self.printAllChildren(self, False)

    def printAllChildren(self, parent_widget, isPrint=True):
        if isPrint:
            for child_widget in parent_widget.findChildren(QWidget):
                print(child_widget.objectName(), child_widget.__class__.__name__)
                self.printAllChildren(child_widget)  # 遞迴列印子小部件