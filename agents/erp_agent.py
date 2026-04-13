from langchain_core.messages import HumanMessage, ToolMessage
import os
from dotenv import load_dotenv
from tools.register_tools import llm_with_tools, tools
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_BASE_URL")
)


langfuse_handler = CallbackHandler()

prompt = ChatPromptTemplate([
    ("system", """You are an ERPNext assistant.

Rules:
- ALWAYS use tools for database operations (create, update, delete, fetch)
- NEVER assume success without tool confirmation
- If tool fails, explain the error clearly
- Return concise, structured responses
- Do not hallucinate data

Output format:
- Success: short confirmation + key fields
- Failure: error reason
"""),
    ("human", "{input}")
])

def run_agent(user_input: str):

    messages = prompt.format_messages(input=user_input)


    response = llm_with_tools.invoke(
        messages,
        config={"callbacks": [langfuse_handler]}
    )

    if response.tool_calls:
        results = []

        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            selected_tool = next(
                (t for t in tools if t.name == tool_name),
                None
            )

            if not selected_tool:
                raise ValueError(f"Tool '{tool_name}' not found")

            try:
                result = selected_tool.invoke(tool_args)
            except Exception as e:
                result = f"Tool execution failed: {str(e)}"

            results.append((tool_call, result))


        messages.append(response)

        for tool_call, result in results:
            messages.append(
                ToolMessage(
                    tool_call_id=tool_call["id"],
                    content=str(result)
                )
            )


        final_response = llm_with_tools.invoke(
            messages,
            config={"callbacks": [langfuse_handler]}
        )

        return final_response.content

    return response.content



output = run_agent(
    "Insert a new customer named 'Rahat6' website 'https://testabc.com'"
)

print(output)

