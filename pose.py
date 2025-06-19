import struct, numpy as np

class Pose:
    def __init__(self, x: np.float32, heading: np.float32):
        self.header = np.uint8(1)
        self.x = np.float32(x)
        self.heading = np.float32(heading)

    def pack(self) -> bytes:
        return struct.pack('<iff', self.header, self.x, self.heading)

    @classmethod
    def unpack(cls, b: bytes) -> 'Pose':
        vals = struct.unpack('<iff', b)
        return cls(vals[1], vals[2])

