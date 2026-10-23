# Version deltas: 18.0 → 19.0 → 20.0

Use this before writing or porting code. Rows were checked against the `odoo/odoo` source on the `18.0`, `19.0` and `20.0` branches and the ORM changelogs on 2026-10-23. On-premise 19.0 includes the Online 18.1–18.4 changes, and 20.0 includes Online 19.1–19.4. When a row matters to a change, confirm it in the checked-out core source, which beats this table and the docs.

Changelogs: [19.0](https://www.odoo.com/documentation/19.0/developer/reference/backend/orm/changelog.html), [20.0](https://www.odoo.com/documentation/20.0/developer/reference/backend/orm/changelog.html).

## Never emit on 19.0 or 20.0

These come from older examples, forums and model memory. Each one fails, warns or silently misbehaves on 19+.

| Legacy | Use instead | Changed |
| --- | --- | --- |
| `_sql_constraints = [...]` | `_x = models.Constraint('unique(x)', 'message')`, `models.Index('(a, b)')`, `models.UniqueIndex(...)` | 19.0: **ignored with only a log warning**, so the constraint silently disappears |
| `attrs="{'invisible': [...]}"`, `states="..."` | `invisible="state != 'draft'"`, `readonly=`, `required=`, `column_invisible=` Python expressions | 17.0 |
| `<tree>` root, `view_mode="tree,form"` | `<list>`, `view_mode="list,form"` | 18.0 |
| `<div class="oe_chatter">` with `message_follower_ids`/`message_ids` | `<chatter/>` after `</sheet>` | 18.0 |
| kanban `<t t-name="kanban-box">` | `<t t-name="card">` (plus optional `menu`) | 18.0 |
| `group_operator='sum'` | `aggregator='sum'` | 18.0 (deprecated, still mapped in 19) |
| `name_get()` | override `_compute_display_name()` | 17.0 |
| `_name_search()` | `_search_display_name(operator, value)` returning a `Domain`; `_rec_names_search` | 18.0 |
| `check_access_rights(op)` + `check_access_rule(op)` | `check_access(op)`, `has_access(op)`, `_filtered_access(op)` | 18.0; **removed in 20.0** |
| `read_group(domain, fields, groupby, lazy=...)` returning dicts | backend: `_read_group(domain, groupby, aggregates)` → list of tuples; UI/public: `formatted_read_group` | deprecated 19.0; 20.0 `read_group` takes the `_read_group` signature |
| `self._cr`, `self._uid`, `self._context` | `self.env.cr`, `self.env.uid`, `self.env.context` | deprecated 19.0 |
| `from odoo.osv import expression`, `expression.AND(...)` | `from odoo.fields import Domain`; `Domain('a', '=', 1) & Domain(...)`, `Domain.AND([...])` | deprecated 19.0 |
| `@route(type='json')` | `@route(type='jsonrpc')` | 19.0 |
| `user_has_groups('x.y')` | `self.env.user.has_group('x.y')` | 17.0 |
| `_("text")` in models | `self.env._("text")` (`_` still exists) | 18.0 |
| `res.groups` with `category_id` and `users` | `res.groups.privilege` record + group `privilege_id`, `user_ids` | 19.0 |
| `@api.multi`, `@api.one`, `@api.returns` boilerplate | plain recordset methods | 13.0+ |
| `t-esc`, `t-raw` | `t-out`; `Markup` for trusted HTML | 15.0+ |
| `odoo.define(...)`, `/** @odoo-module **/` everywhere | native ES modules under `static/src` (auto-transpiled) | 16.0–17.0 |
| `useService("rpc")` | `import { rpc } from "@web/core/network/rpc"` | 17.2/18.0 |
| QUnit tests | HOOT `*.test.js` in `web.assets_unit_tests` | 18.0 (no QUnit files in 20.0) |
| `cr.commit()` inside cron loops | `self.env['ir.cron']._commit_progress(n, remaining=...)` | 18.3 → 19.0 |

## 18.0 → 19.0

| Area | Change | Consequence |
| --- | --- | --- |
| Constraints and indexes | Declared as model attributes: `models.Constraint`, `models.Index`, `models.UniqueIndex`. `_sql_constraints` is no longer supported. | Port every `_sql_constraints` entry, or the uniqueness/check is lost without an error. |
| Domains | `odoo.fields.Domain` builder; `odoo.osv` deprecated; dynamic dates in domains; `=` treated like `in` during optimization. | Build domains with `Domain` and never splice user-supplied lists. |
| Grouping | `read_group` deprecated → `_read_group` / `formatted_read_group`; `GROUPING SETS` for pivots. | Port aggregation code before 20, where `read_group` changes signature. |
| RPC exposure | `@api.private` blocks RPC calls to a public-named method. | Mark helper methods that must not be callable remotely. A leading `_` also blocks RPC. |
| Access helpers | `check_access` / `has_access` / `_filtered_access` (from 18.0). Old helpers still exist in 19 but are removed in 20. | Write new code with the new helpers. |
| Groups | `res.groups.privilege` (app scope, exclusive choice in the user form); group fields `privilege_id`, `user_ids`. | Update group XML. Security is still `ir.model.access.csv` + `ir.rule` in 19. |
| Controllers | `type='json'` renamed `type='jsonrpc'`; `auth='bearer'` with API keys; `save_session=False` default for bearer. | Re-decorate overridden routes with `@route()`. |
| External API | JSON-2 `/json/2/<model>/<method>` introduced; XML-RPC/JSON-RPC deprecated. | Use JSON-2 for new integrations. |
| Cron | `_commit_progress(processed, *, remaining=None, deactivate=False)` returns the remaining seconds; the framework re-calls the job until done. | Write crons as batches. Don't hand-roll commits. |
| Demo data | Not loaded by default (18.3); `--with-demo` loads it. | Tests and fresh DBs have no demo data unless asked. Create test fixtures explicitly. |
| Env/records | `record._cr/_uid/_context` deprecated. | Use `self.env.*`. |
| Requirements | Python 3.10+, PostgreSQL 13+. | Check `requirements.txt` of the branch. |
| Tests | Default tags `standard, at_install` (core `odoo/tests/common.py`). | Tag `post_install` explicitly for tests needing all modules (all `HttpCase` tours). |
| Frontend | Owl 2.8; `static props`, `useState`, `useService`, `useRecordObserver`; HOOT tests. | Standard Owl 2 patterns apply. |

## 19.0 → 20.0

| Area | Change | Consequence |
| --- | --- | --- |
| **Security** | `ir.model.access` and `ir.rule` replaced by **`ir.access`** (`ir_rule.py` no longer exists). File `security/ir.access.csv`, header `id,name,model_id,group_id/id,operation,domain`. `model_id` is the **model name** (`acme.case`), `operation` is a subsequence of `crud`, `domain` is optional. Blank group = **global restriction** that intersects with every other access. | Rewrite security files. Never copy a blank-group 19 ACL across: in 19 it grants everyone, in 20 it restricts everyone. Express old record rules as domains on group rows, and multi-company rules as global rows. |
| Domain access operator | `access` domain operator checks comodel permissions (19.3). | Usable in `ir.access` domains. |
| Config parameters | `ir.config_parameter.get_param` / `set_param` **removed**. Typed `get_str/get_int/get_float/get_bool(key, default)` and `set_str/set_int/set_float/set_bool(key, value)`. Getters check read access. | Port every `get_param` call. Use `sudo()` only where a non-admin legitimately needs the value. |
| Grouping | Public `read_group(domain, groupby=(), aggregates=(), having=(), offset, limit, order)` returns tuples, like `_read_group`. | Old dict-based callers break. |
| Binary fields | Values are `BinaryValue` objects; base64 no longer used across the data flow; RPC format for binary changed; `BinaryValue.filename`. | Re-check every `base64.b64encode/decode` around Binary fields, attachments and integrations. |
| Website context | `request` removed from model code; use `self.env.website`. | Keep `odoo.http.request` in controllers only. |
| SQL-backed models | `Model._table_query` removed; `_auto = False` models define a `_table_sql` property returning `SQL` (often built from `self.env[...]._search(domain)` and `query.subselect(...)`). `Field.compute_sql` (19.1) makes computed fields groupable/sortable. | Port report models; copy the shape of `addons/sale/report/sale_report.py` on 20.0. The 20.0 custom-report how-to still shows `_table_query`, which is stale. |
| Field copy | Char field `name` gets "(copy)" on `copy()` by default. | Adjust tests and `copy=` overrides. |
| Translations | Simplified handling; manifest terms live in each module's own `.po`. | Regenerate `.pot` after porting. |
| Tests | Default tags **`standard, post_install`** (core source). The 20.0 testing page contradicts itself; the source is authoritative. | Tag `at_install` explicitly when needed. |
| Populate | `odoo-bin populate` CLI removed; populate script + blueprints instead. | See the 20.0 populate reference. |
| HTTP | h11-based server; `odoo/http/` is a package. | Re-test reverse-proxy, websocket and long-polling setups. |
| **Frontend: Owl 3** | 20.0 bundles Owl 3 (3.0.0-alpha at research time). Components declare `props = useProps({...})` with `t` validators (`t.string()`, `t.boolean().optional()`, `t.object()`) instead of `static props`; reactive state is `proxy({})` (also `signal`, `computed`); `useEffect(fn)` re-runs on the reactive values it reads; **templates reach component members through `this.`** (`this.props.record`, `this.state.value`, `onChange.bind="this.onChange"`), where 19 templates wrote `props.record`; services are now Owl `Plugin`s (`orm_plugin.js`). `useService("orm")` is kept as a temporary shim, and `@web/owl2/utils` provides compatibility exports. | Port every component, field widget and patch. Copy the shape of a nearby 20.0 core component, not an Owl 2 example. |
| Icons | FontAwesome / odoo-ui-icons markup replaced by **Material Symbols**: `<i class="fa fa-user"/>` → `<i class="oi" data-icon="person"/>`, and JS/Python icon names like `check_circle` (19.5). | Don't emit `fa fa-*` classes on 20. Look up names in core usage. |
| Search views | `date` filter range attributes (`start_month`, `end_month`, `start_year`, `end_year`) removed and rejected by the RNG. | Use a plain `<filter name="date" date="date"/>`. |
| `_rec_names_search` | Expected as a tuple: `('name', 'ref')` (19.5). | Use a tuple, not a list. |
| Kanban | Kanban can reference a separate `<card>` view with `card_id="%(module.view_xmlid)d"`; inline `<templates><t t-name="card">` remains. | Inherit the right view when extending a card. |
| Requirements | Python 3.12+ (core uses PEP 695 generics), PostgreSQL 16+. | Upgrade runtimes and CI images. |
| External API | Legacy database service removed; common/object services scheduled for removal in 22. | Move integrations to JSON-2. |

## Automated code rewrites

`odoo-bin upgrade_code` applies the scripts in core `odoo/upgrade_code/` to your addons. Run it first when porting, review the diff, and then fix the rest by hand:

```bash
odoo-bin upgrade_code --addons-path=/path/to/custom/addons --from 18.0 --dry-run   # list files to rewrite
odoo-bin upgrade_code --addons-path=/path/to/custom/addons --from 18.0             # rewrite (inside Git)
odoo-bin upgrade_code --addons-path=/path/to/custom/addons --script 19.4-00-ir-access
```

The scripts available on 20.0 cover tree→list (17.5), `_sql_constraints`→`Constraint` (18.1), `json`→`jsonrpc` routes (18.1), dynamic-date domains and deprecated properties (18.5), `t-call` (19.1), base64 in XML (19.3), **ACL/rules→`ir.access` (19.4; not idempotent, needs complete initial data)**, Material Symbols icons (19.5), tuple `_rec_names_search` (19.5), search date filters (20.0), and `owl3-migration` (templates/JS). Run them against the target branch's `odoo-bin`. They rewrite code only. They don't migrate data and don't prove the result is correct.

Both 19.0 and 20.0 provide the subcommands `odoo-bin module install|upgrade|uninstall|list|force-demo`, `i18n export|import|loadlang`, `db`, `neutralize`, `upgrade_code`, `scaffold` and `shell`. Check `odoo-bin <cmd> --help` on the target.

Source files used for verification (replace `20.0` with the target branch): `odoo/orm/models.py`, `odoo/orm/model_classes.py`, `odoo/orm/decorators.py`, `odoo/addons/base/models/ir_access.py`, `odoo/addons/base/models/ir_config_parameter.py`, `odoo/addons/base/models/ir_cron.py`, `odoo/tests/common.py`, `odoo/tools/config.py`, `addons/web/static/src/views/fields/boolean/boolean_field.js`, `addons/web/static/src/core/orm_plugin.js`, `addons/maintenance/` (security, views, models).
