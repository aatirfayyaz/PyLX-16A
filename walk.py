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

time.sleep(1)

servo1Home = 120
servo2Home = 125
servo3Home = 100
servo4Home = 135

bootMode = False

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
At time t = T; q(T) = servoHome + angleChange, q'(T) = 0, q''(T) = 0
'''
angleChange = 30
timeEnd = 1
timeSleep = 0.002
timeStep = 0.025

servo1Final = servo1Home - angleChange
servo2Final = servo2Home + angleChange
servo3Final = servo3Home - angleChange
servo4Final = servo4Home + angleChange

# For angleChange = 30 degrees, timeEnd = 3
# coeffA = 0.7407
# coeffB = 5.5556
# coeffC = 11.1111

# For angleChange = 40 degrees, timeEnd = 3
# coeffA = 0.9877
# coeffB = 7.4074
# coeffC = 14.8148

# For angleChange = 30 degrees, timeEnd = 2
# coeffA = 5.625
# coeffB = 28.1250
# coeffC = 37.5

# For angleChange = 40 degrees, timeEnd = 2
# coeffA = 7.5
# coeffB = 37.5
# coeffC = 50

# For angleChange = 50 degrees, timeEnd = 2
# coeffA = 9.375
# coeffB = 46.875
# coeffC = 62.5

# For angleChange = 50 degrees, timeEnd = 3
# coeffA = 1.2346
# coeffB = 9.2593
# coeffC = 18.5185

# For angleChange = 40 degrees, timeEnd = 1
# coeffA = 240
# coeffB = 600
# coeffC = 400

# For angleChange = 60 degrees, timeEnd = 2
# coeffA = 11.25
# coeffB = 56.25
# coeffC = 75

# For angleChange = 30 degrees, timeEnd = 1
coeffA = 180
coeffB = 450
coeffC = 300

steps = 15

t = 0
while t < timeEnd:
    servo1.move(-(coeffA * (t ** 5)) + (coeffB * (t ** 4)) - (coeffC * (t ** 3)) + servo1Home)  # forward move
    servo4.move((coeffA * (t ** 5)) - (coeffB * (t ** 4)) + (coeffC * (t ** 3)) + servo4Home)  # forward move
    time.sleep(timeSleep)
    t += timeStep

for step in range(steps):
    t = 0
    while t < timeEnd:
        servo2.move((coeffA * (t ** 5)) - (coeffB * (t ** 4)) + (coeffC * (t ** 3)) + servo2Home)  # forward move
        servo3.move(-(coeffA * (t ** 5)) + (coeffB * (t ** 4)) - (coeffC * (t ** 3)) + servo3Home)  # forward move
        servo1.move((coeffA * (t ** 5)) - (coeffB * (t ** 4)) + (coeffC * (t ** 3)) + servo1Final)  # backward move
        servo4.move(-(coeffA * (t ** 5)) + (coeffB * (t ** 4)) - (coeffC * (t ** 3)) + servo4Final)  # backward move
        time.sleep(timeSleep)
        t += timeStep

    t = 0
    while t < timeEnd:
        servo2.move(-(coeffA * (t ** 5)) + (coeffB * (t ** 4)) - (coeffC * (t ** 3)) + servo2Final)  # backward move
        servo3.move((coeffA * (t ** 5)) - (coeffB * (t ** 4)) + (coeffC * (t ** 3)) + servo3Final)  # backward move
        servo1.move(-(coeffA * (t ** 5)) + (coeffB * (t ** 4)) - (coeffC * (t ** 3)) + servo1Home)  # forward move
        servo4.move((coeffA * (t ** 5)) - (coeffB * (t ** 4)) + (coeffC * (t ** 3)) + servo4Home)  # forward move
        time.sleep(timeSleep)
        t += timeStep

t = 0
# last move
while t < timeEnd:
    servo1.move((coeffA * (t ** 5)) - (coeffB * (t ** 4)) + (coeffC * (t ** 3)) + servo1Final)  # backward move
    servo4.move(-(coeffA * (t ** 5)) + (coeffB * (t ** 4)) - (coeffC * (t ** 3)) + servo4Final)  # backward move
    time.sleep(timeSleep)
    t += timeStep

shutDown = False

if shutDown:
    try:
        error = servo1.get_angle_offset(servo1Home)
        time.sleep(0.2)
        if error > 0.25:
            print("Servo 1 off it's home angle")
        servo1.disable_torque()

    except:
        print("Servo 1 error during shutdown sequence")
        quit()

    try:
        error = servo2.get_angle_offset(servo2Home)
        time.sleep(0.2)
        if error > 0.25:
            print("Servo 2 off it's home angle")
        servo2.disable_torque()

    except:
        print("Servo 2 error during shutdown sequence")
        quit()

    try:
        error = servo3.get_angle_offset(servo3Home)
        time.sleep(0.2)
        if error > 0.25:
            print("Servo 3 off it's home angle")
        servo3.disable_torque()

    except:
        print("Servo 3 error during shutdown sequence")
        quit()

    try:
        error = servo4.get_angle_offset(servo4Home)
        time.sleep(0.2)
        if error > 0.25:
            print("Servo 4 off it's home angle")
        servo4.disable_torque()

    except:
        print("Servo 4 error during shutdown sequence")
        quit()