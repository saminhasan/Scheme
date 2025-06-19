message TestType {
  byte     header = 0;
  int8_t   i8;
  int16_t  i16;
  int32_t  i32;
  int64_t  i64;
  uint8_t  u8;
  uint16_t u16;
  uint32_t u32;
  uint64_t u64;
  float32_t  f32;
  float64_t  f64;
  byte     alias;          // alias for uint8_t
  int8_t   arr8[4];
  float32_t  mat2x3[2][3];
  uint32_t buffer[10];
}

message HeartBeat {
  byte header = 0;
}
message Reboot {
  byte header = 2;
}
message EStop {
  byte header = 4;
}
message Enable {
  byte header = 6;
}
message Disable {
  byte header = 8;
}
message Calibrate {
  byte header = 10;
}
message Mode {
  byte   header = 14;
  byte   value;
}
message Pose6D {
  byte   header = 16;
  float32_t x;
  float32_t y;
  float32_t z;
  float32_t roll;
  float32_t pitch;
  float32_t yaw;
}
message StagePosition {
  byte header = 12;
}
message TrajectoryLength {
  byte   header = 18;
  uint32_t length;
}
message FeedRate {
  byte   header = 20;
  byte   feed_rate;
}
message Trajectory {
  byte   header = 22;
  float32_t dataArray[10000][6];
}
