# Manim Community 節點編輯器
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django)

_期待可以做出一個國中生也能輕鬆遊玩並做出屬於自己的數學動畫製作軟體_
## 資料夾說明
* app - 主資料夾
* config - 基礎設定資料夾
  * icon.py - 圖標路徑
  * palette.py - 顏色路徑
* Node - 節點編輯器資料夾
  * node_Edge.py - 線段基本構造
  * node_Node.py - 節點基本構造
  * node_Socket.py - 連結點基本構造
  * nodeEditor_Scene.py - 節點編輯器畫面
  * nodeEditor_Window.py - 節點編輯器視窗
* resources - 材質包
  * icons - 圖標資料夾
  * qss - QSS 樣式資料夾

## 進度
> 參考影片清單：[https://www.youtube.com/watch?v=xbTLhMJARrk&list=PLZSNHzwDCOggHLThIbCxUhWTgrKVemZkz](https://www.youtube.com/watch?v=xbTLhMJARrk&list=PLZSNHzwDCOggHLThIbCxUhWTgrKVemZkz)

### 目前進度截圖
#### 2024.03.29
![2024.03.29進度螢幕截圖](PyQt5-Manim-Node/app/resources/screenshot/20240403.png)

### 影片練習觀看進度
#### 第一部分：節點編輯器架構
* [ ] [Node Editor in Python Tutorial Series: Introduction](https://www.youtube.com/watch?v=xbTLhMJARrk&list=PLZSNHzwDCOggHLThIbCxUhWTgrKVemZkz) (跳過)
* [ ] [Node Editor 00: Prerequisities - How to setup PyCharm](https://www.youtube.com/watch?v=YV1mEYd7nyM&list=PLZSNHzwDCOggHLThIbCxUhWTgrKVemZkz&index=2) (跳過)
* [x] [Node Editor Tutorial 01: How to create View, Scene and Grid Background](https://www.youtube.com/watch?v=YKpInnvaM-M&list=PLZSNHzwDCOggHLThIbCxUhWTgrKVemZkz&index=3)
* [x] [Node Editor Tutorial 02: How to add items to GraphicsView](https://www.youtube.com/watch?v=kvZVwaZ3WZE&list=PLZSNHzwDCOggHLThIbCxUhWTgrKVemZkz&index=4)
* [x] [Node Editor Tutorial 03: How to navigate scene](https://www.youtube.com/watch?v=5IKOIOg76so&list=PLZSNHzwDCOggHLThIbCxUhWTgrKVemZkz&index=5)
* [x] [Node Editor Tutorial 04: Implementing Scene](https://www.youtube.com/watch?v=MO2ptcCyacY&list=PLZSNHzwDCOggHLThIbCxUhWTgrKVemZkz&index=6)
* [x] [Node Editor Tutorial 05: How to implement Node](https://www.youtube.com/watch?v=CW6QQgUk2qI&list=PLZSNHzwDCOggHLThIbCxUhWTgrKVemZkz&index=7)
* [x] [Node Editor Tutorial 06: Implementing Node Content](https://www.youtube.com/watch?v=YaX8ZQnBgcc&list=PLZSNHzwDCOggHLThIbCxUhWTgrKVemZkz&index=8)
* [x] [Node Editor Tutorial 07: How to implement Sockets](https://www.youtube.com/watch?v=Rs5-Se2F3j8&list=PLZSNHzwDCOggHLThIbCxUhWTgrKVemZkz&index=9)
* [x] [Node Editor Tutorial 08: How to implement Edges](https://www.youtube.com/watch?v=Bis2KcGLfI4&list=PLZSNHzwDCOggHLThIbCxUhWTgrKVemZkz&index=10)
* [x] [Node Editor Tutorial 09: Positioning Edges and Debugging](https://www.youtube.com/watch?v=OPFloSj4GdE&list=PLZSNHzwDCOggHLThIbCxUhWTgrKVemZkz&index=11)
* [x] [Node Editor Tutorial 10: Finishing Edges and Socket Variations](https://www.youtube.com/watch?v=AoSKt36k9bk&list=PLZSNHzwDCOggHLThIbCxUhWTgrKVemZkz&index=12)
* [x] [Node Editor Tutorial 11: How to create Dragging Edge](https://www.youtube.com/watch?v=pk4v2xuXlm4&list=PLZSNHzwDCOggHLThIbCxUhWTgrKVemZkz&index=13)
* [x] [Node Editor Tutorial 12: Finishing Dragging Edge](https://www.youtube.com/watch?v=-VYcQojkloE&list=PLZSNHzwDCOggHLThIbCxUhWTgrKVemZkz&index=14)
* [ ] [Node Editor Tutorial 13: How to implement Selecting Items](https://www.youtube.com/watch?v=efvvJHHLWxA&list=PLZSNHzwDCOggHLThIbCxUhWTgrKVemZkz&index=15)
* [ ] [Node Editor Tutorial 14: Implementing Deleting Items](https://www.youtube.com/watch?v=POiyj0CbUpI&list=PLZSNHzwDCOggHLThIbCxUhWTgrKVemZkz&index=16)
* [ ] [Node Editor Tutorial 15: Cutting Edges](https://www.youtube.com/watch?v=kH3s2ALpcLo&list=PLZSNHzwDCOggHLThIbCxUhWTgrKVemZkz&index=17)

#### 第二部分：節點編輯器功能
* [ ] [Node Editor Tutorial 16: Introduction to Serialization](https://www.youtube.com/watch?v=CNyHqmE5KoU&list=PLZSNHzwDCOggHLThIbCxUhWTgrKVemZkz&index=18)