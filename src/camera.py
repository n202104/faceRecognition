from picamera2 import Picamera2
import cv2

# 创建 Picamera2 实例
picam2 = Picamera2()
# 使用预览配置，适合实时显示
config = picam2.create_preview_configuration()
picam2.configure(config)

# 启动摄像头
picam2.start()

while True:
    # 捕获一帧图像，得到 NumPy 数组
    frame = picam2.capture_array()

    # 在窗口显示图像
    cv2.imshow("Camera Preview", frame)

    # 如果按下 'q' 键则退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 停止摄像头并关闭窗口
picam2.stop()
cv2.destroyAllWindows()
