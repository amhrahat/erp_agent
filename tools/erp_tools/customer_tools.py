from erp.frappe_client import erp
from schemas.customer_schema import InsertCustomerInput
from langchain_core.tools import StructuredTool


def insert_customer(
    customer_name: str,
    customer_type: str,
    website: str
):
    """
    Insert a customer into ERPNext with given details of customer name, type and website. 
    if type is not provided, default to "Company"
    """
    if not customer_type:
        customer_type = "Company"

    return erp.insert_customer(
        customer_name=customer_name,
        customer_type=customer_type,
        website=website
    )

insert_customer_tool = StructuredTool.from_function(
    func=insert_customer,
    name="insert_customer",
    description="Create a customer in ERPNext",
    args_schema=InsertCustomerInput
)
