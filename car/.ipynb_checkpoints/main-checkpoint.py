import sys
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
from adafruit_motor import motor
from controller import PS4Controller
#import camera

#init controller
ps4 = PS4Controller()

#init i2c
i2c = busio.I2C(SCL, SDA)

#init PCA
pca = PCA9685(i2c)
pca.frequency = 50

servo_steer = servo.Servo(pca.channels[0])
esc = servo.ContinuousServo(pca.channels[1])

def scale_servo(x):
    y = round((30-70)*x+1/1+1+70,2) #used to scale -1,1 to 0,180
    return y

def scale_esc(x):
    y = round((x+1)/8,2) #used to scale -1,1 to 0,180
    return y
    
def drive(axis_data):
    servo_steer.angle = scale_servo(axis_data[0])
    sum_inputs = round(-scale_esc(axis_data[4]) + scale_esc(axis_data[3]),2)
    esc.throttle = sum_inputs
    #print(sum_inputs)

def toggle(x):
    return not x

#init vars
train = False
trig = True

#init Camera
#camera = Camera.instance(width=224, height=224)

try:
    while True:
        button_data, axis_data, hat_data = ps4.listen()
        
        if button_data[1] == True and trig:
            train = toggle(train)
            trig = False
            print(train)
        elif button_data[1] == False:
            trig = True
        else:
            pass
        
        if train:
            print('Training Mode!')
            drive(axis_data)
            csave_camera
        else:
            print('Auto Pilot Mode!')
            


except KeyboardInterrupt:
        pca.deinit()
        sys.exit(0)
        
