from common.color_sheet import color_manager

class ContentBaseSetting:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color_background = color_manager.get_color("BLENDERCOLOR", "GRAY_54")
        self.color_clicked = color_manager.get_color("BLENDERCOLOR", "CLICKED")
        self.color_lightgray = color_manager.get_color("BLENDERCOLOR", "GRAY_46")
        self.color_gray_light = color_manager.get_color("BLENDERCOLOR", "GRAY_2a")
        self.color_GRAY_65 = color_manager.get_color("BLENDERCOLOR", "GRAY_65")
        self.color_mouseover = color_manager.get_color("BLENDERCOLOR", "GRAY_MOUSEOVER")