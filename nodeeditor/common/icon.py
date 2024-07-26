# coding:utf-8
from enum import Enum
from typing import Union

from PyQt5.QtXml import QDomDocument
from PyQt5.QtCore import QRectF, Qt, QFile, QObject, QRect
from PyQt5.QtGui import QIcon, QIconEngine, QColor, QPixmap, QImage, QPainter
from PyQt5.QtWidgets import QAction, qApp
from PyQt5.QtSvg import QSvgRenderer

from .overload import singledispatchmethod

class FluentIconEngine(QIconEngine):
    """ Fluent icon engine """

    def __init__(self, icon, reverse=False):
        """
        Parameters
        ----------
        icon: QICon | Icon | FluentIconBase
            the icon to be drawn

        reverse: bool
            whether to reverse the theme of icon
        """
        super().__init__()
        self.icon = icon
        self.isThemeReversed = reverse

    def paint(self, painter, rect, mode, state):
        painter.save()

        if mode == QIcon.Disabled:
            painter.setOpacity(0.5)
        elif mode == QIcon.Selected:
            painter.setOpacity(0.7)

        icon = self.icon

        if isinstance(self.icon, Icon):
            icon = self.icon.fluentIcon.icon()
        elif isinstance(self.icon, FluentIconBase):
            icon = self.icon.icon()

        if rect.x() == 19:
            rect = rect.adjusted(-1, 0, 0, 0)

        icon.paint(painter, rect, Qt.AlignCenter, QIcon.Normal, state)
        painter.restore()


class SvgIconEngine(QIconEngine):
    """ Svg icon engine """

    def __init__(self, svg: str, color: QColor = QColor("black")):
        super().__init__()
        self.svg = svg
        self.color = color

    def paint(self, painter, rect, mode, state):
        if mode == QIcon.Disabled:
            self.color = QColor("gray")
        elif mode == QIcon.Selected:
            self.color = QColor("blue")
        else:
            self.color = QColor("black")
        drawSvgIcon(self.svg.encode(), painter, rect, self.color)

    def clone(self) -> QIconEngine:
        return SvgIconEngine(self.svg, self.color)

    def pixmap(self, size, mode, state):
        image = QImage(size, QImage.Format_ARGB32)
        image.fill(Qt.transparent)
        pixmap = QPixmap.fromImage(image, Qt.NoFormatConversion)

        painter = QPainter(pixmap)
        rect = QRect(0, 0, size.width(), size.height())
        self.paint(painter, rect, mode, state)
        return pixmap

def drawSvgIcon(icon, painter, rect, color):
    renderer = QSvgRenderer(icon)
    painter.setBrush(QColor(color))
    renderer.render(painter, QRectF(rect))



def getIconColor(reverse=False):
    """ get the color of icon based on theme """
    return "white" if not reverse else "black"

def drawSvgIcon(icon, painter, rect):
    renderer = QSvgRenderer(icon)
    renderer.render(painter, QRectF(rect))


def writeSvg(iconPath: str, indexes=None, **attributes):
    if not iconPath.lower().endswith('.svg'):
        return ""

    f = QFile(iconPath)
    f.open(QFile.ReadOnly)

    dom = QDomDocument()
    dom.setContent(f.readAll())

    f.close()

    # change the color of each path
    pathNodes = dom.elementsByTagName('path')
    indexes = range(pathNodes.length()) if not indexes else indexes
    for i in indexes:
        element = pathNodes.at(i).toElement()

        for k, v in attributes.items():
            element.setAttribute(k, v)

    return dom.toString()


def drawIcon(icon, painter, rect, state=QIcon.Off, **attributes):
    if isinstance(icon, FluentIconBase):
        icon.render(painter, rect, **attributes)
    elif isinstance(icon, Icon):
        icon.fluentIcon.render(painter, rect, **attributes)
    else:
        icon = QIcon(icon)
        icon.paint(painter, QRectF(rect).toRect(), Qt.AlignCenter, state=state)


class FluentIconBase:
    """ Fluent icon base class """

    def path(self) -> str:
        raise NotImplementedError

    def icon(self, color: QColor = QColor("black")) -> QIcon:
        path = self.path()

        if not path.endswith('.svg'):
            return QIcon(self.path())

        return QIcon(SvgIconEngine(writeSvg(path, fill=color.name()), color))

    def qicon(self, reverse=False) -> QIcon:
        """ convert to QIcon, the theme of icon will be updated synchronously with app

        Parameters
        ----------
        reverse: bool
            whether to reverse the theme of icon
        """
        return QIcon(FluentIconEngine(self, reverse))

    def render(self, painter, rect, indexes=None, **attributes):
        icon = self.path()

        if icon.endswith('.svg'):
            if attributes:
                icon = writeSvg(icon, indexes, **attributes).encode()

            drawSvgIcon(icon, painter, rect)
        else:
            icon = QIcon(icon)
            rect = QRectF(rect).toRect()
            painter.drawPixmap(rect, icon.pixmap(QRectF(rect).toRect().size()))


class FluentIcon(FluentIconBase, Enum):
    """ Fluent icon """

    ADD = "Add"
    CUT = "Cut"
    IOT = "IOT"
    COPY = "Copy"
    HELP = "Help"
    PLAY = "Play"
    SAVE = "Save"
    CLOSE = "Close"
    PASTE = "Paste"
    FOLDER = "Folder"
    SAVE_AS = "SaveAs"
    DELETE = "Deleted"
    DOCUMENT = "Document"
    BACK_TO_WINDOW = "BackToWindow"

    def path(self):
        return f'nodeeditor/resources/icons/{self.value}_{getIconColor()}.svg'


class Icon(QIcon):

    def __init__(self, fluentIcon: FluentIcon):
        super().__init__(fluentIcon.path())
        self.fluentIcon = fluentIcon


def toQIcon(icon: Union[QIcon, FluentIconBase, str]) -> QIcon:
    """ convet `icon` to `QIcon` """
    if isinstance(icon, str):
        return QIcon(icon)

    if isinstance(icon, FluentIconBase):
        return icon.icon()

    return icon


class Action(QAction):
    """ Fluent action

    Constructors
    ------------
    * Action(`parent`: QWidget = None, `**kwargs`)
    * Action(`text`: str, `parent`: QWidget = None, `**kwargs`)
    * Action(`icon`: QIcon | FluentIconBase, `parent`: QWidget = None, `**kwargs`)
    """

    @singledispatchmethod
    def __init__(self, parent: QObject = None, **kwargs):
        super().__init__(parent, **kwargs)
        self.fluentIcon = None

    @__init__.register
    def _(self, text: str, parent: QObject = None, **kwargs):
        super().__init__(text, parent, **kwargs)
        self.fluentIcon = None

    @__init__.register
    def _(self, icon: QIcon, text: str, parent: QObject = None, **kwargs):
        super().__init__(icon, text, parent, **kwargs)
        self.fluentIcon = None

    @__init__.register
    def _(self, icon: FluentIconBase, text: str, parent: QObject = None, **kwargs):
        super().__init__(icon.icon(), text, parent, **kwargs)
        self.fluentIcon = icon

    def icon(self) -> QIcon:
        if self.fluentIcon:
            return Icon(self.fluentIcon)

        return super().icon()

    def setIcon(self, icon: Union[FluentIconBase, QIcon]):
        if isinstance(icon, FluentIconBase):
            self.fluentIcon = icon
            icon = icon.icon()

        super().setIcon(icon)
