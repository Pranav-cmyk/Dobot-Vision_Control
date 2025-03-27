from pyfirmata2 import Arduino
from utilities  import move_servo

try:
    board = Arduino('COM7')
    SERVO_PIN = board.get_pin('d:3:s')
    print("Servo is connected")
except Exception as e:
    print(e)
    print("Please check the connection")
    

move_servo(SERVO_PIN, 0)

board.exit()