# epi-demand

Epidemiology and end-market demand.

| Skill | Moves | Sub-sector | Ease/Impact |
|---|---|---|---|
| `epi-demand-funnel` | TAM / peak sales | #biopharma #medtech #tools-dx | 3 / 4 |
| `respiratory-surveillance` | Near-term revenue nowcast; season-severity trade | #biopharma #tools-dx | 4 / 3 |
| `nih-reporter-endmarket` | Life-science tools end-market growth / capex cycle | #tools-dx | 4 / 4 |

**Agent:** `demand-watcher` — weekly respiratory surveillance in season, quarterly NIH
RePORTER, annual SEER.

**Data:** CDC WONDER (XML POST API, no key) · FluView / NREVSS via Delphi Epidata ·
CDC NWSS wastewater via Socrata on data.cdc.gov (updated Fridays, preliminary) · SEER
aggregate statistics · NIH RePORTER v2 REST API (no key).

Anchors prompt-library IDs MOD-06 (Tools/Dx Capex-Cycle Model) and SUB-TLS-02 (NGS
Instrument).

## Standard of evidence

Built to **institutional investor standards: rigorous and auditable.** 
In short: every finding carries a source, a retrieval
date and the vintage of the underlying data; confidence is gated by vintage rather
than conviction; scripts fail loudly on empty result sets so silence is never read as
a negative finding; known limitations travel in-line with the number; and evidence
stays separated from view, because this engine issues no recommendations.

## Setup

Open-data endpoints rate-limit unidentified and shared User-Agents, and SEC EDGAR
blocks them outright, so your contact string is required rather than defaulted:

```bash
export HH_CONTACT="Your Name (you@example.com)"
```

## Author

HH-health-ai

## Disclaimers

Not affiliated with, endorsed by, or connected to CMS, HHS, the FDA, the SEC, the
USPTO, the CDC, the EMA or any other government agency. All data is retrieved from
public endpoints subject to those agencies' own terms.

Nothing here is investment advice, and no output should be read as a recommendation to
buy or sell any security. These engines produce evidence for a human analyst to weigh.

Optional MCP servers are independent third-party projects under their own licenses.
Review them before use.

## License

MIT — see [LICENSE](LICENSE).

## NIH query completeness

NIH RePORTER summaries require an explicit API total and a fetched count equal to it.
If matches exceed `--limit`, pagination ends early, or the count changes during the
run, the script exits nonzero without a partial total. Narrow the query or raise
the limit; the default 500 is a safety cap, not a representative sample.
Successful summaries include matched/fetched counts and `truncated: false`.

## Regression tests

Run offline with Python 3.10 or newer (standard library only):

```bash
python3 -m unittest discover -s tests -v
```

Tests use synthetic fixtures and mocked APIs; they do not certify live endpoint
availability or current regulatory facts. GitHub Actions runs the same tests on PRs.
