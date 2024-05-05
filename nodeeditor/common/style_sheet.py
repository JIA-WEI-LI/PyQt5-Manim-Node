from enum import Enum
from PyQt5.QtWidgets import QWidget

class Theme(Enum):
    LIGHT = "Light"
    DARK = "Dark"
    AUTO = "Auto"

class StyleSheet:
    """ Style sheet  """
    # 定義不同的樣式類型
    NODE_COMBOBOX = "node_comboBox"
    NODE_CONTENT = "node_content"
    EDITOR_WINDOW = "editor_window"

    @staticmethod
    def path(style_type, theme=Theme.DARK):
        theme = theme if theme == Theme.DARK else theme
        if style_type not in [StyleSheet.NODE_COMBOBOX, StyleSheet.NODE_CONTENT, StyleSheet.EDITOR_WINDOW]:
            return style_type  # 使用自定義路徑
        else:
            return f"nodeeditor\\resources\\qss\\{theme.value.lower()}\\{style_type}.qss"
    
    @staticmethod
    def apply(style_type, theme=None):
        def decorator(func):
            def wrapper(*args, **kwargs):
                widget = args[0] if args else None
                if widget:
                    nonlocal theme
                    theme = theme if theme is not None else Theme.DARK
                    qss_file = StyleSheet().path(style_type, theme)
                    try:
                        with open(qss_file, 'r') as f:
                            widget.setStyleSheet(f.read())
                    except FileNotFoundError:
                        print("\033[95m Error: QSS file not found at \033[0m", f"{qss_file}")
                    except Exception as e:
                        print("\033[93m Error applying QSS:\033[0m", f"{e}")
                return func(*args, **kwargs)
            return wrapper
        return decorator

