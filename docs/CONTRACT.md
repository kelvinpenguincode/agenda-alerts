# Data contract

This is the agreed shape of the data. Backend produces it, frontend consumes it. If you want to change it, tell everyone first and update this file in the same pull request.

## Agenda item

One decision on one agenda, already translated into plain language.

| Field | Type | Meaning |
| --- | --- | --- |
| `id` | string | Unique id, e.g. `isd-2026-11-10-04` |
| `body` | `"isd"` or `"city"` | Which kind of government body |
| `body_name` | string | Full name of the board or council |
| `meeting_date` | string `YYYY-MM-DD` | When it meets |
| `category` | `tax_rate`, `zoning`, `school_policy`, `budget`, `other` | Used for filtering and alerts |
| `title_original` | string | Item title exactly as printed on the agenda |
| `plain_summary` | string | Plain-English explanation. Every number in it must appear in the source text |
| `amounts` | list | Dollar amounts and rates found in the item (see below) |
| `location` | object or `null` | `address`, `lat`, `lon` when the item concerns a place |
| `source` | object | `url`, `page`, and `quote` (the exact line from the agenda) |
| `verified` | boolean | `true` only if the number check passed |
| `sample` | boolean | `true` on fake demo data. Real data omits it |

Each entry in `amounts`: `label`, `value`, `unit`, `source_quote`.

## Endpoints

| Method and path | Purpose |
| --- | --- |
| `GET /api/health` | Is the server alive |
| `GET /api/items` | All agenda items. Optional `?body=isd` or `?body=city` |
| `POST /api/tax-impact` | Body: `home_value`, `exemption`, `current_rate`, `proposed_rate`. Returns `taxable_value`, `current_bill`, `proposed_bill`, `difference` |

Tax rates are per $100 of taxable value, matching how Texas tax notices print them.

## Coming next (not built yet)

- `GET /api/items/near?address=...` items that concern places near an address
- `POST /api/subscribe` email alerts for an address
