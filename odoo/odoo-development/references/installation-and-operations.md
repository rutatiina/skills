# Installation and operations

## Choose hosting before designing customizations

| Hosting | Development implications |
| --- | --- |
| Odoo Online | Managed database with platform-specific Studio/importable customization capabilities. Do not design around deploying arbitrary Python server addons. |
| Odoo.sh | Git-driven custom addons, builds, development/staging/production lifecycle and managed infrastructure. |
| On-premise | Control of source/addons and runtime, with responsibility for dependencies, security, backups, monitoring and upgrades. |

Online intermediary releases cannot simply be restored onto on-premise or Odoo.sh major-release runtimes; check the documented transition path. Backups used for hosting transfers include the filestore.

Sources: [Online](https://www.odoo.com/documentation/20.0/administration/odoo_online.html), [hosting transitions](https://www.odoo.com/documentation/20.0/administration/hosting.html), [importable modules](https://www.odoo.com/documentation/20.0/developer/tutorials/importable_modules.html).

## Local source development

Use the exact target branch and its dependency files in an isolated environment. Enterprise contains extra addons, not a separate complete server; pair matching Community and Enterprise branches and order addon paths correctly. Create a dedicated PostgreSQL role rather than connecting Odoo as `postgres`. Verify OS libraries, optional vector support, RTL tooling and report rendering dependencies. Current 20.0 requirements are Python 3.12+/PostgreSQL 16+; older targets differ.

Source: [source installation](https://www.odoo.com/documentation/20.0/administration/on_premise/source.html).

Example local launch, after configuring a disposable database and addon paths:

```bash
python3 /path/to/odoo/odoo-bin -c /path/to/dev.conf -d acme_dev
```

Keep credentials in an appropriate secret/config mechanism with restricted access. Do not copy admin demo passwords into exposed environments. Package installations and containers use different launchers; inspect actual service/image configuration. Start with version-matched requirements rather than solving dependency errors by unconstrained upgrades.

Source: [packaged installers](https://www.odoo.com/documentation/20.0/administration/on_premise/packages.html).

Common commands (19/20, adapt the launcher):

```bash
odoo-bin -c dev.conf -d acme_dev -i acme_case --stop-after-init          # install
odoo-bin -c dev.conf -d acme_dev -u acme_case --stop-after-init          # update code/data/schema
odoo-bin -c dev.conf --dev=xml,reload,qweb                               # dev: reload Python, read views from disk
odoo-bin module list -c dev.conf -d acme_dev                             # subcommands: see `odoo-bin --help`
odoo-bin shell -c dev.conf -d acme_dev                                   # `env` in a Python shell
```

A Python change needs a server restart. A view/data change needs `-u` (or `--dev=xml` for views during development). A new field needs `-u` for the schema. JS/SCSS changes need a browser reload, or `?debug=assets` if the old bundle is cached.

## Odoo.sh behavior

Repository layout: the repository root holds the addon folders, and other addon repositories can be added as Git submodules. A root `requirements.txt` installs extra Python packages. The branch's Odoo version comes from the project/branch settings, not from your manifests.


Development builds create fresh test databases; staging uses production-derived data for functional validation; production pushes change the live runtime. A manifest version increment can trigger automatic module updates. Build success does not establish realistic data/workflow correctness. Verify configured test selection: do not assume staging runs all unit tests. Review backup/retention behavior for the relevant stage rather than assuming parity.

Source: [Odoo.sh branches](https://www.odoo.com/documentation/20.0/administration/odoo_sh/getting_started/branches.html).

Inspect build logs/status and the exact revision, dependencies and addon installation set. Use staging to exercise migration and business acceptance cases. Prepare the change and verification evidence before any production push. Verify custom Python/system dependency support in project configuration.

Sources: [builds](https://www.odoo.com/documentation/20.0/administration/odoo_sh/getting_started/builds.html), [project settings](https://www.odoo.com/documentation/20.0/administration/odoo_sh/getting_started/settings.html), [module creation](https://www.odoo.com/documentation/20.0/administration/odoo_sh/create_module.html).

## Public deployment essentials

Configure explicit database routing/filtering, disable unnecessary database listing/manager access, use HTTPS and trusted reverse-proxy settings, and route websocket traffic to the correct listener. Use non-superuser database credentials and restricted service/file access. Size workers/timeouts from measured CPU/memory/workload; documentation heuristics are starting points. Keep database **and filestore** backups outside the instance and verify restoration. Match Linux/Windows process-mode capabilities and keep software updated.

Source: [system configuration](https://www.odoo.com/documentation/20.0/administration/on_premise/deploy.html).

Recommended operational acceptance: health and application logs, outbound email, payment sandbox/live configuration, scheduled jobs, realtime features, attachment restoration and rollback procedure. An application code rollback does not automatically reverse a schema/data migration.

Email routing/gateway changes require verifying aliases, domains and delivery, including duplicates and loops; distinguish incoming gateway setup from outbound server configuration.

Source: [email gateway](https://www.odoo.com/documentation/20.0/administration/on_premise/email_gateway.html).

## Restored test databases

Neutralization disables several production integrations, including scheduled actions, outgoing mail, bank sync, payments, delivery and IAP-related behavior. Verify neutralization after restoring a copy and separately check custom connectors, which may not follow standard neutralization behavior. Keep test copies private and avoid accidental real-world effects when re-enabling a feature for validation.

Source: [neutralized databases](https://www.odoo.com/documentation/20.0/administration/neutralized_database.html).

Distinguish same-major bugfix updates from major upgrades. Check the actual support table and contractual coverage rather than hardcoding support dates.

Sources: [bugfix updates](https://www.odoo.com/documentation/20.0/administration/on_premise/update.html), [support](https://www.odoo.com/documentation/20.0/administration/standard_extended_support.html).
