import tempfile
import unittest
from pathlib import Path

from runtime.core.state import (
    delete_state,
    get_state,
    list_state,
    set_state,
    update_state,
)


class StateTests(unittest.TestCase):
    def test_missing_state_returns_none(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertIsNone(get_state("missing", Path(directory) / "state.json"))

    def test_set_and_get_state(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            value = set_state("media.save", {"status": "success"}, path)
            self.assertEqual(value["status"], "success")
            self.assertEqual(get_state("media.save", path)["status"], "success")

    def test_update_state_merges_values(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            set_state("media.save", {"status": "success"}, path)
            value = update_state("media.save", {"last_run_id": "run-1"}, path)
            self.assertEqual(value["status"], "success")
            self.assertEqual(value["last_run_id"], "run-1")

    def test_delete_state(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            set_state("media.save", {"status": "success"}, path)
            self.assertTrue(delete_state("media.save", path))
            self.assertFalse(delete_state("media.save", path))

    def test_list_state(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            set_state("a", {"value": 1}, path)
            set_state("b", {"value": 2}, path)
            self.assertEqual(set(list_state(path)), {"a", "b"})

    def test_non_object_state_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                set_state("bad", "value", Path(directory) / "state.json")


if __name__ == "__main__":
    unittest.main()
