# Releasing a monthly pass

After a monthly hands-on pass is merged to `main` (adds, removals, and any
description fixes recorded in the README and `DECLINED.md`), create one
GitHub Release so repository watchers are notified.

Do this only after the Pages workflow on `main` has published the
corresponding [updates page](https://anhermon.dev/awesome-agent-observability/updates/).
Do not post the notes anywhere else. Sharing on X stays with the maintainer.

1. Generate the notes from the same sources the site uses. Do not hand-write a second list of adds and removals:

   ```bash
   python3 scripts/release_notes.py YYYY-MM > notes.md
   ```

   `YYYY-MM` is the month of the pass, for example `2026-11`.

2. Create the release at the merge commit on `main`:

   ```bash
   gh release create YYYY-MM --title "Monthly pass YYYY-MM" --notes-file notes.md
   ```

The first release for a month that already has updates should be created only
once the write-ups are live on the site, from that month's generated notes.
