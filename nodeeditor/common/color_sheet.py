import json
from PyQt5.QtGui import QColor

from config.file_path import COLOR_PALETTE_PATH

class ColorManager:
    '''獲取顏色列表'''
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ColorManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, file_path=COLOR_PALETTE_PATH):
        if not hasattr(self, 'file_path'):
            self.file_path = file_path
            self.colors_data = self.load_colors_from_json()

    def load_colors_from_json(self):
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def get_color(self, category, key, index=None):
        '''如果顏色訊息是列表且索引不為 None，則使用索引從列表中獲取顏色訊息， 否則直接將顏色訊息轉換為 QColor 對象'''
        color_info = self.colors_data.get(category, {}).get(key)
        if color_info:
            if isinstance(color_info, list) and index is not None:
                color_index = index % len(color_info)  # 確保索引在合法範圍內
                return QColor(color_info[color_index])
            else:
                return QColor(color_info)
        else:
            return None

    def get_color_list(self, category, key):
        '''如果顏色訊息是列表，則返回列表'''
        color_info = self.colors_data.get(category, {}).get(key)
        if isinstance(color_info, list):
            return color_info
        else:
            return None

# 創建單例對象，供其他模塊引用
color_manager = ColorManager()