# Workflows

Workflows are automation sequences that the agent executes regularly.

## Creating a Workflow

```markdown
# Workflow Name

**Trigger**: Time-based, event-based, or manual
**Frequency**: Daily, weekly, etc.
**Skills Used**: List skills this workflow uses

## Steps

1. Step description
2. Step description
3. Step description

## Conditions

When to execute:
- Time constraints
- Event triggers
- Data conditions

## Success Criteria

How to know the workflow completed successfully
```

## Example Workflow: Monday Morning Brief

```markdown
# Monday Morning CEO Brief

**Trigger**: Time-based (Mon 08:00 AM)
**Frequency**: Weekly
**Skills Used**: audit_transactions, generate_report

## Steps

1. Audit bank transactions since Friday
2. Extract key revenue metrics
3. Identify financial bottlenecks
4. Compile into executive summary
5. Send email with attachments

## Conditions

- Only on business days
- Only if transactions exist
- Skip if already sent today

## Success Criteria

- Email sent successfully
- Metrics calculated
- Executive notified
```

## Predefined Workflows

1. **Daily Standup** - Daily task summary
2. **Weekly Review** - Week overview
3. **Monthly Audit** - Financial review
4. **Email Triage** - Sort and respond to emails

## Customization

Edit workflow files to:
- Change trigger timing
- Add new steps
- Modify success criteria
- Adjust skill parameters

The agent checks this directory and auto-loads workflows on startup.
