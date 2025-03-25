# utils/gpio_utils.py

import RPi.GPIO as GPIO
import atexit
import time

# 初始化 GPIO 设置
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(17, GPIO.OUT, initial=False)
servo_pwm = GPIO.PWM(17, 50)  # 50 Hz PWM
servo_pwm.start(0)

def cleanup_gpio():
    """
    清理 GPIO 资源：停止 PWM 并重置 GPIO 状态
    """
    servo_pwm.stop()
    GPIO.cleanup()

atexit.register(cleanup_gpio)

def unlock_door():
    """
    开锁操作：调整 PWM 信号使门锁舵机转到开锁位置，同时设置 GPIO25 为高电平
    """
    servo_pwm.ChangeDutyCycle(2.5)  # 这个值根据实际硬件可能需要调整
    GPIO.output(25, GPIO.HIGH)
    time.sleep(0.2)
    servo_pwm.ChangeDutyCycle(0)

def lock_door():
    """
    关锁操作：调整 PWM 信号使门锁舵机转到关锁位置，同时设置 GPIO25 为低电平
    """
    servo_pwm.ChangeDutyCycle(12.5)  # 这个值根据实际硬件可能需要调整
    GPIO.output(25, GPIO.LOW)
    time.sleep(0.2)
    servo_pwm.ChangeDutyCycle(0)
