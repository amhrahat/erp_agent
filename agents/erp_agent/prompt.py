from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def build_prompt():
    return ChatPromptTemplate([
        ("system",
         """You are an ERPNext assistant.

Rules:
- ALWAYS use tools for database operations
- NEVER assume success without tool confirmation
- Return concise structured responses
- Do not hallucinate ERP data
"""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])