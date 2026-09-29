# TaskStop

- Stops a running background task by its ID
- Takes a task_id parameter identifying the task to stop
- To stop an agent-team teammate, pass its agent ID ("name@team") or bare teammate name as task_id
- To stop a background agent spawned with a name, pass that name as task_id
- Returns a success or failure status
- Use this tool when you need to terminate a long-running task

## parameters

- `task_id` — string: The ID of the background task to stop. Agent-team teammates and named background agents are also accepted by agent ID or name.
- `shell_id` — string: Deprecated: use task_id instead
