class SceneClipboard():
    def __init__(self, scene):
        self.scene = scene

    def serializeSelected(self, delete=False):
        return {}
    
    def deserializeFromClipboard(self, data):
        print("deserialize from clipboard, data: ", data)