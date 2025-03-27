from livekit.agents.llm import FunctionContext, ai_callable, TypeInfo
from utilities import DobotVision
from typing import Annotated
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)



class AssistantFunctions(FunctionContext):
    
    logger.info('Initializing AssistantFunctions')
    def __init__(self):
        super().__init__()
        self.video_utils = DobotVision(
            COM_PORT = 'COM9'
        )
        self.video_utils.__enter__()
        
        self.positions = self.video_utils.dobot.pose()
        
    logger.info('AssistantFunctions initialized successfully')
    @ai_callable(
        
        description = """

            This Method is used to get objects detected by the camera.
            Call this function whenever the user asks anything about what u can 'see' and if they ask to 'open the camera' 
            You are to use the json data returned by the function, summarize it and describe it in a natural way to the user.
            
        """
    )
    def get_objects(self):
        objects = self.video_utils.get_coords_from_camera()
        return f'Detected Objects: {objects}'
    
    
    @ai_callable(
        description = '''
        
        This function is used to move the robot to the position of the object detected by the camera.
        Call this function whenever the user asks to 'move the robot to the object detected by the camera'.
        
        '''
    )
    def move_robot_from_positions(self):
        objects = self.video_utils.get_coords_from_camera()
        robot_coords = self.video_utils.json_output_to_robot_coordinates(objects)
        
        x = robot_coords['Robot']['x']
        y = robot_coords['Robot']['y']
        z = robot_coords['Robot']['z']
        
        self.video_utils.dobot.move_to(
            x = x,
            y = y,
            z = z,
            r = 0,
            wait = True
        )
        
        return f'Moving robot to {x}, {y}, {z}'
        
    
    @ai_callable(
        description="""
        
        This function moves the robot to the specified joint angle or angles.
        Parameters:
        - base: The base angle of the robot
        - shoulder: The shoulder angle of the robot
        - elbow: The elbow angle of the
        - end_effector: The end-effector angle of the robot
        - end_effector_state: The end-effector state of the robot, this could be either True or False or  on or off
        
        Call this function whenever the user asks you to move the any of the robot's joints to a particular angle.
        if the user only specifies the end-effector state, Then keep the other angles as None.
        
        if the user only specifies one angle, then keep the other angles as None
        
        if the user asks u to move the robot back to it's 'home' position then move the robot's base angle to 1, shoulder angle to 1, elbow angle to 1 and end-effector angle to 1 and set the end_effector state to False
        
        """
    )
    def move_robot(
        self,
        
        base: Annotated[
            int, TypeInfo(description="The base angle of the robot"),
        ] = None,
        
        shoulder: Annotated[
            int, TypeInfo(description="The shoulder angle of the robot"),
        ] = None,
        
        elbow: Annotated[
            int, TypeInfo(description="The elbow angle of the robot"),
        ] = None,
        
        end_effector: Annotated[
            int, TypeInfo(description="The end-effector angle of the robot"),
        ] = None,
        
        end_effector_state: Annotated[
            bool, TypeInfo(description="The end-effector state of the robot, this could be either True or False"),
        ] = False
    ) -> str:
        """
        Called when the user asked to move the robot to a specific joint angle
        """
        logger.info(f"Moving robot to {base}, {shoulder}, {elbow}, {end_effector}")
        
        self.video_utils.dobot._set_ptp_cmd(
            base or self.positions[4],
            shoulder or self.positions[5],
            elbow or self.positions[6],
            end_effector or self.positions[7],
            mode = 4,
            wait = True
        )
        
        #Update the positions of the robot
        self.positions = self.video_utils.dobot.pose()
        logger.info(f"Robot moved to {self.positions}")
        
        if end_effector_state:
            self.video_utils.dobot.suck(True)
        else:
            self.video_utils.dobot.suck(False)
            
        return f"I've Moved the robot's Base: {base}, Shoulder: {shoulder}, elbow: {elbow}, end_effector: {end_effector}"