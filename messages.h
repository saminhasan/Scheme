#ifndef MESSAGES_H
#define MESSAGES_H

#include <cstdint>

struct TestType {
    byte header = 0;
    int8_t i8;
    int16_t i16;
    int32_t i32;
    int64_t i64;
    uint8_t u8;
    uint16_t u16;
    uint32_t u32;
    uint64_t u64;
    float32_t f32;
    float64_t f64;
    byte alias;
    int8_t arr8[4];
    float32_t mat2x3[2][3];
    uint32_t buffer[10];
};

struct HeartBeat {
    byte header = 0;
};

struct Reboot {
    byte header = 2;
};

struct EStop {
    byte header = 4;
};

struct Enable {
    byte header = 6;
};

struct Disable {
    byte header = 8;
};

struct Calibrate {
    byte header = 10;
};

struct Mode {
    byte header = 14;
    byte value;
};

struct Pose6D {
    byte header = 16;
    float32_t x;
    float32_t y;
    float32_t z;
    float32_t roll;
    float32_t pitch;
    float32_t yaw;
};

struct StagePosition {
    byte header = 12;
};

struct TrajectoryLength {
    byte header = 18;
    uint32_t length;
};

struct FeedRate {
    byte header = 20;
    byte feed_rate;
};

struct Trajectory {
    byte header = 22;
    float32_t dataArray[10000][6];
};

#endif // MESSAGES_H
