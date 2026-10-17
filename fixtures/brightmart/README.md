# BrightMart dataset

BrightMart is a fictional online grocery business. These files were generated locally by `scripts/build_fixtures.py` for Company Brain and are intended to be included in the source repository. They contain no real company exports, employee records, customer contracts, API credentials or production database dumps. Any resemblance to real people or businesses is coincidental.

The dataset contains **200 source records, 180 entities and 432 supported claims**:

- 40 people, 8 teams, 10 projects, 16 services and 10 customers.
- 60 tickets, 24 decisions and 12 commitment entities.
- 94 documents, 21 chat exports, 60 ticket records, 24 decision records and one directory.

`registry.json` contains public entity IDs, labels and aliases. `manifest.json` lists the source files, SHA-256 checksums and dataset version. Each source JSON contains a readable `envelope` and reviewed extraction `claims` anchored to exact passages. The application loads these facts into FalkorDB through its normal validated ingestion process. These are extraction fixtures, not prewritten answers.

`engineering`, `leadership` and `all_employees` access labels, including the deliberately confidential-looking markers, are part of the fictional permission scenarios. They are not secrets or real company information. Local uploads and runtime databases are separate and must not be added here without reviewing their contents.

Regenerate from the repository root:

```sh
python3 scripts/build_fixtures.py
```

Regeneration writes the fixture JSON, checksummed manifest, workspace catalog and readable source book. It does not overwrite active graph revisions or reset a running workspace.

See [the source book](../../docs/BrightMart-Sourcebook.md), [the dataset guide](../../docs/BrightMart-Demo.md) and [the project README](../../README.md) for the company story and run instructions. Evaluation questions live separately in `evals/questions.jsonl` and are not loaded as company facts.
