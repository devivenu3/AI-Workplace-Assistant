
import unittest

from workplace_tools import (
    get_leave_balance,
    check_calendar,
    submit_leave_request,
    approve_leave_request,
)


class TestWorkplaceTools(unittest.TestCase):

    def test_valid_employee_leave_balance(self):
        result = get_leave_balance("EMP001")
        self.assertIn("12 days", result)

    def test_invalid_employee_leave_balance(self):
        result = get_leave_balance("EMP999")
        self.assertEqual(result, "Employee not found.")

    def test_calendar_with_meetings(self):
        result = check_calendar("EMP001", "2026-10-02")
        self.assertIn("Team Stand-up", result)
        self.assertIn("Project Review", result)

    def test_calendar_unknown_employee(self):
        result = check_calendar("EMP999", "2026-10-02")
        self.assertEqual(result, "Employee calendar not found.")

    def test_leave_request_prepared(self):
        result = submit_leave_request(
            "EMP001", "2026-10-05", "Testing"
        )
        self.assertTrue(result["success"])
        self.assertEqual(
            result["request"]["status"], "PENDING_APPROVAL"
        )

    def test_invalid_employee_leave_request(self):
        result = submit_leave_request(
            "EMP999", "2026-10-05", "Testing"
        )
        self.assertFalse(result["success"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
