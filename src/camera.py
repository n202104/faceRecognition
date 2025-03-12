from picamera2 import Picamera2
import cv2

# 创建 Picamera2 实例
picam2 = Picamera2()
# 使用预览配置，适合实时显示
config = picam2.create_preview_configuration()
picam2.configure(config)

# 启动摄像头
picam2.start()
print("摄像头初始化成功")  # 初始化成功后打印一句话

def capture_frame():
    """
    捕获一帧图像并返回NumPy数组。
    """
    frame = picam2.capture_array()
    return frame
