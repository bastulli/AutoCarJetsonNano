import sys
import torch
import torchvision
import numpy as np
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
import neural_network


class Autocar():

    def __init__(self):
        # init i2c
        i2c = busio.I2C(SCL, SDA)

        # init PCA
        self.pca = PCA9685(i2c)
        self.pca.frequency = 50

        self.servo_steer = servo.Servo(self.pca.channels[0])
        self.esc = servo.ContinuousServo(self.pca.channels[1])
        
        # init model
        
        model = neural_network.Net()
        for param in model.parameters():
            param.requires_grad = False
        self.model = model.eval()
        self.model.load_state_dict(torch.load('model/autopilot.pt'))
        self.device = torch.device('cuda')
        self.model.to(self.device)
        
        # init vars
        self.temp = 0
        mean = 255.0 * np.array([0.485, 0.456, 0.406])
        stdev = 255.0 * np.array([0.229, 0.224, 0.225])
        self.normalize = torchvision.transforms.Normalize(mean, stdev)
        self.angle_out = 0

        # init Camera
        self.cam = camera.Camera()        

        # initial content
        with open('control_data.csv','w') as f:
            f.write('date,steering,speed\n')
        
    def scale_servo(self, x):
    
        # used to scale -1,1 to 0,180
        y = round((30-70)*x+1/1+1+70,2) 
        
        return y

    def scale_esc(self, x):
    
        # used to scale -1,1 to 0,180
        y = round((x+1)/8,2)
        
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
            
            # append inputs to csv
            with open('control_data.csv','a',newline='') as f:
                writer=csv.writer(f)
                writer.writerow([num,axis_data[0],axis_data[4]])
                
            self.temp = count
            
            print('Save data!')
            
        else:
            pass
        
            
    def preprocess(self, camera_value):
    
        x = camera_value
        x = cv2.resize(x, (224, 224))
        x = cv2.cvtColor(x, cv2.COLOR_BGR2RGB)
        x = x.transpose((2, 0, 1))
        x = torch.from_numpy(x).float()
        x = self.normalize(x)
        x = x.to(self.device)
        x = x[None, ...]
        
        return x        
    
    def autopilot(self):
        
        img = self.preprocess(self.cam.value)
        count = self.cam.count
        
        if count!= self.temp:
            print('RUN!')
            output = self.model(img)
            _, angle_tensor = torch.max(output,1)
            angle = np.squeeze(angle_tensor)
            self.angle_out = angle[0].cpu().numpy()
            self.temp = count
            print(self.angle_out)
            
        else:
            pass
        
        self.drive({0:self.angle_out,1:0.0,2:0.0,3:-1.0,4:1,5:0.0})
        

if __name__ == "__main__":

    car = Autocar()
    
    # init controller
    ps4 = PS4Controller()
    ps4.init()
    
    # Start in training mode
    train = True
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
                car.autopilot()


    except KeyboardInterrupt:
            car.pca.deinit()
            sys.exit(0)
        
