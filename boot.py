from lx16a import *
import time

LX16A.initialize("/dev/ttyUSB0", 0.1)

try:
    servo1 = LX16A(111)
    servo2 = LX16A(121)
    servo3 = LX16A(211)
    servo4 = LX16A(221)

    servo1.set_angle_limits(0, 240)
    servo2.set_angle_limits(0, 240)
    servo3.set_angle_limits(0, 240)
    servo4.set_angle_limits(0, 240)

except ServoTimeoutError as e:
    print(f"Servo {e.id_} is not responding. Exiting...")
    quit()

# Homing / Boot sequence
''' This is a homing/boot sequence to check servo motors are moving correctly.
The sequence moves each servo by +10 and -10 degrees from current position and then
homes it at 120 degrees. A time delay of 0.5s between moves has been implemented.'''

time.sleep(2)

servo1Home = 120
servo2Home = 125
servo3Home = 100
servo4Home = 145

bootMode = True

if bootMode:
    try:
        servo1.move(servo1Home + 10)
        time.sleep(0.5)
        servo1.move(servo1Home - 10)
        time.sleep(0.5)
        servo1.move(servo1Home)
        time.sleep(0.5)

    except:
        print("Servo 1 error during homing sequence")
        quit()

    try:
        servo2.move(servo2Home + 10)
        time.sleep(0.5)
        servo2.move(servo2Home - 10)
        time.sleep(0.5)
        servo2.move(servo2Home)
        time.sleep(0.5)

    except:
        print("Servo 2 error during homing sequence")
        quit()

    try:
        servo3.move(servo3Home + 10)
        time.sleep(0.5)
        servo3.move(servo3Home - 10)
        time.sleep(0.5)
        servo3.move(servo3Home)
        time.sleep(0.5)

    except:
        print("Servo 3 error during homing sequence")
        quit()

    try:
        servo4.move(servo4Home + 10)
        time.sleep(0.5)
        servo4.move(servo4Home - 10)
        time.sleep(0.5)
        servo4.move(servo4Home)
        time.sleep(0.5)

    except:
        print("Servo 4 error during homing sequence")
        quit()
