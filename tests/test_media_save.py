import shutil
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, "runtime/capabilities")
from media_save import save_media


class MediaSaveTests(unittest.TestCase):
    def test_invalid_mode_fails(self):
        with patch.object(shutil, "which", return_value="/usr/bin/yt-dlp"):
            result = save_media("https://example.com", mode="invalid")
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["error"]["kind"], "ValidationError")

    def test_missing_ytdlp_fails(self):
        with patch.object(shutil, "which", return_value=None):
            result = save_media("https://example.com")
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["error"]["kind"], "PrerequisiteError")


if __name__ == "__main__":
    unittest.main()
