import RPi.GPIO as GPIO
import time

# 假设继电器连接在 GPIO 17 引脚（可根据实际调整）
LOCK_PIN = 17

def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LOCK_PIN, GPIO.OUT)
    # 初始化为锁定状态（根据硬件实际逻辑）
    GPIO.output(LOCK_PIN, GPIO.LOW)

def unlock_door():
    """打开门锁（通过继电器控制）"""
    print("门锁已开启")
    GPIO.output(LOCK_PIN, GPIO.HIGH)  # 激活继电器
    time.sleep(5)  # 保持5秒
    GPIO.output(LOCK_PIN, GPIO.LOW)   # 关闭继电器
    print("门锁已关闭")

def control_door(is_recognized):
    """
    根据人脸识别结果控制门锁：
    - 如果识别成功（is_recognized 为 True），则开启门锁；
    - 如果识别失败，则不操作门锁。
    """
    if is_recognized:
        unlock_door()
    else:
        print("识别失败，门锁保持关闭")

def cleanup_gpio():
    GPIO.cleanup()

if __name__ == '__main__':
    init_gpio()
    try:
        # 示例调用，假设识别结果为 True 时开启门锁
        control_door(True)
    finally:
        cleanup_gpio()
