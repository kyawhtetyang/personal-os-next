import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from runtime.execution import ExecutionEngine


class MediaVerificationTests(unittest.TestCase):

    def test_existing_reported_artifact_is_accepted(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "media"
            output.mkdir()

            artifact = output / "existing.mp3"
            artifact.write_text("audio", encoding="utf-8")

            class Result:
                returncode = 0
                stdout = str(artifact) + "\n"
                stderr = ""

            with patch(
                "runtime.capabilities.media_save.shutil.which",
                return_value="/bin/tool",
            ), patch(
                "runtime.capabilities.media_save.subprocess.run",
                return_value=Result(),
            ):
                result = ExecutionEngine().execute(
                    {
                        "capability": "media.save",
                        "input": {
                            "url": "https://example.com/video",
                            "output_dir": str(output),
                        },
                    }
                )

            self.assertEqual(result["status"], "success")
            self.assertEqual(len(result["artifacts"]), 1)

            self.assertEqual(
                Path(result["artifacts"][0]["path"]),
                artifact.resolve(),
            )


if __name__ == "__main__":
    unittest.main()
