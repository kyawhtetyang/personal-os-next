"""Markdown projection for canonical context."""
import json
def project_markdown(context):
    payload = context.to_dict() if hasattr(context, "to_dict") else context
    lines = ["# Personal OS Context", "", f"**Purpose:** {payload['purpose']}", f"**Created:** {payload['created_at']}", "", "## Sources"]
    lines.extend(f"- {source}" for source in payload["sources"])
    lines.extend(["", "## Data", json.dumps(payload["data"], indent=2)])
    return "\n".join(lines)
