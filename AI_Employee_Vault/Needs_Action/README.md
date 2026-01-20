# Needs Action

Items waiting for AI processing or human approval.

## Workflow

1. **Detection**: Watchers place files here
2. **Processing**: Claude processes and creates plans
3. **Approval**: Sensitive items moved to `/Pending_Approval`
4. **Completion**: Completed items moved to `/Done`

## File Naming Convention

- `EMAIL_<id>.md` - Email message requiring response
- `WHATSAPP_<sender>.md` - WhatsApp message
- `FILE_<name>.md` - File requiring processing
- `TASK_<description>.md` - Task for completion

## Automatic Processing

Files placed here are automatically picked up by Claude Code within 60 seconds.
