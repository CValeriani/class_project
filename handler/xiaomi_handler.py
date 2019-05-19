from handler.xiaomi_Yi.xiaomi_yi import XiaomiYi

class XiaomiCam():
    def __init__(self, addr, port):
        self.camera = XiaomiYi(ip=addr, port=port, timeout=4)
        self.camera.connect()

    def vid_stream(self):
        self.camera.stream()

    def vid_close(self):
        self.camera.close()