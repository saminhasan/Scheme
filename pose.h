#ifndef POSE_H
#define POSE_H

#include <cstdint>

struct Pose {
    int32_t header = 1;
    float32_t x;
    float32_t heading;
};

#endif // POSE_H
