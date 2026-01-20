# Pending Approval

Items requiring human approval before execution.

## Approval Workflow

1. AI creates an approval request file
2. Human reviews the file
3. Human moves file to `/Approved` to accept
4. Or moves to `/Rejected` to decline
5. AI executes or logs rejection

## File Format

```markdown
---
type: approval_request
action: [email_send | payment | post_social]
created: 2026-01-17T10:30:00Z
expires: 2026-01-18T10:30:00Z
status: pending
---

## Details

[Describe what is being approved]

## To Approve

Move this file to `/Approved` folder.

## To Reject

Move this file to `/Rejected` folder.
```

Approval files older than 24 hours are auto-rejected.
