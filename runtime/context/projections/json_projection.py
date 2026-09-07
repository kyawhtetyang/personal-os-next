"""JSON projection for canonical context."""
def project_json(context): return context.to_dict() if hasattr(context, "to_dict") else context
