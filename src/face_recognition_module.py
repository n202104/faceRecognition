from picamera2 import Picamera2
import cv2
import face_recognition

# 加载已知人脸图像并计算特征编码
known_image = face_recognition.load_image_file("/home/yun/myproject/known_face.jpg")
known_face_encoding = face_recognition.face_encodings(known_image)[0]

# 初始化摄像头
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)})
picam2.configure(config)
picam2.start()

# 定义检测频率变量：每隔 N 帧检测一次
frame_count = 0
detection_interval = 5  # 每隔5帧检测一次

# 存储上一次检测结果
previous_face_locations = []
previous_face_encodings = []

while True:
    frame = picam2.capture_array()          # 获取一帧图像，RGB 格式
    display_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # 转为 BGR 以便显示
    
    frame_count += 1
    if frame_count % detection_interval == 0:
        # 每隔 detection_interval 帧进行检测
        previous_face_locations = face_recognition.face_locations(frame)
        previous_face_encodings = face_recognition.face_encodings(frame, previous_face_locations)
    
    # 使用上一次检测结果
    for (top, right, bottom, left), face_encoding in zip(previous_face_locations, previous_face_encodings):
        matches = face_recognition.compare_faces([known_face_encoding], face_encoding)
        label = "Authorized" if True in matches else "Unknown"
        
        cv2.rectangle(display_frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(display_frame, label, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    cv2.imshow("Real-time Face Recognition", display_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.stop()
cv2.destroyAllWindows()
