from NodeEditorWindow import *

class Node_Test(Node):
    def __init__(self, scene, title="測試用節點", input=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], output=[1]):
        super().__init__(scene, title, input, output)

        self.node_type(4)
        self.content.addOutputLabel("Output Label", tooltip="Output Label Tooltip")

        # self.content.addCheckbox("Boolean", tooltip="CheckBox Tooltip")
        self.content.addInputLabel("Input Label", tooltip="Input Label Tooltip")
        self.content.addLineEdit("LineEdit", tooltip="LineEdit Tooltip")