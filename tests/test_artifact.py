import tempfile
import unittest
from pathlib import Path

from runtime.core.artifact import (
    find_by_run,
    get_artifact,
    list_artifacts,
    register_artifact,
)


class ArtifactTests(unittest.TestCase):
    def test_register_and_get_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            file_path = root / "output.txt"
            file_path.write_text("artifact", encoding="utf-8")
            registry = root / "registry.json"

            artifact = register_artifact(
                file_path, "document", run_id="run-1", registry_path=registry
            )

            self.assertEqual(get_artifact(artifact["artifact_id"], registry)["type"], "document")
            self.assertEqual(len(list_artifacts(registry)), 1)

    def test_find_by_run(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            registry = root / "registry.json"
            for name, run_id in [("a.txt", "run-1"), ("b.txt", "run-2")]:
                path = root / name
                path.write_text(name, encoding="utf-8")
                register_artifact(path, "document", run_id=run_id, registry_path=registry)

            self.assertEqual(len(find_by_run("run-1", registry)), 1)

    def test_missing_file_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(FileNotFoundError):
                register_artifact(
                    Path(directory) / "missing.txt",
                    "document",
                    registry_path=Path(directory) / "registry.json",
                )


if __name__ == "__main__":
    unittest.main()
