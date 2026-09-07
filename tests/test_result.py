import unittest
from runtime.core.result import failure, success, validate_result


class ResultTests(unittest.TestCase):
    def test_success_has_canonical_shape(self):
        result = success("test.capability", run_id="run-1")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["artifacts"], [])
        self.assertIsNone(result["error"])
        self.assertEqual(validate_result(result), result)

    def test_failure_has_canonical_shape(self):
        error = {"kind": "ValidationError", "message": "bad input"}
        result = failure("test.capability", error, run_id="run-1")
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["error"], error)
        self.assertEqual(validate_result(result), result)

    def test_missing_field_fails(self):
        with self.assertRaises(ValueError):
            validate_result({"status": "success"})

    def test_invalid_success_error_fails(self):
        result = success("test.capability")
        result["error"] = {"kind": "Error"}
        with self.assertRaises(ValueError):
            validate_result(result)


if __name__ == "__main__":
    unittest.main()
