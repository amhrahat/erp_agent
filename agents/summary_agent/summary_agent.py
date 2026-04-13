def generate_summary(llm, chat_history):
    text = "\n".join(
        f"{type(m).__name__}: {m.content}"
        for m in chat_history
    )

    prompt = f"""
You are maintaining a running summary of a conversation.

Update the previous summary using the new messages.

Rules:
- Keep it concise
- Preserve important facts, decisions, and entities
- Remove redundancy
- Do NOT repeat information
- Output a clean updated summary only
- If the new messages do not add anything important, return the previous summary without changes
- Do not include any information that is not in the messages
- If the messages contain contradictory information, prioritize the most recent ones
- Always return a summary, even if it's the same as before
- Do not include any formatting, just plain text

Conversation:
{text}
"""

    return llm.invoke(prompt).content