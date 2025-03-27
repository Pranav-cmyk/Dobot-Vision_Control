import logging
from dotenv import load_dotenv
from livekit.agents import(
    AutoSubscribe, JobContext, WorkerOptions, WorkerType,
    cli, multimodal
)
from livekit.plugins import google
from assistant_functions import AssistantFunctions


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
            max_output_tokens=150,
            top_k=50,
            top_p=0.9,
            instructions="You are a Capable and helpful Vision based assistant, You are to begin the conversation by welcoming the user in a friendly way",
        ),
        fnc_ctx=AssistantFunctions()
    )
    
    agent.start(ctx.room, participant)
    agent.generate_reply()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, worker_type=WorkerType.ROOM))
    