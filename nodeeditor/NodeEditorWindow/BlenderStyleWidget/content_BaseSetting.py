from common.color_sheet import color_manager
from common.style_sheet import StyleSheet

class ContentBaseSetting:
    def __init__(self, apply_style=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color_BACKGROUND_WINDOW = color_manager.get_color("BLENDERCOLOR", "BACKGROUND_WINDOW")
        self.color_GRAY_24 = color_manager.get_color("BLENDERCOLOR", "GRAY_24")
        self.color_GRAY_2a = color_manager.get_color("BLENDERCOLOR", "GRAY_2a")
        self.color_GRAY_30 = color_manager.get_color("BLENDERCOLOR", "GRAY_30")
        self.color_GRAY_46 = color_manager.get_color("BLENDERCOLOR", "GRAY_46")
        self.color_GRAY_54 = color_manager.get_color("BLENDERCOLOR", "GRAY_54")
        self.color_GRAY_65 = color_manager.get_color("BLENDERCOLOR", "GRAY_65")
        self.color_clicked = color_manager.get_color("BLENDERCOLOR", "CLICKED")
        self.color_mouseover = color_manager.get_color("BLENDERCOLOR", "HOVER")

        self.content_height = kwargs.get("content_height", 24)

        # if apply_style: StyleSheet.applyStyle("node_content", self)