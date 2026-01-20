# Memory Storage

This directory stores facts, context, and learned patterns.

## File Types

### Context Files (context_*.md)
- User preferences and settings
- Business configuration
- Learned patterns

### Facts Files (facts_*.md)
- Business facts
- User information
- Integration details

## Example Context

```json
{
  "user_name": "Your Name",
  "timezone": "UTC",
  "business_hours": "09:00-17:00",
  "email_domains": ["company.com", "personal.com"],
  "response_style": "professional"
}
```

## Privacy

- Keep sensitive data minimal
- Encrypt credentials before storing
- Regular cleanup of obsolete entries

## Auto-Populated

The agent automatically updates:
- Task completion status
- Email summaries
- Decision history
- Event logs
