import cv2
from utils.face_utils import detect_faces

# 打开摄像头
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("无法打开摄像头")
    exit()

# 预热摄像头
import time
time.sleep(2)

ret, frame = cap.read()
if not ret:
    print("无法读取摄像头帧")
else:
    # 将捕获到的图像转换为灰度图
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 检测人脸
    faces = detect_faces(gray)
    print("检测到的人脸数量：", len(faces))
    for (x, y, w, h) in faces:
        # 在图像上绘制绿色矩形框
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # 显示检测结果
    cv2.imshow("Face Detection", frame)
    print("按任意键关闭窗口")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

cap.release()
