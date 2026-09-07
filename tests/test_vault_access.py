import tempfile
import unittest
from pathlib import Path

from runtime.capabilities.vault_access import read_vault, write_vault


class VaultAccessTests(unittest.TestCase):
    def test_write_then_read_markdown(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "vault"
            written = write_vault("journal/today.md", "# Today", vault_root=root)
            self.assertEqual(written["status"], "success")
            result = read_vault("journal/today.md", vault_root=root)
            self.assertEqual(result["status"], "success")
            self.assertEqual(result["data"]["content"], "# Today")

    def test_write_refuses_existing_without_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "vault"
            write_vault("note.md", "one", vault_root=root)
            result = write_vault("note.md", "two", vault_root=root)
            self.assertEqual(result["status"], "failed")
            self.assertEqual(result["error"]["kind"], "ConflictError")

    def test_path_cannot_escape_vault(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "vault"
            result = write_vault("../outside.md", "x", vault_root=root)
            self.assertEqual(result["status"], "failed")
            self.assertEqual(result["error"]["kind"], "ValidationError")

    def test_non_markdown_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            result = write_vault("note.txt", "x", vault_root=Path(directory) / "vault")
            self.assertEqual(result["status"], "failed")
            self.assertEqual(result["error"]["kind"], "ValidationError")


if __name__ == "__main__":
    unittest.main()
