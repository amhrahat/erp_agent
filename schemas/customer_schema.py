from pydantic import BaseModel, Field

class InsertCustomerInput(BaseModel):
    customer_name: str = Field(..., description="Customer name")
    customer_type: str = Field(..., description="Company or Individual or Patnership")
    website: str = Field(..., description="Customer website")