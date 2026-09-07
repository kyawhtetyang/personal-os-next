# AI Agent Guide

## Mission
Help operate and evolve Personal OS Next without inventing parallel architecture.

## Request flow
1. Read relevant context.
2. Identify an existing capability.
3. Read its contract.
4. Reuse runtime implementation when available.
5. Execute or provide the exact command appropriate to the agent.
6. Verify the result.
7. Persist outputs in the correct location.

## Architecture rules
- vault = human-facing source material and Obsidian interface.
- system = governance and definitions.
- runtime = executable behavior.
- data = machine state and artifacts.
- Do not place runtime code in vault.
- Do not place canonical contracts inside generated artifacts.
- Prefer existing capabilities over new scripts.
- Prefer deterministic workflows over agentic behavior.
- Add complexity only after repeated real use demonstrates need.

## Model roles
ChatGPT may reason and provide semantic guidance.
Codex may inspect and modify the repository and execute tools.
Local/API models are replaceable intelligence providers.

Models are clients of the OS, not the OS itself.