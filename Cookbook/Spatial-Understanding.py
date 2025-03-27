from utilities import get_response_from_camera, parse_json, output_to_joint_angle, move_servo
from dotenv import load_dotenv
from os import getenv
from google.genai import Client
from cv2 import VideoCapture
from pyfirmata2 import Arduino
from time import sleep
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

SYSTEM_INSTRUCTIONS = """

    Detect the position of the green cube.
    Output a json object with the following format:
    {
        "object": {
                "name": "object_name",
                "position": {
                    "x": 0.0,
                    "y": 0.0,
                    "z": 0.0
                }
            }
    }
    Ensure that the position values are in pixel coordinates relative to the top left corner of the image(Assume the top left corner is (0, 0, 0)).
    Let the z value determine the height of the object and x, y determine the plane of the base of the image. 

"""
load_dotenv()


try:
    logger.info('Initializing Client')
    client = Client(
        api_key=getenv('GOOGLE_API_KEY'),
        http_options={'api_version': 'v1alpha'}
        )
    logger.info('Initializing Camera')
    cap = VideoCapture(0)
    
    logger.info('Initializing Board')
    board = Arduino('COM7')
    SERVO_PIN = board.get_pin('d:3:s')
    
    logger.info('Client, Camera & Board Initialized')
    move_servo(SERVO_PIN, 0)
except Exception as e:
    print(e)


logger.info('Generating Response')
response = get_response_from_camera(
    client = client,
    cap = cap,
    prompt = SYSTEM_INSTRUCTIONS
)

logger.info('Parsing Response')
logger.info(parse_json(response))

angle = output_to_joint_angle(parse_json(response))
logger.info(f'Angle: {angle}')
move_servo(SERVO_PIN, angle)