import io
import json
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from runtime.__main__ import main


class CLIAccessTests(unittest.TestCase):
    def _run(self, argv):
        output = io.StringIO()
        with patch("sys.argv", ["python -m runtime", *argv]), redirect_stdout(output):
            with self.assertRaises(SystemExit) as exit_info:
                main()
        return exit_info.exception.code, output.getvalue()

    def test_execute_valid_request(self):
        result = {
            "status": "success",
            "capability": "media.save",
            "run_id": "run-1",
            "artifacts": [],
            "data": {},
            "error": None,
        }
        with patch("runtime.__main__.ExecutionEngine.execute", return_value=result) as execute:
            code, output = self._run([
                "execute",
                "media.save",
                "--input",
                '{"url":"https://example.com/video"}',
                "--options",
                '{"mode":"audio"}',
            ])

        self.assertEqual(code, 0)
        request = execute.call_args.args[0]
        self.assertEqual(request.capability, "media.save")
        self.assertEqual(request.input["url"], "https://example.com/video")
        self.assertEqual(request.options["mode"], "audio")
        self.assertEqual(json.loads(output)["status"], "success")

    def test_execute_unknown_capability_returns_failure(self):
        result = {
            "status": "failed",
            "capability": "missing",
            "run_id": None,
            "artifacts": [],
            "data": {},
            "error": {"kind": "ResolutionError", "message": "Unknown capability"},
        }
        with patch("runtime.__main__.ExecutionEngine.execute", return_value=result):
            code, output = self._run([
                "execute",
                "missing",
                "--input",
                "{}",
            ])

        self.assertEqual(code, 1)
        self.assertEqual(json.loads(output)["error"]["kind"], "ResolutionError")

    def test_execute_invalid_json_fails(self):
        with patch("sys.argv", [
            "python -m runtime",
            "execute",
            "media.save",
            "--input",
            "{invalid",
        ]):
            with self.assertRaises(SystemExit) as exit_info:
                main()
        self.assertEqual(exit_info.exception.code, 2)

    def test_execute_non_object_input_fails(self):
        with patch("sys.argv", [
            "python -m runtime",
            "execute",
            "media.save",
            "--input",
            "[]",
        ]):
            with self.assertRaises(SystemExit) as exit_info:
                main()
        self.assertEqual(exit_info.exception.code, 2)

    def test_media_save_convenience_command_uses_execution_engine(self):
        result = {
            "status": "failed",
            "capability": "media.save",
            "run_id": None,
            "artifacts": [],
            "data": {},
            "error": {"kind": "PrerequisiteError", "message": "test"},
        }
        with patch("runtime.__main__.ExecutionEngine.execute", return_value=result) as execute:
            code, _ = self._run([
                "media",
                "save",
                "https://example.com/video",
            ])

        self.assertEqual(code, 1)
        request = execute.call_args.args[0]
        self.assertEqual(request.capability, "media.save")
        self.assertEqual(request.input["url"], "https://example.com/video")


if __name__ == "__main__":
    unittest.main()
