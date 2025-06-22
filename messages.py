import struct, numpy as np

class HeartBeat:
    def __init__(self):
        self.header = np.uint8(0)

    def pack(self) -> bytes:
        return struct.pack('<B', self.header)

    @classmethod
    def unpack(cls, b: bytes) -> 'HeartBeat':
        vals = struct.unpack('<B', b)
        return cls()

class Reboot:
    def __init__(self):
        self.header = np.uint8(2)

    def pack(self) -> bytes:
        return struct.pack('<B', self.header)

    @classmethod
    def unpack(cls, b: bytes) -> 'Reboot':
        vals = struct.unpack('<B', b)
        return cls()

class EStop:
    def __init__(self):
        self.header = np.uint8(4)

    def pack(self) -> bytes:
        return struct.pack('<B', self.header)

    @classmethod
    def unpack(cls, b: bytes) -> 'EStop':
        vals = struct.unpack('<B', b)
        return cls()

class Enable:
    def __init__(self):
        self.header = np.uint8(6)

    def pack(self) -> bytes:
        return struct.pack('<B', self.header)

    @classmethod
    def unpack(cls, b: bytes) -> 'Enable':
        vals = struct.unpack('<B', b)
        return cls()

class Disable:
    def __init__(self):
        self.header = np.uint8(8)

    def pack(self) -> bytes:
        return struct.pack('<B', self.header)

    @classmethod
    def unpack(cls, b: bytes) -> 'Disable':
        vals = struct.unpack('<B', b)
        return cls()

class Calibrate:
    def __init__(self):
        self.header = np.uint8(10)

    def pack(self) -> bytes:
        return struct.pack('<B', self.header)

    @classmethod
    def unpack(cls, b: bytes) -> 'Calibrate':
        vals = struct.unpack('<B', b)
        return cls()

class Mode:
    def __init__(self, value: np.uint8):
        self.header = np.uint8(14)
        self.value = np.uint8(value)

    def pack(self) -> bytes:
        return struct.pack('<BB', self.header, self.value)

    @classmethod
    def unpack(cls, b: bytes) -> 'Mode':
        vals = struct.unpack('<BB', b)
        return cls(vals[1])

class Q:
    def __init__(self, axisAngle: np.ndarray):
        self.header = np.uint8(16)
        self.axisAngle = np.asarray(axisAngle, dtype=np.float32_t)  # shape [6]

    def pack(self) -> bytes:
        flat = self.axisAngle.ravel()
        return struct.pack('<B6f', self.header, *flat)

    @classmethod
    def unpack(cls, b: bytes) -> 'Q':
        allv = struct.unpack('<B6f', b)
        header = allv[0]
        data = np.array(allv[1:], dtype=np.float32_t)
        data = data.reshape([6])
        return cls(data)  # header is constant

class StagePosition:
    def __init__(self):
        self.header = np.uint8(12)

    def pack(self) -> bytes:
        return struct.pack('<B', self.header)

    @classmethod
    def unpack(cls, b: bytes) -> 'StagePosition':
        vals = struct.unpack('<B', b)
        return cls()

class TrajectoryLength:
    def __init__(self, length: np.uint32):
        self.header = np.uint8(18)
        self.length = np.uint32(length)

    def pack(self) -> bytes:
        return struct.pack('<BI', self.header, self.length)

    @classmethod
    def unpack(cls, b: bytes) -> 'TrajectoryLength':
        vals = struct.unpack('<BI', b)
        return cls(vals[1])

class FeedRate:
    def __init__(self, feed_rate: np.uint8):
        self.header = np.uint8(20)
        self.feed_rate = np.uint8(feed_rate)

    def pack(self) -> bytes:
        return struct.pack('<BB', self.header, self.feed_rate)

    @classmethod
    def unpack(cls, b: bytes) -> 'FeedRate':
        vals = struct.unpack('<BB', b)
        return cls(vals[1])

class Trajectory:
    def __init__(self, dataArray: np.ndarray):
        self.header = np.uint8(22)
        self.dataArray = np.asarray(dataArray, dtype=np.float32_t)  # shape [10000, 6]

    def pack(self) -> bytes:
        flat = self.dataArray.ravel()
        return struct.pack('<B60000f', self.header, *flat)

    @classmethod
    def unpack(cls, b: bytes) -> 'Trajectory':
        allv = struct.unpack('<B60000f', b)
        header = allv[0]
        data = np.array(allv[1:], dtype=np.float32_t)
        data = data.reshape([10000, 6])
        return cls(data)  # header is constant

class ACK:
    def __init__(self, sequence: np.uint32):
        self.header = np.uint8(24)
        self.sequence = np.uint32(sequence)

    def pack(self) -> bytes:
        return struct.pack('<BI', self.header, self.sequence)

    @classmethod
    def unpack(cls, b: bytes) -> 'ACK':
        vals = struct.unpack('<BI', b)
        return cls(vals[1])

class NACK:
    def __init__(self, sequence: np.uint32):
        self.header = np.uint8(26)
        self.sequence = np.uint32(sequence)

    def pack(self) -> bytes:
        return struct.pack('<BI', self.header, self.sequence)

    @classmethod
    def unpack(cls, b: bytes) -> 'NACK':
        vals = struct.unpack('<BI', b)
        return cls(vals[1])

class SyncTime:
    def __init__(self):
        self.header = np.uint8(28)

    def pack(self) -> bytes:
        return struct.pack('<B', self.header)

    @classmethod
    def unpack(cls, b: bytes) -> 'SyncTime':
        vals = struct.unpack('<B', b)
        return cls()



# --- Dispatch table and decoder ---
msg_dispatch = {
    0: HeartBeat,
    2: Reboot,
    4: EStop,
    6: Enable,
    8: Disable,
    10: Calibrate,
    14: Mode,
    16: Q,
    12: StagePosition,
    18: TrajectoryLength,
    20: FeedRate,
    22: Trajectory,
    24: ACK,
    26: NACK,
    28: SyncTime,
}

def decode_msg(blob: bytes):
    header = blob[0]
    cls = msg_dispatch.get(header)
    if cls is None:
        raise ValueError(f'Unknown message header: {header}')
    return cls.unpack(blob)
