# utils/face_utils.py

import cv2
import numpy as np
import os
from PIL import Image
from utils.constants import CASCADE_PATH, FACE_DATA_PATH, FACE_TRAINING_PATH

# 初始化 Haar 级联分类器
faceCascade = cv2.CascadeClassifier(CASCADE_PATH)

def detect_faces(gray_frame):
    """
    在灰度图像中检测人脸。
    返回检测到的人脸区域列表，每个区域为 (x, y, w, h)。
    """
    faces = faceCascade.detectMultiScale(
        gray_frame,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20)
    )
    return faces

def save_face_samples(user_id, image, sample_count):
    """
    在给定图像中检测人脸，并保存检测到的人脸区域为灰度图像样本。
    参数:
      user_id: 用户标识（用于文件命名）
      image: 原始图像（BGR 格式）
      sample_count: 当前已保存的样本数量
    返回更新后的样本计数。
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detect_faces(gray)
    if not os.path.exists(FACE_DATA_PATH):
        os.makedirs(FACE_DATA_PATH, exist_ok=True)
        os.chmod(FACE_DATA_PATH, 0o777)
    for (x, y, w, h) in faces:
        sample_count += 1
        face_img = gray[y:y+h, x:x+w]
        filename = f"{FACE_DATA_PATH}/User.{user_id}.{sample_count}.png"
        cv2.imwrite(filename, face_img)
    return sample_count

def get_images_and_labels(path):
    """
    遍历指定目录，读取所有保存的人脸图像及其标签。
    文件名要求格式为 "User.{id}.{sample}.png"。
    返回:
      face_samples: 人脸图像数据列表
      ids: 对应的人脸标签列表
    """
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    face_samples = []
    ids = []
    for imagePath in imagePaths:
        try:
            PIL_img = Image.open(imagePath).convert('L')
        except Exception as e:
            print(f"读取图片 {imagePath} 失败: {e}")
            continue
        img_numpy = np.array(PIL_img, 'uint8')
        try:
            user_id = int(os.path.split(imagePath)[-1].split(".")[1])
        except Exception as e:
            print(f"解析文件名 {imagePath} 失败: {e}")
            continue
        faces = detect_faces(img_numpy)
        for (x, y, w, h) in faces:
            face_samples.append(img_numpy[y:y+h, x:x+w])
            ids.append(user_id)
    return face_samples, ids

def train_faces():
    """
    使用 FACE_DATA_PATH 目录下的样本数据训练人脸识别模型，
    并将训练好的模型保存到 FACE_TRAINING_PATH。
    返回训练后不同人脸的数量。
    """
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_samples, ids = get_images_and_labels(FACE_DATA_PATH)
    if len(face_samples) == 0:
        print("没有检测到任何人脸样本！")
        return 0
    recognizer.train(face_samples, np.array(ids))
    training_dir = os.path.dirname(FACE_TRAINING_PATH)
    if not os.path.exists(training_dir):
        os.makedirs(training_dir, exist_ok=True)
        os.chmod(training_dir, 0o777)
    recognizer.write(FACE_TRAINING_PATH)
    unique_ids = len(set(ids))
    print(f"\n [INFO] 训练完成，共有 {unique_ids} 个不同人脸。模型保存在 {FACE_TRAINING_PATH}")
    return unique_ids
