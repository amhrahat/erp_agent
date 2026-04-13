import os
from dotenv import load_dotenv

from langfuse import Langfuse
from langfuse.langchain import CallbackHandler

from tools.register_tools import llm_with_tools
from llms.ollama_client import llm
from llms.gemini_client import gemini_llm

from agents.erp_agent.memory import MemoryManager
from agents.erp_agent.prompt import build_prompt
from agents.erp_agent.runner import AgentRunner
from agents.summary_agent.summary_agent import generate_summary
     
load_dotenv()

Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_BASE_URL")
)

langfuse_handler = CallbackHandler()


memory = MemoryManager()
prompt = build_prompt()

agent = AgentRunner(
    llm=llm_with_tools,
    memory=memory,
    prompt=prompt,
    langfuse_handler=langfuse_handler
)

summary_path = "storage/summary.txt"

prev_summary = ""
if os.path.exists(summary_path):
    with open(summary_path, "r") as f:
        prev_summary = f.read()
summary_llm = gemini_llm


while True:
    user_input = input("Enter request (exit to quit): ")

    if user_input.lower() == "exit":
        break

    context = memory.get_context(user_input)
    print("Context retrieved. Running agent...")
    print("Context:", context)

    output = agent.run(user_input, context)

    memory.update(user_input, output)

    if memory.needs_summary():
        combined_input = f"""
        Previous summary:
        {prev_summary}

        New conversation:
        {memory.chat_history}
"""
  
        summary = generate_summary(summary_llm, memory.chat_history)

        os.makedirs("storage", exist_ok=True)
        with open("storage/summary.txt", "w") as f:
            f.write(summary)

        memory.trim_after_summary()

    print("\nResponse:")
    print(output)
    print("-" * 50)