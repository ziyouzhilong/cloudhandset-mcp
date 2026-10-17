# Parallel control of multiple Android phones

Use this workflow when the user requests work on multiple phones. An account connection must cover those phones; a legacy single-phone authorization cannot see the others. Refresh `list_devices`, match the requested phone names, and exclude phones outside the task. A busy phone stays with its current operator. Do not expand the task to every visible phone merely because the account has access.

## One independent sequence per phone

Keep a record for each `device_id`: its acquisition operation ID, returned `session_id` and control epoch, latest observation ID/expiry and image, any pending operation/upload IDs, outcome, and release evidence. Never keep a shared “current phone”, session, screenshot, or operation ID across workers.

Different phones may have requests in flight together. Within one phone, finish or resolve the current step before starting the next. Acquire each phone separately; then observe, inspect its actual image, perform its next authorized action, and verify that action. A mutation invalidates only that phone's previous observation. Do not copy coordinates, observations, uploads, or results from another phone. Do not queue a visual action until its image has been read; re-observe if the observation expires while waiting for a dispatch slot.

Use the host's native parallel tool facility when it exists. Issue one step per ready phone and retain a separate result for every call, including failures. If the host can only call tools sequentially, interleave the independent phone sequences and report that execution was interleaved. Do not claim simultaneous execution or create extra tasks/agents merely to work around a missing host capability.

## Dispatch and limits

An account may control at most **16 Android phones at the same time**, across all clients, connections, credentials, processes, and tasks. The account may own and list more phones. Reserving, active, stopping, and isolating sessions occupy capacity; only confirmed closed/drained sessions free it. A different credential or coordinator does not create another allowance.

Use one coordinator for the account's phone work. Before dispatching a batch, count its distinct target phones together with the sessions already held by this task. Reject a set larger than 16 before any acquisition or phone action; do not silently truncate, split it into automatic batches, or start extra agents. Report the limit and prepare an explicit smaller batch. Worker count must be 1–16 and controls requests in flight; it does not override the account limit or shared call budgets. Keep one step in flight per phone.

The current service budget is 180 ordinary calls/minute per credential, plus a separate shared 60/minute for release and operation-status calls. New control acquisitions also consume the account's 60/minute and lease's 12/minute acquisition budgets. Device-level limits still apply. Spread new acquisitions and ordinary calls over time, leave room for observation/recovery, and give ready phones a turn before repeatedly polling one phone. Prefer release over status polling in the shared cleanup budget. Account authorization and worker count do not multiply these allowances.

Honor live `rate_limit`, `retry_after_ms` / `retry_after_seconds`, and HTTP `Retry-After` results. Pause dispatch from the affected budget rather than immediately replaying calls. A rate-limit response for one request says nothing about another request whose outcome is unknown. Keep that original operation ID and resolve it through status/observation. Separate processes and host tasks do not share the Muse batch command's local pacing; their coordinator must allocate a combined budget and wait between batches. If a phone will not receive useful work before the idle timeout, release it and acquire again when ready rather than holding control with empty keepalive traffic.

On `account_device_limit_reached`, stop queued acquisitions and report the affected phone and operation ID. Do not retry automatically or switch credentials. Finish/release only this task's own sessions, verify closure, and explicitly request the next acquisition after capacity is free. Other tasks' sessions must remain untouched. Recovery and release calls remain available at the limit.

## Partial failure and cleanup

One phone's busy, stale-image, or unknown-operation result must not overwrite another phone's session or success. Stop new mutations on the affected phone, retain its original request/operation ID, and resolve it without replay. On a lost acquisition result, retain that exact acquisition request and ID for recovery; do not make another acquisition with a new ID. A successful acquisition in another worker still needs cleanup.

On completion, cancellation, or a blocked task, stop further work and release each session acquired by this task independently. Release held inputs first. Send only `session_id` to `release_control`. Verify `closed: true`, `state: "closed"`, and drained-writer evidence separately for every phone. A failed release is unresolved cleanup; it is not permission to stop another writer. Never release a session from another task. Report per-phone outcome and release status, including any unknown acquisition that still needs recovery.
