import json
import tempfile
import unittest
from pathlib import Path

from runtime.core.registry import get_capability, list_capabilities, load_capabilities


class RegistryTests(unittest.TestCase):
    def test_loads_canonical_registry(self):
        registry = load_capabilities()
        self.assertEqual(registry["schema_version"], "0.1")
        self.assertEqual(len(registry["capabilities"]), 1)

    def test_lists_media_save(self):
        capabilities = list_capabilities()
        self.assertEqual(capabilities[0]["id"], "media.save")

    def test_get_capability(self):
        capability = get_capability("media.save")
        self.assertIsNotNone(capability)
        self.assertEqual(capability["runtime"], "runtime.capabilities.media_save")

    def test_missing_capability_returns_none(self):
        self.assertIsNone(get_capability("missing.capability"))

    def test_duplicate_ids_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "registry.json"
            path.write_text(json.dumps({
                "capabilities": [{"id": "x"}, {"id": "x"}]
            }), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_capabilities(path)


if __name__ == "__main__":
    unittest.main()
