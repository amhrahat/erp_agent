import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel
load_dotenv()



def get_llm_instance() -> BaseChatModel:
    return init_chat_model(
        model="qwen3.5:4b",
        model_provider="ollama",
        temperature=0,
        base_url=os.getenv('OLLAMA_URL'),
        extra_body={
            "options": {
                "num_ctx": 16384
            }
        }
    )


llm = get_llm_instance()
# response = llm.invoke("hello")
# print(response.content)