# Gallery guide

Revision `phase1.1`, authored 2026-11-15. Confirm the actual package, version and language before use. Android phones may use different gallery apps; do not assume Google Photos, Samsung Gallery or any other package is installed.

## Preconditions and completion

The QA environment manifest must identify the actual gallery package and version, language, test files and their expected digest/size/content markers. Use only this run's synthetic media. File transfer completion, gallery indexing, opening the correct item, and a visual task are separate conditions.

## Locate and verify media

- After an authorized upload, retain the original upload/completion IDs. Verify terminal `succeeded`, size and returned Android path; an accepted PUT or a progress receipt is not completion. Resolve unknown outcomes without another upload.
- Refresh or reopen the gallery's visible local-media list using current controls. Inspect a fresh screenshot; do not assume an item exists because a file-transfer receipt succeeded.
- Select by multiple visible cues: name, size/time if available, and the synthetic image/video marker. Similar thumbnails or duplicate names require opening and checking the content. Never infer identity from the first matching thumbnail.
- For a video, verify the designated frame marker and requested duration using visible app information and the independent media manifest. Audio is outside this phase. An unviewed image/video path is not evidence.
- For rotation/zoom, inspect the actual before/after view of the same object, then return to the list and verify it. Old coordinates and semantic IDs are invalid after a display change.

## Failure and recovery

An item not yet indexed may warrant a bounded refresh within the task budget, not repeated uploads. Unexpected cloud sign-in, permission scope or a different gallery app is a new prerequisite; do not log into a customer account or enable sync to complete QA. Stop if identity remains ambiguous. Cleanup may delete only files positively matched to this run's manifest; never empty Download, an album, the media database or app data. Restore only display/rotation settings changed by this run, and report uncertain cleanup.

## Evidence boundary

Acceptance must record the actual app/device versions, language, evidence date, upload receipt, independent file digest/size and image/video identity check. Visual effects that need an independent person remain explicitly manual. This guide alone does not establish compatibility with a particular package or version.
