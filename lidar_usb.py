from tfmini import TFmini
import os
import time
tf = TFmini('/dev/ttyUSB0', mode=TFmini.STD_MODE)
try:
    print('=' * 25)
    originalDistance = tf.read()
    setup_attempt = 1
    counter = 1
    for counter in range (10000000):
        print("Attempt="+str(counter)+"\n")
        counter = counter - 1
        currentdistance = tf.read()
        if currentdistance:
            print('Distance: ' + str(currentdistance))
        else:
            print('Object too close')
            continue
        time.sleep(0.25)

        if counter % 120 == 0 and setup_attempt <= 3:
            setup_attempt = setup_attempt + 1
            originalDistance = currentdistance
            print("Resetting base value")
            os.system("sudo python3 /home/pi/curva/lightup_gpio21_green.py")
        difference = abs(currentdistance - originalDistance)
        print("difference="+str(difference))
        tolerance = 0.02
        if difference > tolerance:
            print ("Object detected, time to light up.")
            os.system("sudo python3 /home/pi/curva/lightup_gpio21_red.py")
        else:
            print ("Object not detected, lights off")
            os.system("sudo python3 /home/pi/curva/clear_leds_gpio21.py")
except KeyboardInterrupt:
    tf.close()
    print("Contol-C Pressed. Closed lidar and exiting.")
