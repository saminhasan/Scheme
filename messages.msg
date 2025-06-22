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
message Q {
  byte   header = 16;
  float32_t axisAngle[6];
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
message ACK {
  byte header = 24;
  uint32_t sequence;
}
message NACK {
  byte header = 26;
  uint32_t sequence;
}
message SyncTime {
  byte header = 28;
}