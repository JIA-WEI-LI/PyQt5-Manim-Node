from PyQt5.QtGui import QColor

class WindowColor:
    DEFAULT_BACKGROUND = QColor("#393939")
    DEFAULT_PEN_LIGHT = QColor("#2f2f2f")
    DEFAULT_PEN_DARK = QColor("#292929")

    BLENDER_BACKGROUND = QColor("#1d1d1d") 
    BLENDER_PEN_LIGHT = QColor("#222")
    BLENDER_PEN_DARK = QColor("#2a2a2a")

class NodeColor:
    DEFAULT_TITLE = QColor('#fff')
    DEFAULT_PEN = QColor('#7F000000')
    DEFAULT_PEN_SELECTED = QColor('#FFFFA637')
    DEFAULT_BRUSH_TITLE = QColor('#FF313131')
    DEFAULT_BRUSH_BACKGROUND = QColor('#E3212121')

    BLENDER_TITLE = QColor('#fff')
    BLENDER_PEN = QColor('#7F000000')
    BLENDER_PEN_SELECTED = QColor('#FFFFFF')
    BLENDER_BRUSH_TITLE = QColor('#1d725e')
    BLENDER_BRUSH_BACKGROUND = QColor('#E3303030')
    BLENDER_TITLE_LIST = [
        QColor('#FF246283'),
        QColor('#FF79461d'),
        QColor('#FF344621'),
        QColor('#FF83314a'),
        QColor('#FF1d2546'),
        QColor('#FF1d1d1d'),
    ]

class SocketColor:
    DEFAULT_BACKGROUND = QColor('#FFFF7700')
    DEFAULT_OUTLINE = QColor('#FF000000')
    DEFAULT_COLOR_LIST = [
        QColor('#FFa1a1a1'),
        QColor('#FF00d6a3'),
        QColor('#FFc7c729'),
        QColor('#FF6363c7'),
        QColor('#FF598c5c'),
        QColor('#FFcca6d6'),
    ]

class EdgeColor:
    DEFAULT_PEN = QColor('#001000')
    DEFAULT_PEN_SELECTED = QColor('#00ff00')
    ORANGE = QColor('#FFFF7700')

    BLENDER_PEN_SELECTED = QColor('#b3f3e4')
    BLENDER_GREEN = QColor('#FF03bd91')