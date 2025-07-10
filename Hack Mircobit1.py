import music
DELAY_VALUE =100
while True:
    x = accelerometer.get_x() # gets accelerometers value of x 
    print(x)           
    sleep(DELAY_VALUE)
    
    if button_a.was_pressed() or button_b.was_pressed(): # if one of buttons pressed
        print(3000)