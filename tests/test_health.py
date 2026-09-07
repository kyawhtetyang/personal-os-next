import unittest
from unittest.mock import patch
from runtime.health import check

class HealthTests(unittest.TestCase):
    @patch("runtime.health.shutil.which")
    def test_healthy(self, which):
        which.return_value="/bin/tool"
        self.assertEqual(check()["status"],"healthy")
    @patch("runtime.health.shutil.which")
    def test_degraded(self, which):
        which.side_effect=lambda name: None if name=="yt-dlp" else "/bin/tool"
        self.assertEqual(check()["status"],"degraded")
