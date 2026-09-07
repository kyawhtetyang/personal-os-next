import json
import tempfile
import unittest
from pathlib import Path
from runtime.core.run_record import write_run

class RunRecordTests(unittest.TestCase):
    def test_write_run_creates_json_record(self):
        with tempfile.TemporaryDirectory() as directory:
            record=write_run("test.capability","success",runs_dir=directory)
            path=Path(directory)/f"{record['run_id']}.json"
            self.assertTrue(path.exists())
            stored=json.loads(path.read_text())
            self.assertEqual(stored["capability"],"test.capability")
            self.assertEqual(stored["status"],"success")

if __name__=="__main__":
    unittest.main()
