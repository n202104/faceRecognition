# 人脸识别门禁系统
## 前期准备
树莓派4b带摄像头  
Python 3.11.2  
查阅GPIO引脚https://hackpi.fun/docs/usage/gpio/
### 人脸识别模块
2025.3.12 实现了检测到人脸时开启视频画面，未检测到人脸约15秒关闭视频画面，由于树莓派设备性能不足，选择每15帧获取一次画面来保证视频画面相对流畅