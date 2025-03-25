# 人脸识别门禁系统
## 前期准备
树莓派4b带摄像头  
Python 3.11.2  
查阅GPIO引脚https://hackpi.fun/docs/usage/gpio/
## 问题记录
- 管理员界面无法录入人脸问题
> 树莓派默认使用 libcamera，导致 OpenCV 的 cv2.VideoCapture(0) 无法正常工作

解决方案：使用 libcamera + picamera2 来替代 cv2.VideoCapture(0)

- 点击普通用户闪退问题
> 没有导入time模块

- 采集完照片后未生成训练文件
> 该问题导致点击普通用户直接报错（无法加载训练文件问题）