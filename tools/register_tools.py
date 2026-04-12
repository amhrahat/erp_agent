from langchain_core.tools import StructuredTool
from erp.frappe_client import erp
from schemas.customer_schema import InsertCustomerInput
from tools.erp_tools.customer_tools import insert_customer_tool
# from llms.ollama_client import llm
from llms.gemini_client import llm

tools = [insert_customer_tool]

llm_with_tools = llm.bind_tools(tools)