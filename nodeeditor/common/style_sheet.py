from enum import Enum
from PyQt5.QtWidgets import QWidget

class StyleSheet:
    """ Style sheet  """
    # 定義不同的樣式類型
    NODE_COMBOBOX = "node_comboBox"
    NODE_CONTENT = "node_content"
    EDITOR_WINDOW = "editor_window"

    @staticmethod
    def path(style_type):
        if style_type not in [StyleSheet.NODE_COMBOBOX, StyleSheet.NODE_CONTENT, StyleSheet.EDITOR_WINDOW]:
            return style_type  # 使用自定義路徑
        else:
            return f"nodeeditor\\resources\\qss\\{style_type}.qss"
    
    @staticmethod
    def apply(style_type):
        def decorator(func):
            def wrapper(*args, **kwargs):
                widget = args[0] if args else None
                if widget:
                    qss_file = StyleSheet().path(style_type)
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
    
    def applyStyle(style_type, widget):
        qss_file = StyleSheet().path(style_type) 
        try:
            with open(qss_file, 'r') as f:
                widget.setStyleSheet(f.read())
        except FileNotFoundError:
            print("\033[95m Error: QSS file not found at \033[0m", f"{qss_file}")
        except Exception as e:
            print("\033[93m Error applying QSS:\033[0m", f"{e}")