# utils/gpio_utils.py

import RPi.GPIO as GPIO
import atexit
import time

# 初始化GPIO设置
GPIO.setmode(GPIO.BCM)
# 设置GPIO25为输出，用于门禁控制
GPIO.setup(25, GPIO.OUT)
# 设置GPIO17为输出，并使用PWM控制（50Hz）
GPIO.setup(17, GPIO.OUT, initial=False)
servo_pwm = GPIO.PWM(17, 50)
servo_pwm.start(0)

def cleanup_gpio():
    """
    清理GPIO资源，停止PWM并重置GPIO状态
    """
    servo_pwm.stop()
    GPIO.cleanup()

atexit.register(cleanup_gpio)

def unlock_door():
    """
    开锁操作：
      - 调整PWM信号使门锁舵机转到开锁位置
      - 设置GPIO25为高电平
    """
    servo_pwm.ChangeDutyCycle(2.5)  # 根据具体硬件调整该值
    GPIO.output(25, GPIO.HIGH)
    time.sleep(0.2)
    servo_pwm.ChangeDutyCycle(0)

def lock_door():
    """
    关锁操作：
      - 调整PWM信号使门锁舵机转到关锁位置
      - 设置GPIO25为低电平
    """
    servo_pwm.ChangeDutyCycle(12.5)  # 根据具体硬件调整该值
    GPIO.output(25, GPIO.LOW)
    time.sleep(0.2)
    servo_pwm.ChangeDutyCycle(0)
