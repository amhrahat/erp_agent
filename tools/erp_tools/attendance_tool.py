from erp.frappe_client import erp
from schemas.attendance_schema import AttendanceQueryInput
from langchain_core.tools import StructuredTool

def get_attendance(
    employee=None,
    status=None,
    from_date=None,
    to_date=None,
    limit=20
):
    filters = []

    if employee:
        filters.append(["employee", "=", employee])

    if status:
        filters.append(["status", "=", status])

    if from_date and to_date:
        filters.append(["attendance_date", "between", [from_date, to_date]])

    return erp.get_attendance_list(
        filters=filters,
        limit=limit
    )

get_attendance_tool = StructuredTool.from_function(
    func=get_attendance,
    name="get_attendance",
    description="Fetch attendance records (supports employee, status, date filters)",
    args_schema=AttendanceQueryInput
)