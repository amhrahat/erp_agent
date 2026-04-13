from frappeclient import FrappeClient
from typing import Dict, Any
from typing import List, Optional


class ERPClient:
    """
    Central ERP client wrapper.
    Add all ERPNext operations here.
    """

    # def __init__(self):
    #     self.client = FrappeClient("http://127.0.0.1:8000/")
    #     self.client.authenticate(
    #         "bf6b1fe25a100a0",
    #         "ac36014ba0481ea"
    #     )

    def __init__(self):
        self.client = FrappeClient("http://localhost:8080/")
        self.client.authenticate(
            "5906dcb71db097c",
            "573afe72f3bf7df"
        )


    def insert_customer(
        self,
        customer_name: str,
        customer_type: str,
        website: str
    ) -> Dict[str, Any]:
        doc = self.client.insert({
            "doctype": "Customer",
            "customer_name": customer_name,
            "customer_type": customer_type,
            "website": website
        })
        return doc
    

    def get_attendance_list(
            self,
            filters: Optional[List] = None,
            limit: int = 50,
            order_by: str = "creation desc"
        ) -> Dict[str, Any]:

            return self.client.get_list(
                doctype="Attendance",
                fields=["name", "employee", "attendance_date", "status"],
                filters=filters,
                limit_page_length=limit,
                order_by=order_by
            )

erp = ERPClient()


# result = erp.insert_customer(
#     customer_name="Test Customer ABC",
#     customer_type="Company",
#     website="https://testabc.com"
# )

# print("Inserted Customer Successfully:")
# print(result)