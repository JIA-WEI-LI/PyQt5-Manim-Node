import typing
from PyQt5.QtWidgets import QMessageBox

from common.style_sheet import StyleSheet

class MessageBox(QMessageBox):
    @staticmethod
    def warning(parent, title:str, text:str, buttons: typing.Union['QMessageBox.StandardButtons', 'QMessageBox.StandardButton'] , **kwargs) -> QMessageBox.StandardButton:
        save_button = None
        discard_button = None
        cancel_button = None
        save_text = kwargs.get("save_text", "Save")
        discard_text = kwargs.get("discard_text", "Discard")
        cancel_text = kwargs.get("cancel_text", "Cancel")
        
        messageBox = QMessageBox(parent)
        messageBox.setWindowTitle(title)
        messageBox.setText(text)
        
        # 添加按鈕
        if buttons == QMessageBox.StandardButton.Save:
            save_button = messageBox.addButton(save_text, QMessageBox.ButtonRole.YesRole)
            discard_button = None
            cancel_button = None
        if buttons == QMessageBox.StandardButton.Discard:
            discard_button = messageBox.addButton(discard_text, QMessageBox.ButtonRole.NoRole)
            save_button = None
            cancel_button = None
        if buttons == QMessageBox.StandardButton.Cancel:
            cancel_button = messageBox.addButton(cancel_text, QMessageBox.ButtonRole.InvalidRole)
            save_button = None
            discard_button = None

        # 設置按鈕樣式
        for button in messageBox.buttons():
            button.setStyleSheet("background-color: #666; color: white;")

        clicked_button = messageBox.clickedButton()
        if clicked_button == save_text: return QMessageBox.StandardButton.Save
        elif clicked_button == discard_text: return QMessageBox.StandardButton.Discard
        elif clicked_button == cancel_text: return QMessageBox.StandardButton.Cancel
        else: return QMessageBox.StandardButton.NoButton