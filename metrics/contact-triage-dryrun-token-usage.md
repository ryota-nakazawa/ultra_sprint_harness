# contact-triage-dryrun token usage

## Method

- Tool: `tiktoken`
- Encoding: `o200k_base`
- Manifest: `metrics/contact-triage-dryrun-token-manifest.tsv`
- Scope: files actually used for the harness dry run and files generated as the project output.
- Caveat: this is still an estimate from visible text. It excludes Codex system/developer instructions, tool schemas, hidden reasoning, cache effects, and transient tool output that was not saved to files.
- Calibration multiplier `k = measured tokens / estimated tokens`: TBD.
- Calibration procedure: in the next real project, compare this estimate with measured usage from Codex session logs under `~/.codex/sessions/` and record `k` here.

## Result

| Bucket | Tokens |
|---|---:|
| input | 16,433 |
| output | 10,611 |
| total | 27,044 |

## File Breakdown

| Bucket | File | Tokens |
|---|---|---:|
| input | user-provided interview summary | 612 |
| input | harness overview | 5,886 |
| input | discovery flow | 2,240 |
| input | routing rules | 1,013 |
| input | webapp flow | 2,738 |
| input | acceptance criteria template | 1,464 |
| input | sprint metrics template | 853 |
| input | frontend-skill instructions | 1,627 |
| output | project requirements | 1,148 |
| output | acceptance criteria | 1,003 |
| output | sprint metrics | 769 |
| output | findings | 586 |
| output | webapp html | 1,285 |
| output | webapp css | 1,855 |
| output | webapp js | 3,965 |

## CoP-token

The dry run passed the inner loop once, so:

```text
estimated CoP-token = 27,044 tokens / 1 pass
                    = 27,044 tokens per pass
```
