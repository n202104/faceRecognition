import cv2
from camera import capture_frame
from face_recognition_module import load_known_faces, recognize_face
from door_control import init_gpio, unlock_door, cleanup_gpio

def main():
    # 初始化GPIO
    init_gpio()
    
    # 加载已知人脸特征和对应名称
    known_face_encodings, known_face_names = load_known_faces()
    
    while True:
        frame = capture_frame()
        if frame is None:
            continue
        
        # 可选：调整图像尺寸（提高识别速度）
        frame_small = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        
        # 调用人脸识别函数
        name = recognize_face(frame_small, known_face_encodings, known_face_names)
        if name:
            print("识别到：", name)
            unlock_door()
        
        cv2.imshow("Video", frame)
        # 按 'q' 键退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cleanup_gpio()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
