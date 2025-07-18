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

# 🛡️ Guardrail Wrapper (cleaned)
@input_guardrail
async def input_guardrail_wrapper(
    ctx: RunContextWrapper,
    _: Agent,  # ✅ underscore used for unused parameter
    input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    user_id = ctx.context.get("user_id", "unknown")
    history = ctx.context.get("chat_history", [])

    print(f"[Guardrail] Checking input from user: {user_id}")
    print(f"[Guardrail] Chat history length: {len(history)}")

    res = await Runner.run(input_guardrails_agent, input, context=ctx.context)

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
    cl.user_session.set("history", [])  # reset chat history
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
        # Load chat history
        history = cl.user_session.get("history") or []
        history.append({"role": "user", "content": message.content})
        cl.user_session.set("history", history)

        # Prepare context
        context = {
            "user_id": message.author,
            "message_id": message.id,
            "chat_history": history
        }

        # Run main agent with context
        result = await Runner.run(main_agent, message.content, context=context)

        # Add assistant reply to history
        history.append({"role": "assistant", "content": str(result.final_output)})
        cl.user_session.set("history", history)

        await cl.Message(
            content=f"✅ Here's the Python code:\n```python\n{result.final_output}\n```"
        ).send()

    except InputGuardrailTripwireTriggered as e:
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
