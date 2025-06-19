import struct, numpy as np

class TestType:
    def __init__(self, i8: np.int8, i16: np.int16, i32: np.int32, i64: np.int64, u8: np.uint8, u16: np.uint16, u32: np.uint32, u64: np.uint64, f32: np.float32, f64: np.float64, alias: np.uint8, arr8: np.ndarray, mat2x3: np.ndarray, buffer: np.ndarray):
        self.header = np.uint8(0)
        self.i8 = np.int8(i8)
        self.i16 = np.int16(i16)
        self.i32 = np.int32(i32)
        self.i64 = np.int64(i64)
        self.u8 = np.uint8(u8)
        self.u16 = np.uint16(u16)
        self.u32 = np.uint32(u32)
        self.u64 = np.uint64(u64)
        self.f32 = np.float32(f32)
        self.f64 = np.float64(f64)
        self.alias = np.uint8(alias)
        self.arr8 = np.asarray(arr8, dtype=np.int8_t)  # shape [4]
        self.mat2x3 = np.asarray(mat2x3, dtype=np.float32_t)  # shape [2, 3]
        self.buffer = np.asarray(buffer, dtype=np.uint32_t)  # shape [10]

    def pack(self) -> bytes:
        flat = self.arr8.ravel()
        return struct.pack('<BbhiqBHIQfdB4b6f10I', self.header, *flat)

    @classmethod
    def unpack(cls, b: bytes) -> 'TestType':
        allv = struct.unpack('<BbhiqBHIQfdB4b6f10I', b)
        header = allv[0]
        data = np.array(allv[1:], dtype=np.int8_t)
        data = data.reshape([4])
        return cls(data)  # header is constant

class HeartBeat:
    def __init__(self, ):
        self.header = np.uint8(0)

    def pack(self) -> bytes:
        return struct.pack('<B', self.header)

    @classmethod
    def unpack(cls, b: bytes) -> 'HeartBeat':
        vals = struct.unpack('<B', b)
        return cls()

class Reboot:
    def __init__(self, ):
        self.header = np.uint8(2)

    def pack(self) -> bytes:
        return struct.pack('<B', self.header)

    @classmethod
    def unpack(cls, b: bytes) -> 'Reboot':
        vals = struct.unpack('<B', b)
        return cls()

class EStop:
    def __init__(self, ):
        self.header = np.uint8(4)

    def pack(self) -> bytes:
        return struct.pack('<B', self.header)

    @classmethod
    def unpack(cls, b: bytes) -> 'EStop':
        vals = struct.unpack('<B', b)
        return cls()

class Enable:
    def __init__(self, ):
        self.header = np.uint8(6)

    def pack(self) -> bytes:
        return struct.pack('<B', self.header)

    @classmethod
    def unpack(cls, b: bytes) -> 'Enable':
        vals = struct.unpack('<B', b)
        return cls()

class Disable:
    def __init__(self, ):
        self.header = np.uint8(8)

    def pack(self) -> bytes:
        return struct.pack('<B', self.header)

    @classmethod
    def unpack(cls, b: bytes) -> 'Disable':
        vals = struct.unpack('<B', b)
        return cls()

class Calibrate:
    def __init__(self, ):
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

class Pose6D:
    def __init__(self, x: np.float32, y: np.float32, z: np.float32, roll: np.float32, pitch: np.float32, yaw: np.float32):
        self.header = np.uint8(16)
        self.x = np.float32(x)
        self.y = np.float32(y)
        self.z = np.float32(z)
        self.roll = np.float32(roll)
        self.pitch = np.float32(pitch)
        self.yaw = np.float32(yaw)

    def pack(self) -> bytes:
        return struct.pack('<Bffffff', self.header, self.x, self.y, self.z, self.roll, self.pitch, self.yaw)

    @classmethod
    def unpack(cls, b: bytes) -> 'Pose6D':
        vals = struct.unpack('<Bffffff', b)
        return cls(vals[1], vals[2], vals[3], vals[4], vals[5], vals[6])

class StagePosition:
    def __init__(self, ):
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

