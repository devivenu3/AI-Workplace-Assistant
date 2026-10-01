
# Sample employee data for our project
employees = {
    "EMP001": {
        "name": "Alex",
        "leave_balance": 12
    },
    "EMP002": {
        "name": "Sam",
        "leave_balance": 8
    }
}


def get_leave_balance(employee_id):
    """Return an employee's remaining leave balance."""

    employee = employees.get(employee_id)

    if employee is None:
        return "Employee not found."

    return (
        f"{employee['name']} has "
        f"{employee['leave_balance']} days of leave remaining."
    )

# Sample calendar data for our project
calendar = {
    "EMP001": [
        {
            "date": "2026-10-02",
            "time": "10:00 AM",
            "meeting": "Team Stand-up"
        },
        {
            "date": "2026-10-02",
            "time": "2:00 PM",
            "meeting": "Project Review"
        }
    ],
    "EMP002": [
        {
            "date": "2026-10-02",
            "time": "11:00 AM",
            "meeting": "Client Meeting"
        }
    ]
}


def check_calendar(employee_id, date):
    """Return an employee's meetings for a given date."""

    if employee_id not in calendar:
        return "Employee calendar not found."

    meetings = [
        meeting for meeting in calendar[employee_id]
        if meeting["date"] == date
    ]

    if not meetings:
        return f"No meetings found for {employee_id} on {date}."

    result = f"Meetings for {employee_id} on {date}:\n"

    for meeting in meetings:
        result += (
            f"- {meeting['time']}: {meeting['meeting']}\n"
        )

    return result.strip()

# Store submitted leave requests (mock data)
leave_requests = []


def submit_leave_request(employee_id, date, reason):
    """Prepare a leave request for human approval."""

    if employee_id not in employees:
        return {
            "success": False,
            "message": "Employee not found."
        }

    request = {
        "employee_id": employee_id,
        "date": date,
        "reason": reason,
        "status": "PENDING_APPROVAL"
    }

    leave_requests.append(request)

    return {
        "success": True,
        "message": "Leave request prepared for approval.",
        "request": request
    }


def approve_leave_request(request_index):
    """Approve a pending leave request."""

    if request_index < 0 or request_index >= len(leave_requests):
        return "Request not found."

    request = leave_requests[request_index]

    if request["status"] != "PENDING_APPROVAL":
        return "This request is not pending approval."

    request["status"] = "APPROVED"

    return (
        f"Leave request for {request['employee_id']} "
        f"on {request['date']} has been approved."
    )


# Test the tool
if __name__ == "__main__":
    print(get_leave_balance("EMP001"))
    print(get_leave_balance("EMP002"))
    print(get_leave_balance("EMP999"))
