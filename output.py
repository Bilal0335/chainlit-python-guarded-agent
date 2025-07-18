from agents import (
    Agent, Runner, OpenAIChatCompletionsModel,
    input_guardrail, output_guardrail,
    RunContextWrapper, TResponseInputItem,
    GuardrailFunctionOutput, set_tracing_disabled
)
from agents.exceptions import InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
from openai import AsyncOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
import chainlit as cl
import os

# 🔧 Disable tracing
set_tracing_disabled(disabled=True)

# 🔑 Load environment variables
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

# ✅ Output schema for input guardrail
class OutputPython(BaseModel):
    is_python_related: bool
    reasoning: str

# 🛡️ Input Guardrail Agent
input_guardrails_agent = Agent(
    name="Input Guardrails Agent",
    instructions="Check if the input is a valid Python code snippet or related to Python programming. If yes, return True and a reasoning. Otherwise, return False and the reason.",
    model=model,
    output_type=OutputPython
)

# 🛡️ Input Guardrail Wrapper
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

# ✅ Output schema for output guardrail
class PythonOut(BaseModel):
    is_python: bool
    reasoning: str

class MessageOutput(BaseModel):
    response: str

# 🛡️ Output Guardrail Agent
output_guardrails_agent = Agent(
    name="Output Guardrails Agent",
    instructions="Check if the output includes any Python-related response. If yes, allow. Else block.",
    model=model,
    output_type=PythonOut
)

# 🛡️ Output Guardrail Wrapper
@output_guardrail
async def output_guardrail_wrapper(
    ctx: RunContextWrapper,
    agent: Agent,
    output: MessageOutput
) -> GuardrailFunctionOutput:
    out_res = await Runner.run(output_guardrails_agent, output)
    return GuardrailFunctionOutput(
        output_info=out_res.final_output,
        tripwire_triggered=not out_res.final_output.is_python
    )

# 🧠 Main Agent
main_agent = Agent(
    name="Main Python Code Generator",
    instructions="You are a Python code generator. Generate Python code based on the input provided.",
    model=model,
    input_guardrails=[input_guardrail_wrapper],
    output_guardrails=[output_guardrail_wrapper]
)

# 🔄 Chat Start Handler
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

# 💬 Message Handler
# @cl.on_message
# async def on_message(message: cl.Message):
#     try:
#         result = await Runner.run(main_agent, message.content)
#         await cl.Message(
#             content=f"✅ Here's the Python code:\n```python\n{result.final_output}\n```"
#         ).send()

#     except InputGuardrailTripwireTriggered as e:
#         reason = getattr(e.output_info, "reasoning", None) or "Your message doesn't seem to be about Python programming."
#         await cl.Message(
#             content=(
#                 f"❌ Sorry, I can only help with Python programming topics.\n\n"
#                 f"🧐 {reason}\n\n"
#                 f"💡 Try asking something like:\n"
#                 f"• 'Write a Python function to calculate factorial'\n"
#                 f"• 'Explain how decorators work in Python'\n"
#                 f"• 'Generate Python code for a to-do app'"
#             )
#         ).send()

#     except OutputGuardrailTripwireTriggered as e:
#         reason = getattr(e.output_info, "reasoning", None) or "The response doesn't seem to include Python-related output."
#         await cl.Message(
#             content=(
#                 f"❌ Response blocked by output guardrail.\n\n"
#                 f"🧐 {reason}\n\n"
#                 f"🔁 Please try rephrasing your request."
#             )
#         ).send()


@cl.on_message
async def on_message(message: cl.Message):
    try:
        result = await Runner.run(main_agent, message.content)

        code_output = result.final_output.strip()

        if code_output and any(keyword in code_output for keyword in ["def ", "import ", "class ", "print(", "="]):
            await cl.Message(
                content=f"✅ Here's the Python code:\n```python\n{code_output}\n```"
            ).send()
        else:
            await cl.Message(
                content="⚠️ The response did not include valid Python code. Try rephrasing your prompt."
            ).send()

    except InputGuardrailTripwireTriggered as e:
        reason = getattr(e.output_info, "reasoning", None) or "Your message doesn't seem to be about Python programming."
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

    except OutputGuardrailTripwireTriggered as e:
        reason = getattr(e.output_info, "reasoning", None) or "The response doesn't seem to include Python-related output."
        await cl.Message(
            content=(
                f"❌ Response blocked by output guardrail.\n\n"
                f"🧐 {reason}\n\n"
                f"🔁 Please try rephrasing your request."
            )
        ).send()
