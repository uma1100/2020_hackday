import sys
import pigpio

SERVO_PIN = 18

args = sys.argv

f = 0
if ( len( args ) > 1 ):
    if ( args[1].isdecimal() ):
        p_width = int( args[1] )
        if ( p_width >= 500 and p_width <= 2500 ):
            f = 1
if ( f == 1 ):
    print ("Servo set", p_width )
    pi = pigpio.pi()
    pi.set_servo_pulsewidth(SERVO_PIN, p_width)
else:
    print ("USAGE: python3 servo.py PULSE_WIDTH")
    print ("  PULSE_WHDHT : Pulse range is 500-2500.")
