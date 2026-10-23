---
name: odoo-development
description: Develop, debug, review, test, port, install, integrate, deploy and upgrade Odoo addons and customizations (odoo.com, Community or Enterprise, Odoo Online/Odoo.sh/on-premise). Use for any Odoo work, including __manifest__.py, models/ORM, ir.access/ir.model.access security, XML views, Owl/JavaScript, QWeb reports, controllers and JSON-2/RPC integrations, odoo-bin, tests, and version migrations. Version-aware for 19.0 and 20.0.
---

# Odoo development

Odoo changes APIs, XML schemas and security models between majors, and most examples online (and in model memory) are for older versions. **The main failure mode is writing code for the wrong version.** Confirm the target before writing code, and compare it with core source on that branch.

## 1. Establish the target

Find out the **series (19.0/20.0/…), edition (Community/Enterprise), hosting (Online/Odoo.sh/on-premise), addon paths, affected apps and company setup**. Discover these locally first: server `odoo/release.py` or `odoo-bin --version`, manifests' `version`, config files, Docker image tags, CI and `requirements.txt` ([discovery](references/version-and-discovery.md)). Ask only for what you can't discover and what changes the implementation. Never silently move a project to a newer version.

Documentation links in this skill use `/documentation/20.0/`. **Replace `20.0` with the target series** before reading them.

## 2. Implement

1. Reproduce the standard workflow first. Configuration, an existing module or Studio may already cover the need ([functional workflows](references/functional-workflows.md)).
2. Find the closest core or existing module that does something similar on the target branch and follow its patterns ([ecosystem](references/ecosystem.md)).
3. Write the smallest coherent change in a custom addon: `_inherit` extension points, explicit `depends`, stable XML IDs and the repository's conventions. Use [scaffolds](references/scaffolds.md) for file shapes and [version deltas](references/version-deltas.md) for syntax.
4. Enforce rules and access on the server. Make every method handle multi-record recordsets and leave transaction control to the framework.
5. Validate on a disposable database: install/update the module, run the business action as a non-admin user, check multi-company behavior, and run the relevant tests ([testing](references/testing-and-performance.md)). Report exactly what ran. A static review is not a runtime check.
6. Deliver: target version/edition, the change, verification evidence, migration/deployment steps and remaining limits.

## 3. Avoid the common mistakes

- **Wrong-version syntax.** On 19/20: no `attrs`/`states`, no `<tree>`, no `_sql_constraints` (19 silently ignores them), no `name_get`, no `type='json'` routes, no `read_group` dict API, no `check_access_rights`. On 20: no `ir.model.access.csv`/`ir.rule`, no `get_param`, no Owl 2 `static props`/`useState`, no `fa fa-*` icons. Full list: [version deltas](references/version-deltas.md).
- Missing `_description`, a file not imported in `__init__.py`, or a data file missing from the manifest `data` list (or listed in the wrong order: groups → access → actions → views → menus).
- New model or wizard without access rows, so it is invisible to everyone but the superuser.
- Treating view `invisible`/`readonly`, menu `groups` or action domains as security. They only hide things; server access and `groups=` on fields enforce.
- `sudo()` widening access beyond the case that needs it, or `browse(id)` from input without `exists()` plus an access check.
- Business rules only in `@api.onchange`. Imports, RPC and code bypass onchange, so use constraints or `create`/`write` logic.
- `self.ensure_one()` missing where a singleton is assumed, or a per-record `search()`/`write()` inside a loop (N+1 queries).
- `cr.commit()` / `cr.rollback()` in business code. In crons, use `_commit_progress`.
- Raw SQL without `SQL(...)` parameters, or without flush/invalidate around it.
- `noupdate="1"` data that you then expect `-u` to refresh, or renaming XML IDs without a migration.
- Tests relying on demo data (off by default on 19+), or only running as admin.
- Copying Enterprise code into a custom addon, or picking a manifest `license` that conflicts with its dependencies.

## 4. Read only the relevant reference

| Task | Reference |
| --- | --- |
| Syntax/API differences 18→19→20, legacy patterns, `upgrade_code` | [Version deltas](references/version-deltas.md) |
| Ready-to-adapt manifest, model, security, views, wizard, cron, controller, Owl, tests, migration | [Scaffolds](references/scaffolds.md) |
| Target detection, conflicting documentation | [Version and discovery](references/version-and-discovery.md) |
| Addons, ORM, data files, constraints, mixins, crons | [Backend](references/backend.md) |
| `ir.access`, ACLs/rules, groups, multi-company | [Security and companies](references/security-and-companies.md) |
| Views, actions, Owl, assets, QWeb, reports, website | [UI and frontend](references/ui-and-frontend.md) |
| Python/JS/tour tests, debugging, profiling | [Testing and performance](references/testing-and-performance.md) |
| Controllers, JSON-2, legacy RPC, webhooks, payments, IoT | [Integrations](references/integrations.md) |
| Installation, CLI, Odoo.sh, deployment, neutralization | [Installation and operations](references/installation-and-operations.md) |
| Module updates, migration scripts, major upgrades | [Upgrades and migrations](references/upgrades-and-migrations.md) |
| Accounting, sales, stock/MRP, HR, POS, Studio, imports | [Functional workflows](references/functional-workflows.md) |
| Core source, OCA, Docker, `scaffold`/`shell`, debug modes | [Ecosystem](references/ecosystem.md) |
| Training, certification, white-paper fit analysis | [Learning and fit analysis](references/learning-and-fit-analysis.md) |
| Licensing, Enterprise code, contracts, privacy | [Legal and licensing](references/legal-and-licensing.md) |
| Research coverage, provenance, refresh procedure | [Sources and maintenance](references/sources.md) |

[resource-catalog.json](references/resource-catalog.json) indexes about 1,000 official 20.0 documentation URLs by title. Search it to find the right page for a topic.
