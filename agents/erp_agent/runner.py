from langchain_core.messages import ToolMessage
from tools.register_tools import llm_with_tools, tools


class AgentRunner:
    def __init__(self, llm, memory, prompt, langfuse_handler=None):
        self.llm = llm
        self.memory = memory
        self.prompt = prompt
        self.langfuse_handler = langfuse_handler

    def run(self, user_input, context):

        messages = self.prompt.format_messages(
            input=user_input,
            chat_history=context["recent"]
        )

        response = self.llm.invoke(
            messages,
            config={"callbacks": [self.langfuse_handler]} if self.langfuse_handler else {}
        )

        if response.tool_calls:
            tool_results = []

            for call in response.tool_calls:
                tool = next((t for t in tools if t.name == call["name"]), None)

                if not tool:
                    raise ValueError(f"Tool not found: {call['name']}")

                try:
                    result = tool.invoke(call["args"])
                except Exception as e:
                    result = f"Tool failed: {str(e)}"

                tool_results.append((call, result))

            messages.append(response)

            for call, result in tool_results:
                messages.append(
                    ToolMessage(
                        tool_call_id=call["id"],
                        content=str(result)
                    )
                )

            final = self.llm.invoke(
                messages,
                config={"callbacks": [self.langfuse_handler]} if self.langfuse_handler else {}
            )

            return final.content

        return response.content