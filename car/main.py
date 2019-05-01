import sys
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
from adafruit_motor import motor
from controller import PS4Controller
import camera
import cv2
import csv
from uuid import uuid1

class Autocar():

    def __init__(self):
        #init i2c
        i2c = busio.I2C(SCL, SDA)

        #init PCA
        self.pca = PCA9685(i2c)
        self.pca.frequency = 50

        self.servo_steer = servo.Servo(self.pca.channels[0])
        self.esc = servo.ContinuousServo(self.pca.channels[1])

        #init vars

        self.temp = 0

        #init Camera
        self.cam = camera.Camera()        

        #initial content
        with open('control_data.csv','w') as f:
            f.write('date,steering,speed\n') # TRAILING NEWLINE
        
    def scale_servo(self, x):
        y = round((30-70)*x+1/1+1+70,2) #used to scale -1,1 to 0,180
        return y

    def scale_esc(self, x):
        y = round((x+1)/8,2) #used to scale -1,1 to 0,180
        return y
        
    def drive(self, axis_data):
        self.servo_steer.angle = self.scale_servo(-axis_data[0])
        sum_inputs = round(-self.scale_esc(axis_data[4]) + self.scale_esc(axis_data[3]),2)
        self.esc.throttle = sum_inputs

    def save_data(self, axis_data):
    
        count = self.cam.count
        img = self.cam.value

        if count!= self.temp:
            num = uuid1()
            cv2.imwrite('images/'+str(num)+".jpg", img)
            
            with open('control_data.csv','a',newline='') as f:
                writer=csv.writer(f)
                writer.writerow([num,axis_data[0],axis_data[4]])
            self.temp = count
            print('Save data!')
        else:
            pass
        

if __name__ == "__main__":

    car = Autocar()
    
    #init controller
    ps4 = PS4Controller()
    ps4.init()
    
    train = False
    trig = True
    
    def toggle(x):
        return not x
        
    try:
        while True:
        
            button_data, axis_data, hat_data = ps4.listen()
            
            if button_data[1] == True and trig:
                train = toggle(train)
                trig = False
                
            elif button_data[1] == False:
                trig = True
            else:
                pass
            
            if train:
                car.drive(axis_data)
                
                if axis_data[4] >= 0.12:
                    car.save_data(axis_data)
                else:
                    print('Not saving img')
            else:
                pass            


    except KeyboardInterrupt:
            car.pca.deinit()
            sys.exit(0)
        
