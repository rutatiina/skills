# Upgrades and migrations

## Separate three operations

1. Same-major server bugfix update: replace the runtime with a compatible maintained revision and follow its documented update steps.
2. Custom module update: apply changed code/data and any versioned migration logic to an existing database.
3. Major database upgrade: transform standard/custom schemas and data, port code and validate all affected workflows.

Do not use `-u all` as a substitute for a major upgrade. Keep source revisions, dependency versions and database/filestore snapshots reproducible.

Sources: [bugfix updates](https://www.odoo.com/documentation/20.0/administration/on_premise/update.html), [database upgrade](https://www.odoo.com/documentation/20.0/administration/upgrade.html).

## Custom major-version upgrades

Review whether new standard features replace customizations. Stabilize the upgrade scope, obtain an upgraded test database, port each addon to install on a clean target database, then update it on the migrated production copy. Inspect disabled views and protected configuration as well as tracebacks. Reconcile real data and rehearse the complete cutover/restore process before production. Clarify who maintains each extra module; standard upgrade coverage does not automatically cover all custom code.

Source: [upgrade a customized database](https://www.odoo.com/documentation/20.0/developer/howtos/upgrade_custom_db.html).

Odoo's upgrade platform converts the **standard** data:

```bash
python <(curl -s https://upgrade.odoo.com/upgrade) test -d <db> -t <target-version>         # repeatable test copy
python <(curl -s https://upgrade.odoo.com/upgrade) production -d <db> -t <target-version>   # real cutover; DB unavailable meanwhile
```

The test copy has no filestore, so merge the production filestore before realistic testing. Request fresh test copies periodically, because both the upgrade scripts and your database change over time. On Odoo.sh, request the upgrade from the project's Upgrade tab on a staging branch. Each push then restores the upgraded backup and updates your custom modules; check `~/logs/upgrade.log`. Production changes made after the upload are lost, so freeze production use during the cutover.

Port the **code** in a separate step: run `odoo-bin upgrade_code --from <old-series>` from the target checkout ([version deltas](version-deltas.md#automated-code-rewrites)), then fix the remaining items by hand from the deltas table, and make each addon install on an empty target database before updating it on the upgraded copy.

Recommended verification includes record counts/external IDs, balances and open items, stock quantities/valuation, taxes, company isolation, attachments, reports, scheduled jobs, webhooks and integrations. Select actual affected domains rather than treating every upgrade as an identical checklist.

## Versioned scripts

Scripts live under `module/upgrades/<full-module-version>/` (or `migrations/`) and use `pre-*.py`, `post-*.py`, `end-*.py` with `migrate(cr, version)`. Pre runs before module loading, post after the module/dependencies, end after all modules for that version. Lexical names control order within phases. Scripts normally run on module update, with a directory version above the installed version and at or below the new version. Fresh installation is not the same execution path.

Source: [upgrade scripts](https://www.odoo.com/documentation/20.0/developer/reference/upgrades/upgrade_scripts.html).

Use supported `odoo.upgrade.util` helpers for renames, reference preservation and controlled recomputation rather than ad hoc destructive changes. Check the helper version/signature and install it through supported upgrade paths/dependencies. Module operations can require execution before base loading. Respect `noupdate`; use deliberate update helpers for protected records.

Source: [upgrade utilities](https://www.odoo.com/documentation/20.0/developer/reference/upgrades/upgrade_utils.html).

Test migration outcomes against known source data, including meaningful invariants before/after, and repeat from a fresh backup to establish reproducibility. Prefer bounded transformations with observable results; document any non-repeatable assumption or external side effect.

Source: [upgrade testing utilities](https://www.odoo.com/documentation/20.0/developer/reference/upgrades/upgrade_utils.html).

The CLI's `upgrade_code` transforms code for supported changes; it does not perform the business-data upgrade or prove semantic compatibility. Current `--reinit` reloads data in installation mode, can ignore protection and is intended for debugging/development, not production recovery.

Source: [CLI](https://www.odoo.com/documentation/20.0/developer/reference/cli.html).
