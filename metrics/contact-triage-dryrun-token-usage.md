# contact-triage-dryrun token usage

## Method

- Tool: `tiktoken`
- Encoding: `o200k_base`
- Manifest: `metrics/contact-triage-dryrun-token-manifest.tsv`
- Scope: files listed in the manifest as inputs and generated outputs.
- Caveat: this is a lower-bound estimate from visible text. It excludes Codex system/developer instructions, tool schemas, hidden reasoning, cache effects, and transient tool output that was not saved to files.
- Calibration multiplier `k = measured tokens / estimated tokens`: TBD.
- Calibration procedure: in the next real project, compare this estimate with measured usage from Codex session logs under `~/.codex/sessions/` and record `k` here.

## Result

| Bucket | Tokens |
|---|---:|
| input | 17,224 |
| output | 10,729 |
| total | 27,953 |

## File Breakdown

| Bucket | File | Tokens |
|---|---|---:|
| input | user-provided interview summary | 612 |
| input | harness overview | 6,196 |
| input | discovery flow | 2,240 |
| input | routing rules | 1,013 |
| input | webapp flow | 2,857 |
| input | acceptance criteria template | 1,575 |
| input | sprint metrics template | 1,104 |
| input | frontend-skill instructions | 1,627 |
| output | project requirements | 1,148 |
| output | acceptance criteria | 1,003 |
| output | sprint metrics | 801 |
| output | findings | 586 |
| output | webapp html | 1,297 |
| output | webapp css | 1,855 |
| output | webapp js | 3,573 |
| output | triage rules | 466 |

## Build CoP Tokens

```text
build CoP tokens = 27,953 tokens
                   = cumulative tokens until the artifact passes layer 1 and 2
```
