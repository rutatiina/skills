# Backend development

## Module boundary

Addons are Python packages with import files and a `__manifest__.py` dictionary. Declare dependencies for models, XML IDs, mixins and assets you use. Data loads in manifest order. Use optional integration addons when coupling otherwise independent apps. Choose deliberate license/install flags and external dependencies. Reserve lifecycle hooks for needs ordinary models/data cannot express.

Source: [manifests](https://www.odoo.com/documentation/20.0/developer/reference/backend/module.html).

Follow repository naming and layout: `models`, `security`, `views`, `data`, `wizard`, `report`, `controllers`, `static`, `tests` as needed. Import model/controller/test files explicitly. Keep stable-branch diffs focused and preserve existing style.

Source: [coding guidelines](https://www.odoo.com/documentation/20.0/contributing/development/coding_guidelines.html).

## Models and ORM

Choose persistent `Model`, temporary `TransientModel` or reusable `AbstractModel` deliberately. `_inherit` extends an existing identity; adding `_name` creates another model. `_inherits` delegates through relationships and has different lifecycle/access implications.

Sources: [models](https://www.odoo.com/documentation/20.0/developer/tutorials/server_framework_101/03_basicmodel.html), [inheritance](https://www.odoo.com/documentation/20.0/developer/tutorials/server_framework_101/12_inheritance.html).

Treat `self` as a recordset; support batches or explicitly establish a singleton. Preserve `super()` return contracts and use batch-compatible `@api.model_create_multi` overrides. `browse()` does not prove existence or authorization. Prefer `fields.Command` in Python; RPC uses command triples. Distinguish deleting records from unlinking relations. Select stored/related/computed/company-dependent fields and indexes consciously. Use Date/Datetime helpers, UTC server datetimes and compatible comparison types. Keep ORM transactions intact. Direct SQL requires parameterization, authorization analysis and correct flush/cache/recompute handling.

Source: [ORM API](https://www.odoo.com/documentation/20.0/developer/reference/backend/orm.html).

## Computation and invariants

Compute methods assign every record and declare complete dependencies. Store values only when search/reporting/persistence needs justify recomputation cost. Context-sensitive computations need context dependencies. Inverses translate edits back to source values. Onchange improves forms; imports, RPC and backend creates do not execute it as a mandatory business rule.

Source: [computed fields/onchanges](https://www.odoo.com/documentation/20.0/developer/tutorials/server_framework_101/08_compute_onchange.html).

Prefer database constraints for concurrency-sensitive integrity and Python constraints for model-level validation. Check decorator trigger limits, including fields absent from create/write. Use the target's constraint declaration API; older `_sql_constraints` examples differ from current `models.Constraint`. Clean existing data before adding uniqueness/non-null requirements.

Source: [constraints](https://www.odoo.com/documentation/20.0/developer/tutorials/server_framework_101/10_constraints.html).

Put workflow transitions in model actions that check permissions and allowed states and call standard app methods. Preserve cancellation/reversal contracts and decide how repeats behave. Keep button handlers thin; avoid forcing accounting, stock or status internals directly.

Sources: [actions tutorial](https://www.odoo.com/documentation/20.0/developer/tutorials/server_framework_101/09_actions.html), [module interactions](https://www.odoo.com/documentation/20.0/developer/tutorials/server_framework_101/13_other_module.html).

## Data lifecycle

Use stable `module.identifier` external IDs. Records and references load sequentially; dependencies must exist first. Separate business configuration from demo data. `noupdate` prevents ordinary source updates from replacing protected records. Renaming/deleting IDs can affect ownership and cleanup; migrate important configuration rather than recreating it.

Source: [data files](https://www.odoo.com/documentation/20.0/developer/reference/backend/data.html).

Reuse mixins for chatter, tracking, activities, publication and ratings; add explicit dependencies and consider notification side effects. Translate literals/templates with the target APIs, preserving placeholders and avoiding concatenated fragments.

Sources: [mixins](https://www.odoo.com/documentation/20.0/developer/reference/backend/mixins.html), [translations](https://www.odoo.com/documentation/20.0/developer/howtos/translations.html).

Process cron work in short, resumable batches using the target progress API. Current docs use `ir.cron._commit_progress()` and its remaining-time result. Framework-controlled batch commits differ from arbitrary commits in business methods. Avoid self-rescheduling and duplicate effects during retries.

Source: [scheduled actions](https://www.odoo.com/documentation/20.0/developer/reference/backend/actions.html).
