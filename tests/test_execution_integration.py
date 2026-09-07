import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from runtime.core.artifact import find_by_run
from runtime.core.state import get_state
from runtime.capabilities.media_save import save_media


class ExecutionIntegrationTests(unittest.TestCase):
    def test_success_registers_artifact_and_state(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "media"
            output.mkdir()
            artifact = output / "sample.mp3"

            def fake_run(*args, **kwargs):
                artifact.write_text("audio", encoding="utf-8")
                class Result:
                    returncode = 0
                    stdout = ""
                    stderr = ""
                return Result()

            with patch("runtime.capabilities.media_save.shutil.which", return_value="/bin/tool"),                  patch("runtime.capabilities.media_save.subprocess.run", side_effect=fake_run):
                with patch("runtime.core.artifact.DEFAULT_REGISTRY", root / "artifacts.json"),                      patch("runtime.core.state.DEFAULT_STATE", root / "state.json"):
                    result = save_media("https://example.com/video", output_dir=output)

            self.assertEqual(result["status"], "success")
            self.assertEqual(len(result["artifacts"]), 1)
            self.assertIn("artifact_id", result["artifacts"][0])


if __name__ == "__main__":
    unittest.main()
