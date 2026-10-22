# Version and discovery

## Inspect the project

Recommended commands, adapting paths:

```bash
rg --files -g AGENTS.md -g __manifest__.py -g release.py -g requirements.txt -g '*odoo*.conf' -g '*compose*.yml'
python3 /path/to/odoo/odoo-bin --version
python3 /path/to/odoo/odoo-bin --help
```

If dependencies are unavailable, read release files as text. Inspect source revision, image tags, service configuration, addon paths, CI and tests. Avoid exposing secrets. Separate confirmed facts from assumptions. This workspace initially contained no Odoo server or target version; the skill intentionally sets none.

Use fixed version URLs during implementation. `latest` and `master` move, and Online intermediary versions differ from on-premise majors. An Online 19.x change does not automatically exist in 19.0.

Sources: [documentation home](https://www.odoo.com/documentation/20.0/), [CLI](https://www.odoo.com/documentation/20.0/developer/reference/cli.html), [hosting](https://www.odoo.com/documentation/20.0/administration/hosting.html).

## Compatibility boundaries

| Area | Researched difference | Consequence |
| --- | --- | --- |
| Dependencies | 19.0: Python 3.10+, PostgreSQL 13+. 20.0: Python 3.12+, PostgreSQL 16+ | Use target requirements and OS instructions; check optional AI/vector dependencies separately. |
| Security | 19.0: `ir.model.access` and `ir.rule`. 20.0: unified `ir.access` | Select matching CSV headers, models and permission semantics. |
| Test defaults | 18.0: `standard, at_install`. 20.0: `standard, post_install` | Inspect target tags and runner behavior. |
| JSON routes | Through 18: `type='json'`; newer releases: `type='jsonrpc'` | Match route options; distinguish controllers from legacy external RPC endpoints. |
| Views | Modern versions use direct modifier expressions and `<list>` | Check target schema before porting `attrs`, `states`, `<tree>` or kanban templates. |
| External API | JSON-2 starts in 19.0 | Prefer it for compatible new integrations; isolate older adapters. |
| ORM internals | Domain, constraints/index declarations and binary representation evolve | Read the complete source-to-target changelog before porting. |

Sources: [19 installation](https://www.odoo.com/documentation/19.0/administration/on_premise/source.html), [20 installation](https://www.odoo.com/documentation/20.0/administration/on_premise/source.html), [19 security](https://www.odoo.com/documentation/19.0/developer/reference/backend/security.html), [20 security](https://www.odoo.com/documentation/20.0/developer/reference/backend/security.html), [18 tests](https://www.odoo.com/documentation/18.0/developer/reference/backend/testing.html), [20 tests](https://www.odoo.com/documentation/20.0/developer/reference/backend/testing.html), [view architectures](https://www.odoo.com/documentation/20.0/developer/reference/user_interface/view_architectures.html), [ORM changelog](https://www.odoo.com/documentation/20.0/developer/reference/backend/orm/changelog.html).

## Resolve conflicting evidence

The 20.0 source-install page retains a Python 3.10 note although its requirement/change note specifies 3.12. The 20.0 licensing page still labels its current edition sections “Odoo 19.” Verify target source and license when such inconsistencies matter.

The changelog records security consolidation in Online 19.4, binary/BinaryValue changes across 19.2–20.0 and removal of `_table_query` in 20.0. Check linked source changes before reusing old base64 or SQL-view recipes. Do not assume the documentation's older example matches a newer implementation.

Confirm checked-out and deployed revisions first. Use actual source to identify available behavior, tests to establish contracts, and report consequential discrepancies. Build compatibility layers only for identified supported versions.
