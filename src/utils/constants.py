# utils/constants.py

# 人脸标签对应的人物名称列表
NAMES = [
    'None', 'oneStar', 'denghaibo', 'zhangzhaohui',
    'zhangchaoyang', 'guomo', 'yanjie', 'luochao',
    'yanggong', 'gaogong'
]

# Haar级联分类器文件路径（请根据实际情况修改路径）
CASCADE_PATH = './resources/haarcascades/haarcascade_frontalface_default.xml'

# 保存采集人脸样本的目录
FACE_DATA_PATH = './data/Face_data/'

# 训练后模型文件保存路径
FACE_TRAINING_PATH = './data/Face_training/trainer.yml'
