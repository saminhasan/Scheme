#ifndef MESSAGES_H
#define MESSAGES_H

#include <cstdint>

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

struct Q {
    byte header = 16;
    float32_t axisAngle[6];
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

struct ACK {
    byte header = 24;
    uint32_t sequence;
};

struct NACK {
    byte header = 26;
    uint32_t sequence;
};

struct SyncTime {
    byte header = 28;
};

#endif // MESSAGES_H
