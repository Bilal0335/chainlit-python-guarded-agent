# from agents import (
#     Agent, Runner, OpenAIChatCompletionsModel,
#     input_guardrail, RunContextWrapper,
#     TResponseInputItem, GuardrailFunctionOutput,
#     set_tracing_disabled
# )
# from openai import AsyncOpenAI
# from dotenv import load_dotenv
# from pydantic import BaseModel
# import chainlit as cl
# import os

# # Disable tracing
# set_tracing_disabled(disabled=True)

# # Load environment variables
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# if not GEMINI_API_KEY:
#     raise ValueError("GEMINI_API_KEY is not set")

# # External OpenAI-compatible client (for Gemini)
# external_client = AsyncOpenAI(
#     api_key=GEMINI_API_KEY,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# # Define the model using Gemini via OpenAI wrapper
# model = OpenAIChatCompletionsModel(
#     model="gemini-2.5-flash",
#     openai_client=external_client
# )

# # Define output schema
# class OutputPython(BaseModel):
#     is_python_related: bool
#     resoning: str  # You had a typo here; it's better as 'reasoning'

# # Input guardrail agent
# input_guardrails_agent = Agent(
#     name="Input Guardrails Agent",
#     instructions="Check if the input is a valid Python code snippet. If it is, return True and the reasoning. Otherwise, return False and the reasoning.",
#     model=model,
#     output_type=OutputPython
# )

# # Guardrail wrapper
# @input_guardrail
# async def input_guardrail_wrapper(
#     ctx: RunContextWrapper,
#     agent: Agent,
#     input: str | list[TResponseInputItem]
# ) -> GuardrailFunctionOutput:
#     res = await Runner.run(input_guardrails_agent, input)
#     return GuardrailFunctionOutput(
#         output_info=res.final_output,
#         tripwire_triggered=not res.final_output.is_python_related
#     )

# # Main agent with input guardrail
# main_agent = Agent(
#     name="Main Python Code Generator",
#     instructions="You are a Python code generator. Generate Python code based on the input provided.",
#     model=model,
#     input_guardrails=[input_guardrail_wrapper]
# )

# # Chainlit start event
# @cl.on_chat_start
# async def on_chat_start():
#     await cl.Message(
#         content="👋 Welcome to the Python Code Generator! Please provide your input."
#     ).send()

# # Chainlit message handler
# @cl.on_message
# async def on_message(message: cl.Message):
#     result = await Runner.run(main_agent, message.content)

#     await cl.Message(
#         content=f"✅ Generated Python code:\n```\n{result.final_output}\n```"
#     ).send()





# from agents import (
#     Agent, Runner, OpenAIChatCompletionsModel,
#     input_guardrail, RunContextWrapper,
#     TResponseInputItem, GuardrailFunctionOutput,
#     set_tracing_disabled
# )
# from agents.exceptions import InputGuardrailTripwireTriggered
# from openai import AsyncOpenAI
# from dotenv import load_dotenv
# from pydantic import BaseModel
# import chainlit as cl
# import os

# # Disable tracing
# set_tracing_disabled(disabled=True)

# # Load environment variables
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# if not GEMINI_API_KEY:
#     raise ValueError("GEMINI_API_KEY is not set")

# # Gemini API client using OpenAI wrapper
# external_client = AsyncOpenAI(
#     api_key=GEMINI_API_KEY,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# # Model definition
# model = OpenAIChatCompletionsModel(
#     model="gemini-2.5-flash",
#     openai_client=external_client
# )

# # Output schema
# class OutputPython(BaseModel):
#     is_python_related: bool
#     resoning: str  # Corrected typo (resoning → reasoning)

# # Input guardrail agent
# input_guardrails_agent = Agent(
#     name="input Guardrails Agent",
#     instructions="Check if the input is a valid Python code snippet. If it is, return True and the reasoning. Otherwise, return False and the reasoning.",
#     model=model,
#     output_type=OutputPython
# )

# # Guardrail wrapper
# @input_guardrail
# async def input_guardrail_wrapper(
#     ctx: RunContextWrapper,
#     agent: Agent,
#     input: str | list[TResponseInputItem]
# ) -> GuardrailFunctionOutput:
#     res = await Runner.run(input_guardrails_agent, input)
#     return GuardrailFunctionOutput(
#         output_info=res.final_output,
#         tripwire_triggered=not res.final_output.is_python_related
#     )

# # Main agent
# main_agent = Agent(
#     name="main agent",
#     instructions="You are a Python code generator. Generate Python code based on the input provided.",
#     model=model,
#     input_guardrails=[input_guardrail_wrapper]
# )

# # Chainlit chat start
# @cl.on_chat_start
# async def on_chat_start():
#     await cl.Message(
#         content="Welcome to the Python Code Generator! Please provide your input."
#     ).send()

# # Chainlit message handler with fixed error handling
# @cl.on_message
# async def on_message(message: cl.Message):
#     try:
#         result = await Runner.run(main_agent, message.content)
#         await cl.Message(
#             content=f"✅ Generated Python code:\n```\n{result.final_output}\n```"
#         ).send()

#     except InputGuardrailTripwireTriggered as e:
#         # Show friendly message if guardrail blocks input
#         reason = getattr(e.result.output_info, "resoning", "Input is not Python-related.")
#         await cl.Message(
#             content=f"❌ Your input was rejected by the Python guardrail.\n\n**Reason:** {reason}"
#         ).send()



# from agents import (
#     Agent, Runner, OpenAIChatCompletionsModel,
#     input_guardrail, RunContextWrapper,
#     TResponseInputItem, GuardrailFunctionOutput,
#     set_tracing_disabled
# )
# from agents.exceptions import InputGuardrailTripwireTriggered
# from openai import AsyncOpenAI
# from dotenv import load_dotenv
# from pydantic import BaseModel
# import chainlit as cl
# import os

# # 🔧 Disable tracing for agents (optional)
# set_tracing_disabled(disabled=True)

# # 🔑 Load environment variables
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# if not GEMINI_API_KEY:
#     raise ValueError("GEMINI_API_KEY is not set")

# # 🌐 Setup Gemini client using OpenAI wrapper format
# external_client = AsyncOpenAI(
#     api_key=GEMINI_API_KEY,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# # 🤖 Gemini model definition
# model = OpenAIChatCompletionsModel(
#     model="gemini-2.5-flash",
#     openai_client=external_client
# )

# # ✅ Guardrail Output Schema
# class OutputPython(BaseModel):
#     is_python_related: bool
#     reasoning: str  # fixed typo

# # 🛡️ Guardrail Agent
# input_guardrails_agent = Agent(
#     name="Input Guardrails Agent",
#     instructions="Check if the input is a valid Python code snippet or related to Python programming. If yes, return True and a reasoning. Otherwise, return False and the reason.",
#     model=model,
#     output_type=OutputPython
# )

# # 🛡️ Guardrail Function Wrapper
# @input_guardrail
# async def input_guardrail_wrapper(
#     ctx: RunContextWrapper,
#     agent: Agent,
#     input: str | list[TResponseInputItem]
# ) -> GuardrailFunctionOutput:
#     res = await Runner.run(input_guardrails_agent, input)
#     return GuardrailFunctionOutput(
#         output_info=res.final_output,
#         tripwire_triggered=not res.final_output.is_python_related
#     )

# # 🧠 Main Agent with Guardrail
# main_agent = Agent(
#     name="Main Python Code Generator",
#     instructions="You are a Python code generator. Generate Python code based on the input provided.",
#     model=model,
#     input_guardrails=[input_guardrail_wrapper]
# )

# # 🔄 On Chat Start
# @cl.on_chat_start
# async def on_chat_start():
#     await cl.Message(
#         content="👋 Welcome to the Python Code Generator! Please provide your input."
#     ).send()

# # 💬 On User Message
# @cl.on_message
# async def on_message(message: cl.Message):
#     try:
#         result = await Runner.run(main_agent, message.content)
#         await cl.Message(
#             content=f"✅ Generated Python code:\n```python\n{result.final_output}\n```"
#         ).send()

#     except InputGuardrailTripwireTriggered as e:
#         # Handle input rejection gracefully
#         reason = getattr(e.output_info, "reasoning", "Input is not Python-related.")
#         await cl.Message(
#             content=f"❌ Input rejected by guardrail.\n\n**Reason:** {reason}"
#         ).send()




# from agents import (
#     Agent, Runner, OpenAIChatCompletionsModel,
#     input_guardrail, RunContextWrapper,
#     TResponseInputItem, GuardrailFunctionOutput,
#     set_tracing_disabled
# )
# from agents.exceptions import InputGuardrailTripwireTriggered
# from openai import AsyncOpenAI
# from dotenv import load_dotenv
# from pydantic import BaseModel
# import chainlit as cl
# import os

# # 🔧 Disable tracing for agents
# set_tracing_disabled(disabled=True)

# # 🔑 Load environment variables
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# if not GEMINI_API_KEY:
#     raise ValueError("GEMINI_API_KEY is not set")

# # 🌐 Setup Gemini client
# external_client = AsyncOpenAI(
#     api_key=GEMINI_API_KEY,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# # 🤖 Define model
# model = OpenAIChatCompletionsModel(
#     model="gemini-2.5-flash",
#     openai_client=external_client
# )

# # ✅ Guardrail output schema
# class OutputPython(BaseModel):
#     is_python_related: bool
#     reasoning: str

# # 🛡️ Guardrail agent
# input_guardrails_agent = Agent(
#     name="Input Guardrails Agent",
#     instructions="Check if the input is a valid Python code snippet or related to Python programming. If yes, return True and a reasoning. Otherwise, return False and the reason.",
#     model=model,
#     output_type=OutputPython
# )

# # 🛡️ Guardrail wrapper function
# @input_guardrail
# async def input_guardrail_wrapper(
#     ctx: RunContextWrapper,
#     agent: Agent,
#     input: str | list[TResponseInputItem]
# ) -> GuardrailFunctionOutput:
#     res = await Runner.run(input_guardrails_agent, input)
#     return GuardrailFunctionOutput(
#         output_info=res.final_output,
#         tripwire_triggered=not res.final_output.is_python_related
#     )

# # 🧠 Main agent
# main_agent = Agent(
#     name="Main Python Code Generator",
#     instructions="You are a Python code generator. Generate Python code based on the input provided.",
#     model=model,
#     input_guardrails=[input_guardrail_wrapper]
# )

# # 🔄 On chat start
# @cl.on_chat_start
# async def on_chat_start():
#     await cl.Message(
#         content="👋 Welcome to the Python Code Generator! Please provide your input."
#     ).send()

# # 💬 On message
# @cl.on_message
# async def on_message(message: cl.Message):
#     try:
#         result = await Runner.run(main_agent, message.content)
#         await cl.Message(
#             content=f"✅ Generated Python code:\n```python\n{result.final_output}\n```"
#         ).send()

#     except InputGuardrailTripwireTriggered as e:
#         # 🛡️ Friendly rejection response
#         try:
#             reason = getattr(e.output_info, "reasoning", None)
#             if not reason:
#                 reason = "This input doesn't seem to be related to Python programming."
#         except Exception:
#             reason = "Your input was rejected by the Python relevance guardrail."

#         await cl.Message(
#             content=(
#                 f"❌ **Input rejected.**\n\n"
#                 f"🛡️ **Reason:** {reason}\n\n"
#                 f"💡 Try asking something like:\n"
#                 f"- 'Write a Python function to calculate factorial'\n"
#                 f"- 'Explain how decorators work in Python'\n"
#                 f"- 'Generate Python code for a to-do app'"
#             )
#         ).send()
















from agents import (
    Agent, Runner, OpenAIChatCompletionsModel,
    input_guardrail, RunContextWrapper,
    TResponseInputItem, GuardrailFunctionOutput,
    set_tracing_disabled
)
from agents.exceptions import InputGuardrailTripwireTriggered
from openai import AsyncOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
import chainlit as cl
import os

# 🔧 Disable tracing
set_tracing_disabled(disabled=True)

# 🔑 Load env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set")

# 🌐 Setup Gemini client
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# 🤖 Model setup
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

# ✅ Output schema for guardrail
class OutputPython(BaseModel):
    is_python_related: bool
    reasoning: str

# 🛡️ Guardrail Agent
input_guardrails_agent = Agent(
    name="Input Guardrails Agent",
    instructions="Check if the input is a valid Python code snippet or related to Python programming. If yes, return True and a reasoning. Otherwise, return False and the reason.",
    model=model,
    output_type=OutputPython
)

# 🛡️ Guardrail Wrapper
@input_guardrail
async def input_guardrail_wrapper(
    ctx: RunContextWrapper,
    agent: Agent,
    input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    res = await Runner.run(input_guardrails_agent, input)
    return GuardrailFunctionOutput(
        output_info=res.final_output,
        tripwire_triggered=not res.final_output.is_python_related
    )

# 🧠 Main Agent
main_agent = Agent(
    name="Main Python Code Generator",
    instructions="You are a Python code generator. Generate Python code based on the input provided.",
    model=model,
    input_guardrails=[input_guardrail_wrapper]
)

# 🔄 Chat Start
@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content=(
            "👋 Welcome! I’m your Python Code Assistant. 🐍\n\n"
            "You can ask me to generate Python code, explain Python concepts, or solve Python-related problems.\n\n"
            "💬 Try something like:\n"
            "• 'Write a Python function to reverse a string'\n"
            "• 'How do list comprehensions work in Python?'\n"
            "• 'Generate Python code for a calculator app'"
        )
    ).send()

# 💬 On Message
@cl.on_message
async def on_message(message: cl.Message):
    try:
        result = await Runner.run(main_agent, message.content)
        await cl.Message(
            content=f"✅ Here's the Python code:\n```python\n{result.final_output}\n```"
        ).send()

    except InputGuardrailTripwireTriggered as e:
        # Friendly non-technical rejection message
        try:
            reason = getattr(e.output_info, "reasoning", None)
            if not reason:
                reason = "Your message doesn't seem to be about Python programming."
        except Exception:
            reason = "That doesn't seem related to Python programming."

        await cl.Message(
            content=(
                f"❌ Sorry, I can only help with Python programming topics.\n\n"
                f"🧐 {reason}\n\n"
                f"💡 Try asking something like:\n"
                f"• 'Write a Python function to calculate factorial'\n"
                f"• 'Explain how decorators work in Python'\n"
                f"• 'Generate Python code for a to-do app'"
            )
        ).send()
