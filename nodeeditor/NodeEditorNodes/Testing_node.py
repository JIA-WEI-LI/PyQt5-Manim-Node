from NodeEditorWindow import *

class Node_Test(Node):
    def __init__(self, scene, title="測試用節點", input=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], output=[1]):
        super().__init__(scene, title, input, output)

        self.node_type(4)
        self.content.addOutputLabel("Output Label", tooltip="Output Label Tooltip")

        self.content.addCheckbox("Boolean", tooltip="CheckBox Tooltip")
        self.content.addColorPickerButton(show_text=True, tooltip="ColorPickerButton Tooltip")
        self.content.addComboBox(["List 1", "List 2", "List 3"], tooltip="ComboBox Tooltip")
        self.content.addInputLabel("Input Label", tooltip="Input Label Tooltip")
        self.content.addLineEdit("LineEdit", tooltip="LineEdit Tooltip")
        self.content.addProgressBar("ProgressBar", minimum=0, maximum=100, initial_value=20, tooltip="ProgressBar Tooltip")
        self.content.addPushButton("PushButton", tooltip="PushButton Tooltip")
        self.content.addSpinBox("SpinBox", minimum=0, maximum=1000, initial_value=20, tooltip="SpinBox Tooltip")
        self.content.addVectorSpinBox(["Vector 1", "Vector 2", "Vector 3"])