from langchain_core.messages import HumanMessage, AIMessage
import json
import os

HISTORY_FILE = "storage/chat_history.json"
SUMMARY_FILE = "storage/summary.txt"


class MemoryManager:
    def __init__(self):
        self.chat_history = []
        self.load()


    def load(self):
        if not os.path.exists(HISTORY_FILE):
            return

        try:
            with open(HISTORY_FILE, "r") as f:
                content = f.read().strip()
                if not content:
                    return
                data = json.loads(content)

            for msg in data:
                if msg["type"] == "human":
                    self.chat_history.append(HumanMessage(content=msg["content"]))
                else:
                    self.chat_history.append(AIMessage(content=msg["content"]))
        except (json.JSONDecodeError, ValueError):

            return


    def save(self):
        os.makedirs("storage", exist_ok=True)

        data = [
            {
                "type": "human" if isinstance(m, HumanMessage) else "ai",
                "content": m.content
            }
            for m in self.chat_history
        ]

        with open(HISTORY_FILE, "w") as f:
            json.dump(data, f, indent=2)


    def get_context(self, user_input: str):
        recent = self.chat_history[-8:]

        summary = ""
        if os.path.exists(SUMMARY_FILE):
            with open(SUMMARY_FILE, "r") as f:
                summary = f.read()

        return {
            "recent": recent,
            "summary": summary
        }


    def update(self, user_input: str, ai_output: str):
        self.chat_history.append(HumanMessage(content=user_input))
        self.chat_history.append(AIMessage(content=ai_output))

        self.save()

    def needs_summary(self, threshold=8):
        return len(self.chat_history) >= threshold

    def trim_after_summary(self, keep_last=5):
        self.chat_history = self.chat_history[-keep_last:]
        self.save()