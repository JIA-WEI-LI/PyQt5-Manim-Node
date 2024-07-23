from typing import Union
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QRadioButton
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtCore import QSize, QRectF

from common.font import setFont
from common.style_sheet import BlenderStyleSheet
from common.icon import FluentIconBase, toQIcon, drawIcon
from common.overload import singledispatchmethod
from .content_BaseSetting import ContentBaseSetting

class PushButton(QPushButton, ContentBaseSetting):
    """ Push button

    Constructors
    ------------
    * PushButton(`parent`: QWidget = None)
    * PushButton(`text`: str, `parent`: QWidget = None, `icon`: QIcon | str | FluentIconBase = None)
    * PushButton(`icon`: QIcon | FluentIcon, `text`: str, `parent`: QWidget = None)
    """

    @singledispatchmethod
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.BaseSetting()
        BlenderStyleSheet.BUTTON.apply(self)
        self.isPressed = False
        self.isHover = False
        self.setIconSize(QSize(12, 12))
        self.setIcon(None)
        setFont(self)
        self._postInit()

    @__init__.register
    def _(self, text: str, parent: QWidget = None, icon: Union[QIcon, str, FluentIconBase] = None):
        self.__init__(parent=parent)
        self.setText(text)
        self.setIcon(icon)

    @__init__.register
    def _(self, icon: QIcon, text: str, parent: QWidget = None):
        self.__init__(text, parent, icon)

    @__init__.register
    def _(self, icon: FluentIconBase, text: str, parent: QWidget = None):
        self.__init__(text, parent, icon)

    def _postInit(self):
        pass

    def setIcon(self, icon: Union[QIcon, str, FluentIconBase]):
        self.setProperty('hasIcon', icon is not None)
        self.setStyle(QApplication.style())
        self._icon = icon or QIcon()
        self.update()

    def icon(self):
        return toQIcon(self._icon)

    def setProperty(self, name: str, value) -> bool:
        if name != 'icon':
            return super().setProperty(name, value)

        self.setIcon(value)
        return True

    def mousePressEvent(self, e):
        self.isPressed = True
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self.isPressed = False
        super().mouseReleaseEvent(e)

    def enterEvent(self, e):
        self.isHover = True
        self.update()

    def leaveEvent(self, e):
        self.isHover = False
        self.update()

    def _drawIcon(self, icon, painter, rect, state=QIcon.Off):
        """ draw icon """
        drawIcon(icon, painter, rect, state)

    def paintEvent(self, e):
        super().paintEvent(e)
        if self.icon().isNull():
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)

        if not self.isEnabled():
            painter.setOpacity(0.3628)
        elif self.isPressed:
            painter.setOpacity(0.786)

        w, h = self.iconSize().width(), self.iconSize().height()
        y = (self.height() - h) / 2
        mw = self.minimumSizeHint().width()
        if mw > 0:
            x = 12 + (self.width() - mw) // 2
        else:
            x = 12

        if self.isRightToLeft():
            x = self.width() - w - x
            
        self._drawIcon(self._icon, painter, QRectF(x, y, w, h))

class ToggleButton(PushButton):
    """ Toggle push button

    Constructors
    ------------
    * ToggleButton(`parent`: QWidget = None)
    * ToggleButton(`text`: str, `parent`: QWidget = None, `icon`: QIcon | str | FluentIconBase = None)
    * ToggleButton(`icon`: QIcon | FluentIcon, `text`: str, `parent`: QWidget = None)
    """

    def _postInit(self):
        self.setCheckable(True)
        self.setChecked(False)

    def _drawIcon(self, icon, painter, rect):
        if not self.isChecked():
            return PushButton._drawIcon(self, icon, painter, rect)

        PushButton._drawIcon(self, icon, painter, rect, QIcon.On)

TogglePushButton = ToggleButton