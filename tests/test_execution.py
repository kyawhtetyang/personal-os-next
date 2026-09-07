import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from runtime.execution import ExecutionEngine, ExecutionContext, ExecutionRequest


class ExecutionModelTests(unittest.TestCase):
    def test_request_serialization(self):
        request = ExecutionRequest("media.save", {"url": "x"}, {"mode": "audio"})
        self.assertEqual(ExecutionRequest.from_dict(request.to_dict()).capability, "media.save")

    def test_invalid_request(self):
        with self.assertRaises(ValueError):
            ExecutionRequest("", {})

    def test_context_creation(self):
        context = ExecutionContext.create(ExecutionRequest("media.save", {"url": "x"}))
        self.assertTrue(context.run_id)


class ExecutionEngineTests(unittest.TestCase):
    def test_resolution_failure(self):
        result = ExecutionEngine().execute({"capability": "missing", "input": {}})
        self.assertEqual(result["error"]["kind"], "ResolutionError")

    def test_validation_failure(self):
        result = ExecutionEngine().execute({"capability": "", "input": {}})
        self.assertEqual(result["error"]["kind"], "ValidationError")

    def test_success_lifecycle(self):
        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "sample.mp3"
            artifact.write_text("audio", encoding="utf-8")
            raw = {"status": "success", "capability": "media.save", "run_id": None, "artifacts": [], "data": {"source_url": "x", "artifact_path": str(artifact), "artifact_type": "media"}, "error": None}
            with patch("runtime.execution.engine.get_capability", return_value={"id": "media.save"}), patch("runtime.execution.engine.save_media", return_value=raw):
                result = ExecutionEngine().execute({"capability": "media.save", "input": {"url": "x"}})
            self.assertEqual(result["status"], "success")
            self.assertEqual(len(result["artifacts"]), 1)


    def test_non_artifact_success_lifecycle(self):
        raw = {
            "status": "success",
            "capability": "vault.read",
            "run_id": None,
            "artifacts": [],
            "data": {"path": "journal/today.md", "content": "# Today", "format": "markdown"},
            "error": None,
        }
        with patch("runtime.execution.engine.get_capability", return_value={"id": "vault.read"}), patch("runtime.execution.engine.read_vault", return_value=raw):
            result = ExecutionEngine().execute({"capability": "vault.read", "input": {"path": "journal/today.md"}})
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["artifacts"], [])
        self.assertTrue(result["run_id"])

if __name__ == "__main__":
    unittest.main()
