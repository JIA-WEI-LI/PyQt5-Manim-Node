from PyQt5.QtGui import QIcon, QColor, QImage, QPainter, QPixmap
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import Qt, QByteArray
from io import BytesIO

class BlenderIcon:
    ICON_PATH = "nodeeditor/resources/icons/"
    WINDOW_LOGO = ICON_PATH + "logo.png"
    CLOSE = ICON_PATH + "icon_close.svg"
    CHECK = ICON_PATH + "icon_check.svg"
    DOCUMENT = ICON_PATH + "icon_document.svg"
    FOLDER = ICON_PATH + "icon_folder.svg"
    PLUS = ICON_PATH + "icon_plus.svg"
    POWER = ICON_PATH + "icon_power.svg"
    SAVE = ICON_PATH + "icon_save.svg"

    @staticmethod
    def color(icon_path, color: QColor = None) -> QIcon:
        """ Creates a QIcon with the specified color for SVG icons.

        Parameters
        ----------
        icon_path: str
            Path to the icon file.
        
        color: QColor | None
            Color to apply to the SVG icon. If None, no color change is applied.

        Returns
        -------
        QIcon
            The QIcon object with the specified color.
        """
        if icon_path.endswith('.svg') and color:
            # Load the SVG file
            renderer = QSvgRenderer(icon_path)
            # Create a QImage to draw the SVG onto
            image = QImage(renderer.defaultSize(), QImage.Format_ARGB32)
            image.fill(Qt.transparent)
            painter = QPainter(image)
            renderer.render(painter)
            painter.end()

            # Apply the color filter
            if color:
                color_image = QImage(image.size(), QImage.Format_ARGB32)
                color_image.fill(color)
                painter.begin(color_image)
                painter.setCompositionMode(QPainter.CompositionMode_SourceAtop)
                painter.drawImage(0, 0, image)
                painter.end()
                image = color_image

            # Convert the QImage to a QPixmap and then to a QIcon
            pixmap = QPixmap.fromImage(image)
            return QIcon(pixmap)
        
        return QIcon(icon_path)