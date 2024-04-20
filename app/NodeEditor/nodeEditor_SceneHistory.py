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
        if DEBUG: print("Restoring history ... current_step: @%d" % self.history_current_step, 
                        "(%d)" % len(self.history_stack))
            
    def storeHistory(self, desc):
        if DEBUG: print("Storing history", '"%s"' % desc,
                        "... current_step: @%d" % self.history_current_step, 
                        "(%d)" % len(self.history_stack))
            
        # 歷史紀錄超過上限
        if self.history_current_step+1 >= self.history_limit:
            self.history_stack = self.history_stack[1:]
            self.history_current_step -=1
            
        hs = self.createHistoryStamp(desc)

        self.history_stack.append(hs)
        self.history_current_step += 1
        if DEBUG: print(" -- setting step to: ", self.history_current_step)

    def createHistoryStamp(self, desc):
        return desc
            
    def restoreHistoryStamp(self, history_stamp):
        if DEBUG: print("RHS: ", history_stamp)