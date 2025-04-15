import logging
from dotenv import load_dotenv
from livekit.agents import(
    AutoSubscribe, JobContext, WorkerOptions, WorkerType,
    cli, multimodal
)
from livekit.plugins import google
from src.assistant_functions import AssistantFunctions


load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def entrypoint(ctx: JobContext):
    logger.info("Starting entrypoint")
    
    
    await ctx.connect(auto_subscribe=AutoSubscribe.SUBSCRIBE_ALL)
    participant = await ctx.wait_for_participant()
    
    
    agent = multimodal.MultimodalAgent(
        model = google.beta.realtime.RealtimeModel(
            voice='Aoede',
            temperature=0.4,
            max_output_tokens=100,
            instructions="""
            
            You are a friendly and capable assistant with the ability to move a robot. Greet the user with a friendly tone
            
            """,
        ),
        fnc_ctx = AssistantFunctions(),
    )
    
    agent.start(ctx.room, participant)
    agent.generate_reply()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, worker_type=WorkerType.ROOM))
    