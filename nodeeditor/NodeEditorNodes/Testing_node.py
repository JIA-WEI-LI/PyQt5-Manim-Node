from NodeEditorWindow import *

class Node_Test(Node):
    def __init__(self, scene, title="測試用節點", input=[1, 2, 3, 0 ,1], output=[1, 2, 3, 3, 4, 1]):
        super().__init__(scene, title, input, output)

        self.content.addOutputLabel("Output")
        self.content.addCheckbox("Check Box")
        self.content.addLineEdit("Line Edit", tooltip="New Tooltip")
        self.content.addLineEdit("", tooltip="New Tooltip")
        self.content.addProgressBar(tooltip="測試文件")
        self.content.addComboBox(["List 1", "List 1", "List 1"])
        self.content.addInputLabel("Test Label 1")
        self.content.addInputLabel("Test Label 2")
        self.content.addInputLabel("Test Label 3")
        self.content.addInputLabel("Test Label 2")
        self.content.addInputLabel("Test Label 3")