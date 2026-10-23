# Version and discovery

## Inspect the project

```bash
rg --files -g AGENTS.md -g CLAUDE.md -g __manifest__.py -g release.py -g requirements.txt -g '*odoo*.conf' -g '*compose*.y*ml' -g Dockerfile
python3 /path/to/odoo/odoo-bin --version            # or: docker compose run --rm odoo odoo --version
rg -n "version_info|serie" /path/to/odoo/odoo/release.py
```

- A custom module's manifest `version` (`19.0.1.2.0`) is a hint, not proof. Check the actual server checkout, image tag or Odoo.sh branch version.
- Enterprise is present when the addons path includes an `enterprise` checkout (e.g. `web_studio`, `account_accountant`).
- Online runs intermediary releases (`19.1`–`19.4`, …) that on-premise never gets. A feature that exists in "19.x Online" may not exist in 19.0.
- Separate confirmed facts from assumptions in your report. Don't print secrets from config files.

Use fixed version URLs during implementation (`/documentation/19.0/...`). `latest` and `master` move.

Sources: [documentation home](https://www.odoo.com/documentation/20.0/), [CLI](https://www.odoo.com/documentation/20.0/developer/reference/cli.html), [hosting](https://www.odoo.com/documentation/20.0/administration/hosting.html).

## Compatibility boundaries

See [version deltas](version-deltas.md) for the full 18 → 19 → 20 tables, the legacy-syntax blacklist and the `upgrade_code` rewrites. The most consequential boundaries:

| Area | 19.0 | 20.0 |
| --- | --- | --- |
| Security | `ir.model.access.csv` + `ir.rule` | `ir.access.csv` (blank group = global restriction) |
| Frontend | Owl 2 (`static props`, `useState`) | Owl 3 (`useProps`, `proxy`, `this.` in templates) |
| Config params | `get_param`/`set_param` | typed `get_str/int/bool/float`, `set_*` |
| Test default | `at_install` | `post_install` |
| Runtime | Python 3.10+, PostgreSQL 13+ | Python 3.12+, PostgreSQL 16+ |

## Resolve conflicting evidence

Known documentation inconsistencies at 20.0 (checked 2026-10-23):

- The testing page states both `standard, at_install` and `standard, post_install` as defaults. Core `odoo/tests/common.py` uses `post_install` on 20.0 and `at_install` on 19.0.
- The custom-report how-to still shows `_table_query`, which the changelog removed. Core report models use `_table_sql` instead.
- The source-install page keeps a Python 3.10 note next to its 3.12 requirement.
- The licensing page still labels the current edition sections "Odoo 19".
- Owl 3, Material Symbols icons and the typed config-parameter API appear in the code and changelog/`upgrade_code` scripts, but the reference pages explain them poorly. Trust the source.

Rule: check-out source > core tests > changelog > reference docs > tutorials > forum or model memory. Report any discrepancy that matters. Build compatibility layers only for versions you have confirmed you support.
