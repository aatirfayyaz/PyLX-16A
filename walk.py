from math import sin, cos
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

# Initializing walking sequence
'''The following represents the robot walking methodology.
Option1: Shift weight to back legs and move both front legs.
Option2: Shift weight to diagonal legs and move diagonals together.

For either case, we used a 5th-order polynomial trajectory to make sure that
all movement was smooth and even accounting for jerk etc.

q(t) = A*(t**5) + B*(t**4) + C*(t**3) + D*(t**2) + E*t + F
q'(t) = d/dt(q(t)) = 5*A*(t**4) + 4*B*(t**3) + 3*C*(t**2) + 2*D*t + E
q''(t) = d/dt(q'(t)) = 20*A*(t**3) + 12*B*(t**2) + 6*C*(t) + 2*D

with boundary conditions:

At time t = 0; q(t) = servoHome, q'(t) = 0, q''(t) = 0
At time t = 3; q(3) = servoHome + 30, q'(3) = 0, q''(3) = 0
'''
angleChange = 30

servo1Final = servo1Home + angleChange
servo2Final = servo2Home + angleChange
servo3Final = servo3Home + angleChange
servo4Final = servo4Home + angleChange

t = 0
while t < 3:
    servo1.move(-(0.7407 * (t ** 5)) + (5.556 * (t ** 4)) - (11.111 * (t ** 3)) + servo1Home)  # forward move
    servo4.move((0.7407 * (t ** 5)) - (5.556 * (t ** 4)) + (11.111 * (t ** 3)) + servo4Home)  # forward move
    time.sleep(0.05)
    t += 0.1

t = 0

while t < 3:
    servo2.move((0.7407 * (t ** 5)) - (5.556 * (t ** 4)) + (11.111 * (t ** 3)) + servo2Home)  # forward move
    servo3.move(-(0.7407 * (t ** 5)) + (5.556 * (t ** 4)) - (11.111 * (t ** 3)) + servo3Home)  # forward move
    servo1.move((0.7407 * (t ** 5)) - (5.556 * (t ** 4)) + (11.111 * (t ** 3)) + servo1Final)  # backward move
    servo4.move(-(0.7407 * (t ** 5)) + (5.556 * (t ** 4)) - (11.111 * (t ** 3)) + servo4Final)  # backward move
    time.sleep(0.05)
    t += 0.1
