import json
from enum import Enum
from copy import deepcopy
from typing import List
from pathlib import Path
from PyQt5.QtGui import  QColor
from PyQt5.QtCore import QObject, pyqtSignal

from .exception_handler import exceptionHandler
    
class ConfigValidator:
    def validate(self, value):
        return True

    def correct(self, value):
        return value
    
class ConfigSerializer:
    def serialize(self, value):
        return value

    def deserialize(self, value):
        return value
    
class ConfigItem(QObject):
    """ Config item """
    valueChanged = pyqtSignal(object)

    def __init__(self, group, name, default, validator=None, serializer=None, restart=False):
        """
        Parameters
        ----------
        group: str
            config group name

        name: str
            config item name, can be empty

        default:
            default value

        options: list
            options value

        serializer: ConfigSerializer
            config serializer

        restart: bool
            whether to restart the application after updating value
        """
        super().__init__()
        self.group = group
        self.name = name
        self.validator = validator or ConfigValidator()
        self.serializer = serializer or ConfigSerializer()
        self.__value = default
        self.value = default
        self.restart = restart
        self.defaultValue = self.validator.correct(default)

    @property
    def value(self):
        """ get the value of config item """
        return self.__value

    @value.setter
    def value(self, v):
        v = self.validator.correct(v)
        ov = self.__value
        self.__value = v
        if ov != v:
            self.valueChanged.emit(v)

    @property
    def key(self):
        """ get the config key separated by `.` """
        return self.group+"."+self.name if self.name else self.group

    def __str__(self):
        return f'{self.__class__.__name__}[value={self.value}]'

    def serialize(self):
        return self.serializer.serialize(self.value)

    def deserializeFrom(self, value):
        self.value = self.serializer.deserialize(value)

class OptionsValidator(ConfigValidator):
    """ Options validator """
    def __init__(self, options):
        if not options:
            raise ValueError("The `options` can't be empty.")

        if isinstance(options, Enum):
            options = options._member_map_.values()

        self.options = list(options)

    def validate(self, value):
        return value in self.options

    def correct(self, value):
        return value if self.validate(value) else self.options[0]

class BoolValidator(OptionsValidator):
    """ Boolean validator """
    def __init__(self):
        super().__init__([True, False])

class FolderValidator(ConfigValidator):
    """ Folder validator """
    def validate(self, value):
        return Path(value).exists()

    def correct(self, value):
        path = Path(value)
        path.mkdir(exist_ok=True, parents=True)
        return str(path.absolute()).replace("\\", "/")
    
class FolderListValidator(ConfigValidator):
    """ Folder list validator """
    def validate(self, value):
        return all(Path(i).exists() for i in value)

    def correct(self, value: List[str]):
        folders = []
        for folder in value:
            path = Path(folder)
            if path.exists():
                folders.append(str(path.absolute()).replace("\\", "/"))

        return folders

class RangeConfigItem(ConfigItem):
    """ Config item of range """
    @property
    def range(self):
        """ get the available range of config """
        return self.validator.range

    def __str__(self):
        return f'{self.__class__.__name__}[range={self.range}, value={self.value}]'
    
class OptionsConfigItem(ConfigItem):
    """ Config item with options """
    @property
    def options(self):
        return self.validator.options

    def __str__(self):
        return f'{self.__class__.__name__}[options={self.options}, value={self.value}]'

class ColorConfigItem(ConfigItem):
    """ Config item for a single color """
    def __init__(self, group, name, default, validator=None, serializer=None, output_type="QColor", **kwargs):
        super().__init__(group, name, default, validator, serializer, **kwargs)
        self.output_type = output_type

    @property
    def color(self):
        if self.output_type == "QColor":
            return QColor(self.value)
        return self.value

    @color.setter
    def color(self, value):
        if self.output_type == "QColor":
            self.value = value.name()  # Store the color as a string in HEX format
        else:
            self.value = value

    def __str__(self):
        return f'{self.__class__.__name__}[color={self.color}, value={self.value}]'
    
class QConfig(QObject):
    def __init__(self):
        super().__init__()
        self.file = Path("nodeeditor\\config\\config.json")
        self._cfg = self

    def get(self, item):
        if isinstance(item, ColorConfigItem):
            return item.color
        return item.value
    
    def set(self, item, value, save=True, copy=True):
        if item.value == value:
            return
        try:
            item.value = deepcopy(value) if copy else value
        except:
            item.value = value
        if save:
            self.save()
        if item.restart:
            self._cfg.appRestartSig.emit()
        
    def save(self):
        """ save config """
        self._cfg.file.parent.mkdir(parents=True, exist_ok=True)
        with open(self._cfg.file, "w", encoding="utf-8") as f:
            json.dump(self._cfg.toDict(), f, ensure_ascii=False, indent=4)

    @exceptionHandler()
    def load(self, file=None, config=None):
        """ load config

        Parameters
        ----------
        file: str or Path
            the path of json config file

        config: Config
            config object to be initialized
        """
        if isinstance(config, QConfig):
            self._cfg = config
            self._cfg.themeChanged.connect(self.themeChanged)

        if isinstance(file, (str, Path)):
            self._cfg.file = Path(file)

        try:
            with open(self._cfg.file, encoding="utf-8") as f:
                cfg = json.load(f)
        except:
            cfg = {}

        # map config items'key to item
        items = {}
        for name in dir(self._cfg.__class__):
            item = getattr(self._cfg.__class__, name)
            if isinstance(item, ConfigItem):
                items[item.key] = item

        # update the value of config item
        for k, v in cfg.items():
            if not isinstance(v, dict) and items.get(k) is not None:
                items[k].deserializeFrom(v)
            elif isinstance(v, dict):
                for key, value in v.items():
                    key = k + "." + key
                    if items.get(key) is not None:
                        items[key].deserializeFrom(value)

        self.theme = self.get(self._cfg.themeMode)
        
    def toDict(self, serialize=True):
        """ convert config items to `dict` """
        items = {}
        for name in dir(self._cfg.__class__):
            item = getattr(self._cfg.__class__, name)
            if not isinstance(item, ConfigItem):
                continue

            value = item.serialize() if serialize else item.value
            if not items.get(item.group):
                if not item.name:
                    items[item.group] = value
                else:
                    items[item.group] = {}

            if item.name:
                items[item.group][item.name] = value

        return items
    
qconfig = QConfig()


class NodeConfig(QConfig):
    """ Config of application """
    # NodeEditor Color
    penDarkColor = ColorConfigItem("NodeEditor_ColorPalette", "PenDark_Color", "#2a2a2a")
    penLightColor = ColorConfigItem("NodeEditor_ColorPalette", "PenLight_Color", "#222222")
    backgroundColor = ColorConfigItem("NodeEditor_ColorPalette", "Background_Color", "#1d1d1d")
    editBackgroundColor = ColorConfigItem("NodeEditor_ColorPalette", "EditBackground_Color", "#1d1d1d")
    # Node Color
    nodePenColor = ColorConfigItem("Node_ColorPalette", "NodePen_Color", "#7F000000")
    nodeTextColor = ColorConfigItem("Node_ColorPalette", "NodePen_Color", "#eeeeee")
    nodeTitleColor = OptionsConfigItem("NodeEditor_ColorPalette", "NodeTitle_Color", "#FF246283", OptionsValidator(["#FF246283", "#FF79461d", "#FF344621", "#FF83314a", "#FF1d2546", "#FF1d1d1d"]), restart=False)
    nodeTitleBrush = ColorConfigItem("Node_ColorPalette", "NodeTitle_Brush", "#1d725e")
    nodeBackgroundBrush = ColorConfigItem("Node_ColorPalette", "NodeBackground_Brush", "#E3303030")
    nodePenSelectedColor = ColorConfigItem("Node_ColorPalette", "NodePenSelected_Color", "#FFFFFF")
    # Edge Color
    edgePenColor = ColorConfigItem("Edge_ColorPalette", "EdgePen_Color", "#FF03bd91")
    edgeDragColor = ColorConfigItem("Edge_ColorPalette", "EdgeDrag_Color", "#FF03bd91")
    edgeSelectedColor = ColorConfigItem("Edge_ColorPalette", "EdgeSelected_Color", "#b3f3e4")
    # Socket Color
    socketColor = OptionsConfigItem("Socket_ColorPalette", "Socket_Color", "#FFa1a1a1", OptionsValidator(["#FFa1a1a1", "#FF00d6a3", "#FFc7c729", "#FF6363c7", "#FF598c5c", "#FFcca6d6", "#FF1d1d1d",]), restart=False)
    socketPenColor = ColorConfigItem("Socket_ColorPalette", "SocketPen_Color", "#FF000000")
    

cfg = NodeConfig()
qconfig.load("nodeeditor\\config\\config.json", cfg)
qconfig.save()