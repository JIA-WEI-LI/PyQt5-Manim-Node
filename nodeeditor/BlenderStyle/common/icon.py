from PyQt5.QtGui import QIcon

class BlenderStyleIcon:
    CHECK = "wblenderstylewidget/icons/icon_check.svg"
    CLOSE = "wblenderstylewidget/icons/icon_close.svg"
    LEFTARROWHEAD = "wblenderstylewidget/icons/icon_leftarrowhead.svg"
    RIGHTARROWHEAD = "wblenderstylewidget/icons/icon_rightarrowhead.svg"
    SEARCH = "wblenderstylewidget/icons/icon_search.svg"

    def __getattribute__(self, name):
        value = super(BlenderStyleIcon, self).__getattribute__(name)
        if name is not None:
            if isinstance(value, str):
                return QIcon(value)
            else:
                return value
        return value