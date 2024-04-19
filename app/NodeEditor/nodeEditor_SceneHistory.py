from config.debug import DebugMode

DEBUG = DebugMode.NODEEEDITOR_SCENEHISTORY

class SceneHistory():
    def __init__(self, scene):
        self.scene = scene

        self.history_stack = []
        self.history_current_step = -1
        self.history_limit = 8

    def undo(self):
        if DEBUG: print("UNDO")

    def redo(self):
        if DEBUG: print("REDO")

    def restoreHistory(self):
        if DEBUG: print("Restoring history ... current_step: @%d" + self.self.history_current_step, 
                        "(%d)" + len(self.history_stack))
            
    def storeHistory(self, desc):
        if DEBUG: print("Storing history ... current_step: @%d" + self.self.history_current_step, 
                        "(%d)" + len(self.history_stack))
            
        hs = self.createHistoryStamp(desc)

    def createHistoryStamp(self, desc):
        return desc
            
    def restoreHistoryStamp(self, history_stamp):
        if DEBUG: print("RHS: ", history_stamp)