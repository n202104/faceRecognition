import cv2
from camera import capture_frame
from face_recognition_module import load_known_faces, recognize_face
from door_control import init_gpio, control_door, cleanup_gpio

def main():
    # 初始化门锁控制GPIO
    init_gpio()
    
    # 加载已知人脸特征和对应名称
    known_faces_path = "/home/yun/myproject/known_faces"  # 修改成你的图片实际路径
    known_face_encodings = load_known_faces(known_faces_path)
    known_face_names = ["Known"]  # 如果只有一个人，可以这样固定名称

    while True:
        frame = capture_frame()
        if frame is None:
            continue
        
        # 调整图像尺寸以提高识别速度
        frame_small = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        
        # 进行人脸识别
        name = recognize_face(frame_small, known_face_encodings, known_face_names)
        if name:
            print("识别成功：", name)
            recognized = True
        else:
            print("识别失败，门锁保持关闭")
            recognized = False
        
        # 根据识别结果控制门锁
        control_door(recognized)
        
        # 显示视频画面
        cv2.imshow("Video", frame)
        # 按 'q' 键退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cleanup_gpio()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
