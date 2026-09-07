import unittest
from runtime.context import ContextAssembler, ContextRequest
from runtime.context.models import Context
from runtime.context.projections import project_json, project_markdown

class ContextModelTests(unittest.TestCase):
    def test_request_serialization(self):
        request = ContextRequest("development", query="continue", sources=["state"])
        self.assertEqual(ContextRequest.from_dict(request.to_dict()).purpose, "development")
    def test_invalid_purpose(self):
        with self.assertRaises(ValueError): ContextRequest("")
    def test_context_serialization(self):
        context = Context("ctx_1", "now", "development", ["state"], {"state": {}})
        self.assertEqual(Context.from_dict(context.to_dict()).id, "ctx_1")

class ContextAssemblyTests(unittest.TestCase):
    def setUp(self):
        self.assembler = ContextAssembler({"state": lambda request: {"current": "v0.2.0"}, "discovery": lambda request: {"version": "0.2.0"}, "artifacts": lambda request: []})
    def test_assemble_selected_sources(self):
        context = self.assembler.assemble(ContextRequest("development", sources=["state", "discovery"]))
        self.assertEqual(context.sources, ["state", "discovery"])
        self.assertIn("state", context.data)
    def test_unknown_source(self):
        with self.assertRaises(ValueError): self.assembler.assemble(ContextRequest("development", sources=["missing"]))
    def test_projections(self):
        context = self.assembler.assemble(ContextRequest("development", sources=["state"]))
        self.assertEqual(project_json(context)["purpose"], "development")
        self.assertIn("# Personal OS Context", project_markdown(context))
