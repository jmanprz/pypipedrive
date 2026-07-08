# Examples

Standalone scripts demonstrating `pypipedrive` usage. They are **not** part of
the installed package or the test suite, and they require a valid
`PIPEDRIVE_API_TOKEN` in your environment (see the project README / `.env`).

- `script_api.py` — quickstart: fetch a deal in both V1 and V2, print its
  `to_record()`, and (re)generate the `tests/sample_data` fixtures.
- `script_activities.py` — fetch activities and deals and inspect their records.
- `export_files.py` — bulk-download and de-duplicate files attached to records
  via the `Files` model. Set `FP` / `FP_CLEAN` to your local folders first.
- `data/` — small **anonymized, sub-sampled** exports in `Model.to_record()`
  shape: `deals_sample.json` and `leads_sample.json` (5 records each). Free-text
  fields (titles, reasons, emails) have been replaced with placeholders; the
  full, non-anonymized dumps are kept out of version control.

> These scripts contain placeholder values (e.g. `your-company.pipedrive.com`,
> local paths). Adjust them to your environment before running.
