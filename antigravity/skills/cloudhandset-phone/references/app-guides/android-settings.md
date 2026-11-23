# Android Settings guide

Revision `phase1.1`, authored 2026-11-15. Package: `com.android.settings`. Check the actual manufacturer, Android version, app version and language before use. Paths and labels vary by manufacturer and language. No fixed coordinates or unverified success claims are provided.

## Preconditions and completion

Use the selected authorized Android phone and a fresh image. Read-only information tasks require the exact requested version/model fields. A requested setting change requires the displayed value after saving and re-entering the page. QA changes additionally require the original value recorded and restored; restore only the values changed by this run.

## Navigation and verification

- Open Settings using the existing supported `device.open_settings` action when authorized, or navigate from the current observed screen. Verify the Settings page after the receipt.
- Read Android version/model from the visible device-information pages. Distinguish Android version from an app version or build number; do not infer a model from the account alias.
- For display timeout, appearance or auto-rotate QA tasks, record the starting value and locate the actual control from current labels and screenshots. Change only the designated field. Return to the previous page, reopen the same setting, and compare the persisted value with the target.
- Search results may have repeated names. Verify the page title and relevant control before changing it. Search text is not evidence that the target setting was reached.

## Failure and recovery

A missing setting, policy restriction, permission dialog or version mismatch is an unsupported path until the current screen resolves it. Back out of an unrelated page and observe again; do not explore account, network, developer or security settings to work around it. An unknown mutation retains its original ID and is resolved through status/readback, not another toggle. Never toggle blindly during restoration. If the initial value or cleanup outcome is unknown, report it and keep the QA phone out of the next run.

## Evidence boundary

Acceptance records must add the actual package/version, manufacturer, Android version, language, evidence date, case/seed and independent state readback. This guide is a navigation aid; verify each procedure against the current device and visible result.
