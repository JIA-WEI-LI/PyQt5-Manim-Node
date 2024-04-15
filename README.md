# Manim Community 節點編輯器
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django)

_期待可以做出一個國中生也能輕鬆遊玩並做出屬於自己的數學動畫製作軟體_
## 資料夾說明(過時待修)
* app - 主資料夾
* common - 常用設定資料夾
  * color_sheet - 
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
#### 2024.04.08
![2024.04.08進度螢幕截圖](app/resources/screenshot/20240408.png)

### 影片練習觀看進度
<details>
<summary>第一部分：節點編輯器架構</summary>

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
* [x] [Node Editor Tutorial 13: How to implement Selecting Items](https://www.youtube.com/watch?v=efvvJHHLWxA&list=PLZSNHzwDCOggHLThIbCxUhWTgrKVemZkz&index=15)
* [x] [Node Editor Tutorial 14: Implementing Deleting Items](https://www.youtube.com/watch?v=POiyj0CbUpI&list=PLZSNHzwDCOggHLThIbCxUhWTgrKVemZkz&index=16)
* [x] [Node Editor Tutorial 15: Cutting Edges](https://www.youtube.com/watch?v=kH3s2ALpcLo&list=PLZSNHzwDCOggHLThIbCxUhWTgrKVemZkz&index=17)

</details>
<details>
<summary>第二部分：節點編輯器功能</summary>

* [x] [Node Editor Tutorial 16: Introduction to Serialization](https://www.youtube.com/watch?v=CNyHqmE5KoU&list=PLZSNHzwDCOggHLThIbCxUhWTgrKVemZkz&index=18)
</details>


---

### 已知程式錯誤：
* [ ] BUG.24040601：已互相連結之線段若重複連線會造成程序崩潰閃退
* [ ] BUG.24040602：在節點內部使用滑鼠中鍵移動視窗時，放開滑鼠並移動到節點外部時鼠標樣式仍保持移動時樣式(放大視窗到最大時較明顯)
* [ ] BUG.24040603：在節點內部使用滑鼠中鍵移動視窗時，滑鼠鼠標有時樣式會跳動
* [ ] BUG.24040801：當視窗放大最大時，有機率無法自連接點延伸出線段

### 已知代待修改錯誤：
* [ ] COD.24040601：`node_node / node_GraphicsNode.py` 節點高度決定位置與預計不符
  > 預期計畫：新增可控制型向量類型，將會改變節點高度
* [x] ~~COD.24040602：`node_node / node_Node.py` 節點內部滑桿內容尚未完善~~
* [ ] COD.24040802：`node_node / node_GraphicsNode.py` 下拉式選單預設高度較進度條小，目前暫時使用另定義高度解決。