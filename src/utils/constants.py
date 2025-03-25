import os

# 获取项目根目录（假设 utils 在 src/utils 里）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASCADE_PATH = os.path.join(BASE_DIR, "resources", "haarcascades", "haarcascade_frontalface_default.xml")

# 其它常量保持不变
NAMES = [
    'None', 'oneStar', 'denghaibo', 'zhangzhaohui',
    'zhangchaoyang', 'guomo', 'yanjie', 'luochao',
    'yanggong', 'gaogong'
]

FACE_DATA_PATH = os.path.join(BASE_DIR, "data", "Face_data")
FACE_TRAINING_PATH = os.path.join(BASE_DIR, "data", "Face_training", "trainer.yml")
