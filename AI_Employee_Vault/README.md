# AI Employee Vault

This Obsidian vault serves as the memory and dashboard for the Bronze Tier Personal AI Employee.

## Structure

### Brain/
Contains agent reasoning logs and decision records.
- Decision logs with timestamps
- Reasoning chains
- Action history

### Memory/
Stores facts, context, and learned patterns.
- User preferences
- Business context
- API keys and credentials (encrypted)
- Task history

### Skills/
Reusable task templates and capabilities.
- Email handling
- Calendar management
- Report generation
- Task automation

### Workflows/
Automation sequences and processes.
- Morning briefings
- Weekly reports
- Recurring tasks

## Integration

The agent automatically:
- Logs decisions to `Brain/`
- Loads context from `Memory/`
- Executes skills defined in `Skills/`
- Follows workflows in `Workflows/`

## Getting Started

1. Create skill templates in `Skills/`
2. Define workflows in `Workflows/`
3. Start the agent with `uv run python src/main.py`
4. Monitor decisions in `Brain/`
