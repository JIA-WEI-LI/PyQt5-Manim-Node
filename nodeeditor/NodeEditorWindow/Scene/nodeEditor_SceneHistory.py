from ..Edge.node_GraphicsEdge import NodeGraphicsEdge
from common import *

DEBUG = DebugMode.NODEEDITOR_SCENEHISTORY

class SceneHistory():
    def __init__(self, scene):
        self.scene = scene

        self.clear()
        # HACK: 若數值調整過高容易導致切割較早線段閃退
        self.history_limit = 8

        self._history_modified_listeners = []

    def clear(self):
        self.history_stack = []
        self.history_current_step = -1

    def storeInitialHistoryStamp(self):
        self.storeHistory("Initial History Stamp")

    def canUndo(self):
        return self.history_current_step > 0
    
    def canRedo(self):
        return self.history_current_step + 1 < len(self.history_stack)

    def undo(self):
        if DEBUG: print("UNDO")

        if self.canUndo():
            self.history_current_step -= 1
            self.restoreHistory()
            self.scene.has_been_modified = True

    def redo(self):
        if DEBUG: print("REDO Current step: ", self.history_current_step)

        if self.canRedo():
            self.history_current_step += 1
            self.restoreHistory()
            self.scene.has_been_modified = True

    def addHistoryModifiedListener(self, callback):
        self._history_modified_listeners.append(callback)

    def restoreHistory(self):
        if DEBUG: print("Restoring history ... current_step: @%d" % self.history_current_step, 
                        "(%d)" % len(self.history_stack))
        self.restoreHistoryStamp(self.history_stack[self.history_current_step])
        for callback in self._history_modified_listeners: callback()
            
    def storeHistory(self, desc, setModified=False):
        if setModified == False:
            self.scene.has_been_modified = True
        if DEBUG: print("Storing history", '"%s"' % desc,
                        "... current_step: @%d" % self.history_current_step, 
                        "(%d)" % len(self.history_stack))
            
        if self.history_current_step+1 < len(self.history_stack):
            self.history_stack = self.history_stack[0:self.history_current_step+1]
            
        # 歷史紀錄超過上限
        if self.history_current_step+1 >= self.history_limit:
            self.history_stack = self.history_stack[1:]
            self.history_current_step -=1

        hs = self.createHistoryStamp(desc)

        self.history_stack.append(hs)
        self.history_current_step += 1
        if DEBUG: print(" -- setting step to: ", self.history_current_step)

        for callback in self._history_modified_listeners: callback()

    def createHistoryStamp(self, desc):
        self_obj = {
            'nodes': [],
            'edges': [],
        }

        for item in self.scene.nodeGraphicsScene.selectedItems():
            if hasattr(item, 'node'):
                self_obj['nodes'].append(item.node.id)
            elif isinstance(item, NodeGraphicsEdge):
                self_obj['edges'].append(item.edge.id)

        history_stamp = {
            'desc': desc,
            'snapshot': self.scene.serialize(),
            'selection': self_obj
        }
        return history_stamp
            
    def restoreHistoryStamp(self, history_stamp):
        if DEBUG: print("RHS: ", history_stamp['desc'])

        try:
            self.scene.deserialize(history_stamp['snapshot'])

            # 回復選擇
            for edge_id in history_stamp['selection']['edges']:
                for edge in self.scene.edges:
                    if edge.id == edge.id:
                        edge.nodeGraphicsEdge.setSelected(True)
                        break

            for node_id in history_stamp['selection']['nodes']:
                for node in self.scene.nodes:
                    if node.id == node.id:
                        node.graphicsNode.setSelected(True)
                        break
        except Exception as e: dumpException(e)