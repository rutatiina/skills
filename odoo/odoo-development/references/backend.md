# Backend development

Shapes to copy are in [scaffolds](scaffolds.md), and version-specific syntax is in [version deltas](version-deltas.md). This page covers the rules behind them.

## Module boundary

- An addon is a Python package with `__init__.py` and `__manifest__.py`. Every model/controller/wizard file must be imported, and every data file must be listed in `data` (or in `demo`). Files load **in manifest order**, and anything referenced must already exist: groups → access → data → actions/wizards → views → menus.
- `depends` must list every module whose models, XML IDs, mixins or assets you use. A missing dependency works by accident in a full database and breaks in a clean install or test run. Use a small bridge module (`acme_case_sale`) to couple two otherwise independent apps.
- Manifest version format is `<series>.<major>.<minor>.<patch>` (e.g. `19.0.1.0.0`). Bump it when an upgrade script must run. On Odoo.sh a bump also triggers the module update.
- Set `license` deliberately (LGPL-3 is the norm for Community dependencies; check [licensing](legal-and-licensing.md)). Use `external_dependencies` for Python/binary requirements. Keep lifecycle hooks (`pre_init_hook`, `post_init_hook`, `uninstall_hook`) for things data files can't express.
- Naming convention (Odoo guidelines): one file per main model (`models/acme_case.py`), views in `views/<model>_views.xml`, XML IDs `<model>_view_form|list|search`, `<model>_action`, `<module>_menu_*`, `group_<module>_<role>`.

Sources: [manifests](https://www.odoo.com/documentation/20.0/developer/reference/backend/module.html), [coding guidelines](https://www.odoo.com/documentation/20.0/contributing/development/coding_guidelines.html).

## Models and inheritance

- `models.Model` (persistent), `models.TransientModel` (wizards; vacuumed periodically, still needs access rows) and `models.AbstractModel` (mixins, report helpers). Always set `_description`.
- `_inherit = 'x'` without `_name` extends model `x` in place. `_name = 'y'` + `_inherit = 'x'` creates a new model copying `x`. `_inherits = {'x': 'x_id'}` delegates fields through a required many2one.
- Override with `super()` and return its result. `create` overrides take `vals_list` with `@api.model_create_multi`. Use `@api.ondelete(at_uninstall=False)` for delete guards instead of overriding `unlink` with raise logic.
- Use `_compute_display_name` and `_search_display_name` / `_rec_names_search` (a tuple on 20) for naming.

Sources: [ORM API](https://www.odoo.com/documentation/20.0/developer/reference/backend/orm.html), [inheritance tutorial](https://www.odoo.com/documentation/20.0/developer/tutorials/server_framework_101/12_inheritance.html).

## Recordsets and the environment

- `self` is a recordset of zero or more records. Loop, or call `self.ensure_one()` when a singleton is required. Prefer batch operations (`records.write(vals)`, `mapped`, `filtered`, `grouped`) over per-record `search`/`write` in loops.
- Use `self.env.cr`, `self.env.uid`, `self.env.context`, `self.env.user`, `self.env.company` (selected company), `self.env.companies` (active companies). `self._cr/_uid/_context` are deprecated since 19.
- `browse(ids)` proves neither existence nor access. Use `.exists()` and `check_access('read'|'write'|'create'|'unlink')` / `has_access(...)` / `_filtered_access(...)`.
- `sudo()` bypasses access rules and record rules. Use it narrowly, after you have validated the caller's right to perform the business action, and never on caller-supplied domains or field names.
- `with_context(...)`, `with_user(...)` and `with_company(...)` return new environments, so they don't mutate `self`.
- x2many writes in Python use `fields.Command` (`Command.create(vals)`, `Command.link(id)`, `Command.set(ids)`, `Command.unlink(id)`, `Command.clear()`). RPC uses the raw tuples.
- Domains: build them with `from odoo.fields import Domain`, using `Domain('state', '=', 'done') & Domain('company_id', 'in', ids)` or `Domain.AND([...])`. Never splice user-supplied lists into a domain.
- Grouped reads: `_read_group(domain, groupby=['partner_id'], aggregates=['amount:sum', '__count'])` returns tuples with records for many2one groups. `formatted_read_group` is for UI/public use. Don't use the old dict `read_group`.
- Dates: `fields.Date.today()`, `fields.Datetime.now()` (UTC, naive), `fields.Datetime.add/subtract`, `fields.Date.context_today(record)` for the user's timezone.

## Fields, computes and constraints

- Computes must assign a value to every record in `self`, and `@api.depends` must list every stored path read, including dotted paths. Add `store=True` only when search, grouping or reporting needs it, since every dependency change then triggers recomputation. `@api.depends_context('company')` covers context-dependent values. Add `inverse=` to make computed fields editable, and `search=` to make non-stored computed fields searchable.
- `@api.onchange` only runs in the form UI. Imports, RPC and code bypass it, so business invariants belong in constraints or `create`/`write`.
- Integrity: `_x = models.Constraint('unique(a, company_id)', msg)` / `models.Constraint('CHECK (qty >= 0)', msg)` / `models.Index('(a, b)')` on 19+. `_sql_constraints` is ignored on 19+. Clean existing data before adding unique or not-null constraints. `@api.constrains('f1', 'f2')` runs only when those fields are written. It does not run for fields absent from `create` vals, and does not follow dotted paths.
- Relational options: `ondelete='cascade'|'restrict'|'set null'`, `index=True` on frequently searched many2ones, `check_company=True` for company-consistent relations, `copy=False` for references/sequences, `tracking=True` with `mail.thread`.
- `company_dependent=True` stores per-company values (JSONB from 18). Read them under `with_company()`.

Sources: [computed fields](https://www.odoo.com/documentation/20.0/developer/tutorials/server_framework_101/08_compute_onchange.html), [constraints](https://www.odoo.com/documentation/20.0/developer/tutorials/server_framework_101/10_constraints.html).

## Business actions, errors and messages

- Button and RPC entry points are public methods (no leading `_`). Check the allowed state and role inside the method, keep the method thin, and call the standard app methods (`action_confirm`, `action_post`, `_action_done`, …) rather than writing derived state, quantities or accounting lines directly. Mark helper methods with a public name `@api.private` (19+) so they can't be called over RPC.
- Raise `UserError` (business refusal), `ValidationError` (constraint failure), `AccessError` (permission) or `RedirectWarning`, from `odoo.exceptions`. Translate messages with `self.env._("Text %s", value)`. Pass values as arguments; never concatenate translated fragments.
- Log with `_logger = logging.getLogger(__name__)`. Never log credentials or personal data.
- `mail.thread`: `message_post(body=..., subtype_xmlid='mail.mt_note')`. A plain-string body is escaped; use `Markup` for trusted HTML. Use `activity_schedule('mail.mail_activity_data_todo', user_id=...)` for activities. Use `mail.template` records + `template.send_mail(res_id)` for emails, and test them with outgoing mail neutralized.
- Sequences: an `ir.sequence` data record with `code`, then `self.env['ir.sequence'].next_by_code('code')` in `create`.
- Config parameters (`ir.config_parameter`): `get_param`/`set_param` on 19, typed `get_str/get_int/get_bool/get_float` + `set_*` on 20. Expose them in settings through a `res.config.settings` field with `config_parameter='module.key'`.

Sources: [actions tutorial](https://www.odoo.com/documentation/20.0/developer/tutorials/server_framework_101/09_actions.html), [module interactions](https://www.odoo.com/documentation/20.0/developer/tutorials/server_framework_101/13_other_module.html), [mixins](https://www.odoo.com/documentation/20.0/developer/reference/backend/mixins.html), [translations](https://www.odoo.com/documentation/20.0/developer/howtos/translations.html).

## Data files

- External IDs: refer to them as `module.identifier`. Use `env.ref('module.xmlid')` in code and `ref="..."`/`%(xmlid)d` in XML. Renaming or deleting an XML ID orphans or deletes the record on update, so migrate it instead.
- `noupdate="1"` records (rules, sequences, crons, default configuration) are created once and not overwritten by `-u`. To change them later, write an upgrade script or use `util.update_record_from_xml`.
- Keep demo data in `demo` and never let business logic depend on it.
- Translations (19/20): `odoo-bin i18n export -c dev.conf -d dev acme_case` writes `acme_case/i18n/acme_case.pot` (use `-l fr` for a language `.po`). `odoo-bin i18n import` and `odoo-bin i18n loadlang` also exist. Older versions use `--i18n-export`.

Source: [data files](https://www.odoo.com/documentation/20.0/developer/reference/backend/data.html).

## Crons and SQL

- Crons process one bounded batch per call and report progress with `self.env['ir.cron']._commit_progress(processed, remaining=...)`, which returns the remaining seconds. The framework commits and calls the job again until nothing remains. Don't call `cr.commit()` yourself, and make retries idempotent. Three consecutive failures count as a failed run, and repeated failures deactivate the cron.
- Raw SQL: use `from odoo.tools import SQL` (`self.env.cr.execute(SQL("... WHERE id = %s", rec_id))`), call `flush_model([...])` before reading what the ORM may not have written yet, and `invalidate_model([...])` after writing behind the ORM's back. Analyse the access implications, since SQL bypasses all rules.

Source: [scheduled actions](https://www.odoo.com/documentation/20.0/developer/reference/backend/actions.html), [security pitfalls](https://www.odoo.com/documentation/20.0/developer/reference/backend/security.html).
