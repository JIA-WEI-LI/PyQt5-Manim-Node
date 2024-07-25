from typing import Union
from PyQt5.QtCore import Qt, QSize, QRectF, QTimer
from PyQt5.QtGui import QIcon, QPainter, QPainterPath
from PyQt5.QtWidgets import QLineEdit, QCompleter, QHBoxLayout, QToolButton

from common.font import setFont
from common.style_sheet import BlenderStyleSheet
from common.icon import FluentIconBase, FluentIcon, drawIcon
from common.overload import singledispatchmethod
from .content_BaseSetting import ContentBaseSetting

class LineEditButton(QToolButton):
    """ Line edit button """

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], parent=None):
        super().__init__(parent=parent)
        self._icon = icon
        self.isPressed = False
        # self.setFixedSize(31, 23)
        self.setIconSize(QSize(10, 10))
        self.setCursor(Qt.PointingHandCursor)
        self.setObjectName('lineEditButton')
        BlenderStyleSheet.LINEEDIT.apply(self)

    def mousePressEvent(self, e):
        self.isPressed = True
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self.isPressed = False
        super().mouseReleaseEvent(e)

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        iw, ih = self.iconSize().width(), self.iconSize().height()
        w, h = self.width(), self.height()
        rect = QRectF((w - iw)/2, (h - ih)/2, iw, ih)

        if self.isPressed:
            painter.setOpacity(0.7)

        drawIcon(self._icon, painter, rect, fill='#656565')

class LineEdit(QLineEdit, ContentBaseSetting):
    """ Line edit """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.BaseSetting()

        self._isClearButtonEnabled = False
        self._completer = None  # type: QCompleter
        self._completerMenu = None

        self.setProperty("transparent", True)
        BlenderStyleSheet.LINEEDIT.apply(self)
        # self.setFixedHeight(33)
        self.setAttribute(Qt.WA_MacShowFocusRect, False)
        setFont(self)

        self.hBoxLayout = QHBoxLayout(self)
        self.clearButton = LineEditButton(FluentIcon.CLOSE, self)

        self.clearButton.setFixedSize(12, 12)
        self.clearButton.hide()

        self.hBoxLayout.setSpacing(3)
        self.hBoxLayout.setContentsMargins(4, 4, 4, 4)
        self.hBoxLayout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.hBoxLayout.addWidget(self.clearButton, 0, Qt.AlignRight)

        self.clearButton.clicked.connect(self.clear)
        self.textChanged.connect(self.__onTextChanged)
        self.textEdited.connect(self.__onTextEdited)

    def setClearButtonEnabled(self, enable: bool):
        self._isClearButtonEnabled = enable
        self.setTextMargins(0, 0, 28*enable, 0)

    def isClearButtonEnabled(self) -> bool:
        return self._isClearButtonEnabled

    def setCompleter(self, completer: QCompleter):
        self._completer = completer

    def completer(self):
        return self._completer

    def focusOutEvent(self, e):
        super().focusOutEvent(e)
        self.clearButton.hide()

    def focusInEvent(self, e):
        super().focusInEvent(e)
        if self.isClearButtonEnabled():
            self.clearButton.setVisible(bool(self.text()))

    def __onTextChanged(self, text):
        """ text changed slot """
        if self.isClearButtonEnabled():
            self.clearButton.setVisible(bool(text) and self.hasFocus())

    def __onTextEdited(self, text):
        if not self.completer():
            return

        if self.text():
            QTimer.singleShot(50, self._showCompleterMenu)
        elif self._completerMenu:
            self._completerMenu.close()

    def setCompleterMenu(self, menu):
        """ set completer menu

        Parameters
        ----------
        menu: CompleterMenu
            completer menu
        """
        menu.activated.connect(self._completer.activated)
        self._completerMenu = menu

    def _showCompleterMenu(self):
        if not self.completer() or not self.text():
            return

        # create menu
        # if not self._completerMenu:
        #     self.setCompleterMenu(CompleterMenu(self))

        # add menu items
        self.completer().setCompletionPrefix(self.text())
        changed = self._completerMenu.setCompletion(self.completer().completionModel())
        self._completerMenu.setMaxVisibleItems(self.completer().maxVisibleItems())

        # show menu
        if changed:
            self._completerMenu.popup()

    # def contextMenuEvent(self, e):
    #     menu = LineEditMenu(self)
    #     menu.exec_(e.globalPos())

    def paintEvent(self, e):
        super().paintEvent(e)
        if not self.hasFocus():
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        m = self.contentsMargins()
        path = QPainterPath()
        w, h = self.width()-m.left()-m.right(), self.height()
        path.addRoundedRect(QRectF(m.left(), h-10, w, 10), 5, 5)

        rectPath = QPainterPath()
        rectPath.addRect(m.left(), h-10, w, 8)
        path = path.subtracted(rectPath)

        # painter.fillPath(path, themeColor())