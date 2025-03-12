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

def cleanup_gpio():
    GPIO.cleanup()

if __name__ == '__main__':
    init_gpio()
    try:
        unlock_door()
    finally:
        cleanup_gpio()
