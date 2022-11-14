from math import sin, cos
from pylx16a.lx16a import *
import time

LX16A.initialize("COM3", 0.1)

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

t = 0
while True:
    servo1.move(sin(t) * 60 + 60)
    servo2.move(cos(t) * 60 + 60)
    servo3.move(sin(t) * 60 + 60)
    servo4.move(cos(t) * 60 + 60)

    time.sleep(0.05)
    t += 0.1
