# Skills

Skills are reusable task templates that the agent can execute.

## Creating a Skill

Create a markdown file with the skill name and format:

```
# Skill Name

**Category**: Email / Task / Report / Custom
**Inputs**: List expected parameters
**Outputs**: What the skill returns
**Steps**: How the skill executes

## Description

Clear description of what this skill does.

## Example Usage

```
execute_skill("Skill Name", {
  "param1": "value1",
  "param2": "value2"
})
```

## Integration Points

- Gmail: Send, read, search emails
- Calendar: Create, update events
- Files: Read, write documents
- Database: Store, retrieve data
```

## Built-in Skills

### Email Skills
- `send_email`: Send an email message
- `read_email`: Extract email content
- `search_emails`: Find emails by criteria

### Task Skills
- `create_task`: Add new task
- `update_task`: Modify task
- `complete_task`: Mark task done

### Report Skills
- `generate_report`: Create status report
- `audit_transactions`: Review financial data

## Creating Custom Skills

1. Define in a `.md` file in this directory
2. Register in `SkillsManager`
3. Implement handler in Python
4. Test with agent

See [Skills Manager](../../src/agents/skills_manager.py) for technical details.
