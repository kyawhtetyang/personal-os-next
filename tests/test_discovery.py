import json
import tempfile
import unittest
from pathlib import Path

from runtime.core.discovery import discover, load_manifest


class DiscoveryTests(unittest.TestCase):
    def test_loads_manifest(self):
        manifest = load_manifest()
        self.assertEqual(manifest["os"]["id"], "personal-os-next")

    def test_discover_returns_os_information(self):
        result = discover()
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["os"]["name"], "Personal OS Next")
        self.assertEqual(result["capabilities"][0]["id"], "media.save")
        self.assertEqual(result["entrypoints"]["cli"], "python -m runtime")

    def test_missing_manifest_fails(self):
        with self.assertRaises(FileNotFoundError):
            load_manifest("missing-manifest.json")

    def test_custom_manifest_loads(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            path.write_text(json.dumps({"os": {"id": "test"}}), encoding="utf-8")
            self.assertEqual(load_manifest(path)["os"]["id"], "test")


if __name__ == "__main__":
    unittest.main()
