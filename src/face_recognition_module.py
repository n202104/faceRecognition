import cv2
import face_recognition
from picamera2 import Picamera2
import time

def main():
    # 加载已知人脸图像并计算其编码
    known_image = face_recognition.load_image_file("/home/yun/myproject/known_face.jpg")
    known_face_encoding = face_recognition.face_encodings(known_image)[0]
    
    # 初始化摄像头（根据需要调整分辨率以提高性能）
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)})
    picam2.configure(config)
    picam2.start()
    
    display_on = False             # 标记视频窗口是否已打开
    last_face_time = time.time()     # 记录上一次检测到人脸的时间
    recognition_start_time = None    # 记录当前人脸识别开始的时间
    
    frame_count = 0                # 帧计数器，每15帧更新一次检测
    cached_overlay_data = None     # 缓存检测结果，用于非检测帧绘制边框和文本

    while True:
        # 捕获一帧图像（RGB格式），转换为BGR格式以便OpenCV显示
        frame = picam2.capture_array()
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame_count += 1
        
        # 每15帧更新一次人脸检测和识别结果
        if frame_count % 15 == 0:
            # 进行人脸检测
            face_locations = face_recognition.face_locations(frame)
            
            if face_locations:
                # 检测到人脸：更新检测时间
                last_face_time = time.time()
                # 如果窗口尚未打开，则打开窗口
                if not display_on:
                    cv2.namedWindow("Real-time Face Recognition", cv2.WINDOW_AUTOSIZE)
                    print("Camera On")
                    display_on = True
                # 记录识别开始时间
                if recognition_start_time is None:
                    recognition_start_time = time.time()
                
                # 根据识别开始时间判断显示效果
                if time.time() - recognition_start_time < 1.0:
                    # 1秒内显示黄色“Recognizing...”状态
                    cached_overlay_data = []
                    for (top, right, bottom, left) in face_locations:
                        cached_overlay_data.append((top, right, bottom, left, (0, 255, 255), "Recognizing..."))
                else:
                    # 超过1秒后进行识别，并缓存结果（绿色或红色）
                    face_encodings = face_recognition.face_encodings(frame, face_locations)
                    cached_overlay_data = []
                    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                        matches = face_recognition.compare_faces([known_face_encoding], face_encoding)
                        if True in matches:
                            color = (0, 255, 0)  # 绿色表示识别成功
                            text = "Recognition Successful"
                            print("Recognition Successful")
                        else:
                            color = (0, 0, 255)  # 红色表示识别失败
                            text = "Recognition Failed"
                            print("Recognition Failed")
                        cached_overlay_data.append((top, right, bottom, left, color, text))
            else:
                # 未检测到人脸时，重置识别开始时间及缓存
                recognition_start_time = None
                cached_overlay_data = None

        # 仅在窗口打开时绘制检测结果，并显示当前帧
        if display_on:
            if cached_overlay_data:
                for (top, right, bottom, left, color, text) in cached_overlay_data:
                    if text == "Recognizing...":
                        cv2.rectangle(frame_bgr, (left, top), (right, bottom), (0, 255, 255), 2)
                        cv2.putText(frame_bgr, text, (left, top - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                    else:
                        offset = 2
                        cv2.rectangle(frame_bgr, (left + offset, top + offset), (right - offset, bottom - offset), color, 2)
                        cv2.putText(frame_bgr, text, (left, top - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            cv2.imshow("Real-time Face Recognition", frame_bgr)
        
        # 如果连续15秒未检测到人脸，则关闭窗口
        if time.time() - last_face_time > 15:
            if display_on:
                cv2.destroyWindow("Real-time Face Recognition")
                print("Camera Off")
                display_on = False
        
        # 按 'q' 键退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # 退出循环后停止摄像头并关闭所有窗口
    picam2.stop()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
