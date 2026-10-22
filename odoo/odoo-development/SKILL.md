---
name: odoo-development
description: Develop, debug, review, test, install, integrate, deploy, and upgrade Odoo addons and customizations. Use for Odoo models, ORM, security, XML views, Owl/JavaScript, QWeb, business workflows, external APIs, and Odoo.sh or on-premise environments. Consult for every Odoo development task and match guidance to the project's exact version and edition.
---

# Odoo development

Consult this skill whenever developing for Odoo. It synthesizes the seven areas linked from [Odoo's documentation portal](https://www.odoo.com/page/docs), researched **2026-10-22**. At that date `latest` resolved to **20.0**. This is a research baseline, not the default version for a project.

## Establish the target before writing code

Inspect repository instructions, server source/version, addon manifests, configuration and tests. Establish **major/minor version, Community/Enterprise, hosting, addon paths, affected apps, company boundaries and business outcome**. A custom module's version alone is not conclusive. Ask only for missing information that materially affects implementation and cannot be discovered locally.

Read [version-and-discovery.md](references/version-and-discovery.md) for compatibility decisions. Use matching official documentation and core code before relying on a signature, XML ID or extension hook. Never silently move a project to the research baseline. Odoo 20 changes security records and test defaults.

## Implement a maintainable extension

1. Reproduce the standard workflow with representative data. Check configuration and installed modules before designing custom behavior. Use [functional-workflows.md](references/functional-workflows.md) for business invariants and acceptance cases.
2. Implement the smallest coherent addon change using extension points, explicit dependencies, stable external IDs and repository conventions. Customer extensions normally belong in custom addons; core fixes follow the task's scope.
3. Enforce access on the server, preserve multi-record semantics and respect framework transactions. UI visibility and domains do not enforce authorization.
4. Validate the affected boundary: install/update, business action, roles/companies, UI or integration. Use a disposable database. Run applicable required checks and report what actually ran; static review is not runtime validation.
5. Deliver the target version/edition, change, verification, migration or operational requirements and limitations. Include a suggested commit message when modifying Git-tracked files.

These are engineering recommendations synthesized for this skill, not authorization to publish, deploy, charge for services, contact others or modify production data.

## Read only the relevant references

| Task | Reference |
| --- | --- |
| Target detection, compatibility, conflicting documentation | [Version and discovery](references/version-and-discovery.md) |
| Addons, manifests, models, ORM, data, constraints, mixins | [Backend](references/backend.md) |
| `ir.access`, older ACLs/rules, roles, multi-company | [Security and companies](references/security-and-companies.md) |
| Views, actions, Owl, assets, QWeb, reports, website | [UI and frontend](references/ui-and-frontend.md) |
| Python/JS/browser tests, debugging, profiling | [Testing and performance](references/testing-and-performance.md) |
| Controllers, JSON-2, legacy RPC, webhooks, devices | [Integrations](references/integrations.md) |
| Installation, configuration, Odoo.sh, deployment | [Installation and operations](references/installation-and-operations.md) |
| Updates, schema/data migrations, major upgrades | [Upgrades and migrations](references/upgrades-and-migrations.md) |
| Accounting, sales, stock/MRP, HR, services, Studio | [Functional workflows](references/functional-workflows.md) |
| Training, certification, white-paper fit analysis | [Learning and fit analysis](references/learning-and-fit-analysis.md) |
| Licensing, Enterprise/custom code, privacy/contracts | [Legal and licensing](references/legal-and-licensing.md) |
| Research coverage, provenance, gaps, refresh | [Sources and maintenance](references/sources.md) |

Distinguish official API facts from recommended practice. References contain direct source links. [source-manifest.json](references/source-manifest.json) records retrieval results and hashes; [resource-catalog.json](references/resource-catalog.json) indexes discovered documentation links. Successful retrieval does not establish that every page or whole course was studied. See the coverage statement.

For a read-only source check:

```bash
python3 scripts/check_sources.py --category developer --limit 10
```

This reports redirects, failures, HTML refreshes and content changes; it does not update knowledge automatically. Re-read changed sources before revising guidance. Verify current hosting capabilities, dependencies, API removal dates, certification rules and legal terms at time of use.
