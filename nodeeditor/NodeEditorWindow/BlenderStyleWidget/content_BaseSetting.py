from common.style_sheet import StyleSheet

class ContentBaseSetting:
    def __init__(self, apply_style=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tooltip = kwargs.get("tooltip", "")
        self.debug = kwargs.get("debug", False)
        self.content_height = kwargs.get("content_height", 24)

    def styles_set(self):
        self.setToolTip(self.tooltip)
        StyleSheet.applyStyle("node_content", self)
        if self.debug: self.setStyleSheet("border: 1px solid red;")