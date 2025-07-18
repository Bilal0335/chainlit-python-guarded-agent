from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, set_tracing_disabled
from openai.types.responses import ResponseTextDeltaEvent
import os
from dotenv import load_dotenv
import chainlit as cl

# ✅ Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
set_tracing_disabled(disabled=True)

# ✅ Validate API Key
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set")

# ✅ Create external client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# ✅ Define model and config
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)
config = RunConfig(
    model=model,
    model_provider=external_client
)

# ✅ Define your Agent
agent = Agent(
    name="Frontend Developer",
    instructions="Write a simple frontend for a web application."
)

# ✅ Optional: Run once in terminal
res = Runner.run_sync(
    agent,
    input="Hello, how are you?",
    run_config=config
)
print(f"[Terminal] Assistant: {res.final_output}")

# ✅ Chainlit: On start
@cl.on_chat_start
async def chat_start():
    cl.user_session.set("history", [])
    await cl.Message(content="👋 Welcome to BilalCode! Ask me anything about frontend dev.").send()

@cl.on_message
async def handle_message(message: cl.Message):
    msg = cl.Message(content="⏳ Thinking...")
    await msg.send()

    history = cl.user_session.get("history") or []
    history.append({'role': 'user', 'content': message.content})

    # ⛔ Don't await here
    res = Runner.run_streamed(
        agent,
        input=message.content,
        run_config=config
    )

    final_response = ""

    # ✅ Stream tokens
    async for event in res.stream_events():
        if event.type == 'raw_response_event' and isinstance(event.data, ResponseTextDeltaEvent):
            delta = event.data.delta
            final_response += delta
            await msg.stream_token(delta)

    msg.content = final_response
    await msg.update()

    history.append({'role': 'assistant', 'content': final_response})
    cl.user_session.set("history", history)

    print(f"User: {message.content}")
    print(f"Assistant: {final_response}")


# ✅ Chainlit: On message
# @cl.on_message
# async def handle_message(message: cl.Message):
#     # ✅ Get user input
#     msg = cl.Message(content="Thinking...")
#     await msg.send()

#     history = cl.user_session.get("history") or []

#     # Save user message
#     history.append({'role': 'user', 'content': message.content})

#     # 🔁 Generate response
#     res = await Runner.run(
#         agent,
#         input=message.content,
#         run_config=config
#     )

#     async for event in res.stream_events():
#         if event.type == 'raw_response_event' and isinstance(event.data,ResponseTextDeltaEvent):
#             await msg.stream_token(event.data.delta)

#     # Save assistant reply
#     history.append({'role': 'assistant', 'content': res.final_output})
#     cl.user_session.set("history", history)

#     # ✅ Show in terminal and Chainlit UI
#     print(f"User: {message.content}")
#     print(f"Assistant: {res.final_output}")
#     await cl.Message(content=res.final_output).send()
print("-------------------------------")