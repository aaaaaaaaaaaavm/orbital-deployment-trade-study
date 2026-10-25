# Publication and contributor rules

Publish an identified source tree whose examples, claims, artifacts and license metadata agree. Retain source and third-party credits and the original identities of historical fixtures. A numerical check or matching hash does not establish physical performance or external approval.

## Prepare the exact payload

Stage the complete intended change, including new files, and run:

```bash
python3 tools/prepublish_gate.py --all
```

The gate checks **Git index contents**, then reconstructs that exact tree in a temporary directory. Unstaged changes and untracked files are not silently included. For a committed release run `python3 tools/prepublish_gate.py --commit HEAD`. The gate source must itself match the selected tree. A temporary `GIT_INDEX_FILE` can test a candidate without changing the working index.

The offline checks cover probable credentials/private exports, private draft filenames, source-identified generation footers, UTF-8/finite JSON, local Markdown/image links, a 30 MB file limit and PDF/STEP/image/ZIP-based document framing. Containers receive CRC, member-path and size checks. Symbolic links, submodules and unmerged entries require separate review and fail this bounded gate. Current authored links must resolve inside the payload. Immutable `reference/volley/` fixtures retain their original link context and are checked by their existing identity validator.

The exact snapshot runs the existing unit suite, `tools/verify_repository.py` where present, and `tools/check_scientific_assets.py` where present. These checks use local inputs; remote service availability is not scientific evidence. A pass reports the checked Git tree, file count and actual test/validator results. It does not record a human review.

## Review and release

Check the reader route, labels, citation/version/license metadata, source/results, uncertainty and any changed fixture assumptions before publication. Record the exact commit/tree, artifact hashes, destination, check results and actual review method. Describe external or human review only when it occurred. Preserve failed results and configuration boundaries; do not widen acceptance bands to pass a release.

Use the installed pre-push hook with `git config core.hooksPath .githooks`. It checks each nondeleted commit being pushed, including release tags, without changing the working index. CI fetches the exact event SHA without third-party Actions and repeats the publication gate. Existing scientific figure and test checks retain their roles. These local/CI controls do not configure server branch protection or prevent an explicitly bypassed local hook; no settings change is implied.

Keep private coordination, correspondence and credentials outside the public payload. Review issue/release/settings text and external artifact destinations with the same claim and privacy criteria because a file gate cannot inspect material it was not given.

The gate adapts the project-owned VOLLEY publication checker; its copyright and source identity are retained in the script and NOTICE. Repository licenses and immutable source-fixture licenses are unchanged.
