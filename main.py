print("Hello, Pi Pico W!")
#import libraries
from machine import Pin
import utime

from imu import MPU6050
import time
from machine import I2C

import network
import time
from machine import Pin
from umqttsimple import MQTTClient

# WiFi Network Parameters
# SSID: Wokwi-GUEST
# Security: Open
print("Connecting to WiFi", end="")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("Wokwi-GUEST", "")
while not wlan.isconnected():
  print(".", end="")
  time.sleep(0.1)
print(wlan.ifconfig())
print("WiFi Connected!")

# MQTT Server Parameters
MQTT_CLIENT_ID = "picow-01"
MQTT_BROKER    = "f7bad57596e34258bc8cde18b8b6474c.s2.eu.hivemq.cloud"
MQTT_USER      = "user2023"
MQTT_PASSWORD  = "Prog6002P@$$"
MQTT_TOPIC     = "wokwi"
print("Connecting to MQTT server... ", end="")
client = MQTTClient(client_id=MQTT_CLIENT_ID, 
server=MQTT_BROKER, user=MQTT_USER, 
password=MQTT_PASSWORD, 
keepalive=7200,
ssl=True,
ssl_params={'server_hostname':'f7bad57596e34258bc8cde18b8b6474c.s2.eu.hivemq.cloud'})



# The callback function
def sub_callback(topic, msg):
  print("Received: {}:{}".format(topic.decode(), msg.decode()))

client.set_callback(sub_callback)
client.connect()
client.subscribe(topic = MQTT_TOPIC)
print("MQTT Connected!")


i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
imu = MPU6050(i2c)

while True:
    # Following print shows original data get from libary. You can uncomment to see raw data
    #print(imu.accel.xyz,imu.gyro.xyz,imu.temperature,end='\r')
    
    # Following rows round values get for a more pretty print:
    ax=round(imu.accel.x,2)
    ay=round(imu.accel.y,2)
    az=round(imu.accel.z,2)
    gx=round(imu.gyro.x)
    gy=round(imu.gyro.y)
    gz=round(imu.gyro.z)
    tem=round(imu.temperature,2)
    print(ax,"\t",ay,"\t",az,"\t",gx,"\t",gy,"\t",gz,"\t",tem,"        ",end="\r")
    
    # Following sleep statement makes values enought stable to be seen and
    # read by a human from shell
    time.sleep(0.2)


#code for relay and lED
RELAY_CTRL_PIN =  16

def main():
    relay = Pin(RELAY_CTRL_PIN, Pin.OUT)
    while True:
        print("Led on")
        print("parking is available ")
        relay.high() #set the output pin to high level (1)
        utime.sleep(2.0)
        
        print("Led off")
        print("parking is unavailable ")
        relay.low() #set the output pin to low level (0)
        utime.sleep(2.0)

if __name__ == "__main__":
    main()


#code for ultrasonic sound sensor with raspberry pi pico w in micropython

trigger = Pin(26, Pin.OUT)
echo = Pin(27, Pin.IN)
def ultra():
        trigger.low()
        utime.sleep_us(2)
        trigger.high()
        utime.sleep_us(5)
        trigger.low()
while echo.value() ==0:
            signaloff = utime.ticks_us()
while echo.value() ==1:
      signalon = utime.ticks_us()
      timepassed = signalon-signaloff 
      distance = (timepassed * 0.0343) / 2
print("The distance from object is ",distance, "cm")
while True: 
       ultra()
       utime.sleep(1)



##code for PIR Motion sensor 
pir = Pin(0,Pin.IN)
while True:
    motion_state=pir.value()
    print(motion_state) #0 - no motion; 1 - there is motion
utime.sleep(1.0) 

from time import sleep
from servo import Servo

'''
from machine import Pin, PWM
pwm = PWM(Pin(27))
pwm.freq(50)

while True:
    for position in range(1000,9000,50):
        pwm.duty_u16(position)
        sleep(0.01)
    for position in range(9000,1000,-50):
        pwm.duty_u16(position)
        sleep(0.01)
'''

SERVO_CTRL_PIN = 27
sg90_servo = Servo(pin=SERVO_CTRL_PIN)
while True:
    sg90_servo.move(0)  # turns the servo to 0°.
    sleep(1)
    sg90_servo.move(90)  # turns the servo to 90°.
    sleep(1)
    