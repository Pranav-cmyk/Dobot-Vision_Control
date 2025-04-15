from livekit.agents.llm import FunctionContext, ai_callable, TypeInfo
from typing import Annotated
from pyfirmata2 import Arduino
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)



class AssistantFunctions(FunctionContext):
    
    def __init__(self):
        
        logger.info('Initializing AssistantFunctions')

        super().__init__()
        try:
            self.board = Arduino('COM7')
            self.IN1 = self.board.get_pin('d:2:o')
            self.IN2 = self.board.get_pin('d:4:o')
            self.IN3 = self.board.get_pin('d:7:o')
            self.IN4 = self.board.get_pin('d:8:o')


            self.ENA = self.board.get_pin('d:3:p')
            self.ENB = self.board.get_pin('d:5:p')
        except Exception as e:
            logger.error(f'Error initializing AssistantFunctions: {e}')
        
        logger.info('AssistantFunctions initialized successfully')
        
    @ai_callable(
        description = """
        Moves the robot forward, 
        Call this function when the user wants to move the robot forward with a specific speed and duration,
        the speed can be either low, moderate or high where low is 15, moderate is 25 and high is 50.
        The delay is the time the robot should move forward for which must be in seconds greater than 0.
        """,
    )
    def forward(
        self,
        speed: Annotated[int, TypeInfo(description = 'The speed of the robot')],
        delay: Annotated[float, TypeInfo(description = 'The time the robot should move for')]
    ):
        self.ENA.write(speed)
        self.ENB.write(speed)

        self.IN1.write(1)
        self.IN2.write(0)

        self.IN3.write(0)
        self.IN4.write(1)
        time.sleep(delay)
        self.stop()
        
    @ai_callable(
        description = """
        Moves the robot backward, 
        Call this function when the user wants to move the robot backward with a specific speed and duration,
        the speed can be either low, moderate or high where low is 15, moderate is 25 and high is 50.
        The delay is the time the robot should move forward for which must be in seconds greater than 0.
        """,
    )
    def backward(
        self,
        speed: Annotated[int, TypeInfo(description = 'The speed of the robot')],
        delay: Annotated[float, TypeInfo(description = 'The time the robot should move for')]
    ):
        self.ENA.write(speed)
        self.ENB.write(speed)

        self.IN1.write(0)
        self.IN2.write(1)

        self.IN3.write(1)
        self.IN4.write(0)
        time.sleep(delay)
        self.stop()
        
    
    def stop(
        self,
    ):
        self.ENA.write(0)
        self.ENB.write(0)