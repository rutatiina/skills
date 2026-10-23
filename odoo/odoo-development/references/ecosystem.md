# Ecosystem beyond odoo.com

These sources are **not** part of the odoo.com documentation portal. They are widely used in real Odoo development. Check each project's own conventions before adopting any of them.

## Core source is the ground truth

The docs lag behind the code, and some docs pages contradict themselves. When a signature, default or XML schema matters, read the target branch:

```bash
git clone --depth 1 --branch 19.0 https://github.com/odoo/odoo.git ~/src/odoo-19.0
rg -n "models.Constraint\(" ~/src/odoo-19.0/addons | head          # find a real usage
rg -n "def _read_group\(" ~/src/odoo-19.0/odoo/orm/models.py
```

- Find the closest core module that already does what you need and copy its shape: model, security, views, assets and tests.
- Enterprise (`github.com/odoo/enterprise`) is private and needs a valid entitlement. Never copy or redistribute its code ([licensing](legal-and-licensing.md)).
- Key files: `odoo/orm/` (models, fields, domains, decorators), `odoo/addons/base/models/` (`ir_access`/`ir_rule`, `ir_cron`, `ir_config_parameter`), `odoo/tests/common.py`, `odoo/tools/config.py` (CLI flags), `odoo/upgrade_code/` (automated rewrites), `addons/web/static/src/` (frontend framework), `addons/web/static/tests/web_test_helpers.js`.
- Data migration helpers: `github.com/odoo/upgrade-util` (`from odoo.upgrade import util`).

## Local runtime

Source checkout (preferred for debugging): use the branch's `requirements.txt` in a virtualenv and a dedicated PostgreSQL role ([installation](installation-and-operations.md)).

Docker, using the official `odoo` image on Docker Hub, tagged by series:

```yaml
services:
  db:
    image: postgres:16
    environment: {POSTGRES_USER: odoo, POSTGRES_PASSWORD: odoo, POSTGRES_DB: postgres}
  odoo:
    image: odoo:19.0          # match the target series
    depends_on: [db]
    ports: ["8069:8069"]
    environment: {HOST: db, USER: odoo, PASSWORD: odoo}
    volumes:
      - ./addons:/mnt/extra-addons
      - ./config:/etc/odoo
```

Run commands through the container, for example `docker compose run --rm odoo odoo -d dev -i acme_case --test-tags /acme_case --stop-after-init`. Keep real credentials out of the compose file.

## Handy CLI

- `odoo-bin scaffold acme_case ./addons` creates a skeleton from a generic template. Update it to the target version's conventions ([scaffolds](scaffolds.md)).
- `odoo-bin shell -c dev.conf -d dev` opens a Python shell with `env` bound. Changes are rolled back unless you call `env.cr.commit()`. Never do that against production.
- `odoo-bin module install|upgrade|uninstall|list`, `odoo-bin i18n export|import|loadlang`, `odoo-bin db`, `odoo-bin neutralize`, `odoo-bin upgrade_code` (all present on 19.0 and 20.0).
- Web debug modes: `?debug=1` (technical menus and metadata), `?debug=assets` (unminified bundles), `?debug=tests` (tour launcher).

## OCA (Odoo Community Association)

`github.com/OCA` hosts hundreds of community addon repositories, each with one branch per series (`19.0`, `20.0`, …). Check there before building generic functionality.

- Conventions: manifest `version` `19.0.x.y.z`, `author` including `Odoo Community Association (OCA)`, `license` (usually AGPL-3 or LGPL-3), `maintainers`, `development_status`. Description fragments go in `readme/*.md` and `README.rst` is generated.
- Tooling: the `oca-addons-repo-template` copier template provides `pre-commit` with `ruff`, `pylint-odoo`, `prettier`, `oca-gen-addon-readme` and CI configuration. Run `pre-commit run -a` before committing in such repos.
- `pylint-odoo` is useful even outside OCA. It catches missing `_description`, SQL injection patterns, bad manifest keys, deprecated APIs and translation misuse.
- OCA addons are third-party code. Check their license compatibility, maintenance status and branch availability for the target series before adding a dependency.

## Version facts to re-check each release

Each autumn a new major appears. Re-run the comparison in [version deltas](version-deltas.md) against the new branch's ORM changelog and `odoo/upgrade_code/`, rather than re-crawling the whole documentation site.
