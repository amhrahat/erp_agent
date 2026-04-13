from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model
load_dotenv()

os.environ['GEMINI_API_KEY']


llm = init_chat_model(
    "gemini-3-flash-preview",
    model_provider="google_genai",
    temperature=0
)

# response = llm.invoke("hello")
# print(response)