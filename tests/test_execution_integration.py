import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from runtime.core.artifact import find_by_run
from runtime.core.state import get_state
from runtime.execution import ExecutionEngine


class ExecutionIntegrationTests(unittest.TestCase):

    def test_success_registers_artifact_and_state(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            artifact_path = root / "sample.mp3"
            artifact_path.write_text("audio", encoding="utf-8")

            raw_result = {
                "status": "success",
                "capability": "media.save",
                "run_id": None,
                "artifacts": [],
                "data": {
                    "source_url": "https://example.com/video",
                    "artifact_path": str(artifact_path),
                    "artifact_type": "media",
                    "format": "mp3",
                },
                "error": None,
            }

            with patch(
                "runtime.execution.engine.get_capability",
                return_value={"id": "media.save"},
            ):
                with patch(
                    "runtime.execution.engine.save_media",
                    return_value=raw_result,
                ):
                    result = ExecutionEngine().execute(
                        {
                            "capability": "media.save",
                            "input": {
                                "url": "https://example.com/video",
                            },
                        }
                    )

            self.assertEqual(result["status"], "success")
            self.assertEqual(len(result["artifacts"]), 1)

            artifact = result["artifacts"][0]

            self.assertIn("artifact_id", artifact)

            run_id = result["run_id"]

            registered = find_by_run(run_id)

            self.assertEqual(len(registered), 1)

            state = get_state("media.save")

            self.assertEqual(state["status"], "success")
            self.assertEqual(state["last_run_id"], run_id)


if __name__ == "__main__":
    unittest.main()
