import sys
import pigpio

FINISH_SERVO = 18
TEMP_SERVO = 19
args = sys.argv

pi = pigpio.pi()

def setTempServo(value):
    print("temp")
    print(value)
    print(type(value))
    if value == 1:
        print("1")
        pi.set_servo_pulsewidth(TEMP_SERVO,2000)
    elif value == 0:
        print("0")
        pi.set_servo_pulsewidth(TEMP_SERVO,500)

def setFinishServo(value):
    print("finish")
    print(value)
    print(type(value))
    if value == 1:
        print("1")
        pi.set_servo_pulsewidth(FINISH_SERVO,2000)
    elif value==0:
        print("0")
        pi.set_servo_pulsewidth(FINISH_SERVO,500)


