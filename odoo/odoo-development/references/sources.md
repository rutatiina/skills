# Sources, coverage and maintenance

## Research scope

Researched on **2026-10-22**, starting from [Odoo Documentation](https://www.odoo.com/page/docs). The seven portal links were inspected. `latest` resolved to **20.0**. Version 19 and 18 pages were also consulted to establish compatibility boundaries.

This is a comprehensive, curated development skill, **not a claim to have read every page, watched every video, completed every course or reviewed every historical legal agreement**. User-guide coverage selects representative workflows and app-family indexes; developer and administration material was retrieved broadly and relevant sections synthesized. The manifest distinguishes retrieval from incorporation into guidance.

| Portal area | Research performed | Skill reference |
| --- | --- | --- |
| User Guides | App-family indexes and selected business/setup/import guides | [Functional workflows](functional-workflows.md) |
| White Papers | Directory, all 18 download attempts; 17 PDFs with extracted text (597 pages), one unavailable document | [Learning and fit analysis](learning-and-fit-analysis.md) |
| Developer Guide | Tutorial/how-to/reference navigation, backend/frontend/security/testing/API/upgrade material; selected older-version comparisons | [Backend](backend.md), [frontend](ui-and-frontend.md), [security](security-and-companies.md), [tests](testing-and-performance.md), [integrations](integrations.md) |
| Installation | Source/packages, deployment, hosting, Odoo.sh, neutralization, updates/support and upgrade guides | [Operations](installation-and-operations.md), [upgrades](upgrades-and-migrations.md) |
| Training Center | Three catalog pages and public course outlines; no claim to viewing all videos or completing exercises | [Learning](learning-and-fit-analysis.md) |
| Certifications | Public listing and version 19/18 functional certification information; no paid exam questions or exam completion | [Certification notes](learning-and-fit-analysis.md) |
| Legal | Licensing, Enterprise/partnership/sale terms, cloud SLA, acceptable use, privacy, GDPR and CLA guidance; no legal-compliance determination | [Legal](legal-and-licensing.md) |

## Core-source verification (2026-10-23)

The review pass checked version-specific claims against `github.com/odoo/odoo` branches `18.0`, `19.0` and `20.0` (raw files and the Git tree API), the 19.0/20.0 ORM changelogs, and `github.com/odoo/owl` `doc/v3`. Results went into [version deltas](version-deltas.md) and [scaffolds](scaffolds.md):

- Confirmed: `ir.access` replaces `ir.model.access`/`ir.rule` on 20.0 (231 `ir.access.csv` files, no `ir_rule.py`); test default tags (`at_install` on 19.0, `post_install` on 20.0); `_sql_constraints` ignored with a warning since 19.0; `read_group` deprecation (19) and signature change (20); `get_param`/`set_param` removed on 20.0; `check_access_rights` removed on 20.0; Owl 2.8 on 19.0 and Owl 3 alpha on 20.0; `odoo/upgrade_code/` scripts; `odoo-bin` subcommands.
- The scaffolds are adapted from core `addons/maintenance` and `addons/web`. They were assembled into an `acme_case` module and run on the official `odoo:19.0` and `odoo:20.0` Docker images (plus Chromium and `websocket-client`) with PostgreSQL 16. Install succeeded, the views passed schema validation, and the 3 Python tests (sequence/compute, workflow guard, record-rule/`ir.access` isolation) and the HOOT field-widget test passed on both versions. The controller, wizard button flow, cron and upgrade script were loaded but not exercised. The upgrade script needs `odoo/upgrade-util`, which the images don't include.

## Retrieval inventory

The manifest contains **274 retrieval records**: **267 content responses**, **5 HTML redirect stubs**, and **2 unavailable URLs**. The two unavailable URLs are attempts to access the same SOFTONE white paper. The resource catalog contains **996 discovered documentation URLs**, not that many reviewed pages.

| Retrieval category | Records |
| --- | --- |
| certifications | 3 |
| developer | 119 |
| installation | 28 |
| legal | 13 |
| portal | 2 |
| training | 37 |
| user-guides | 52 |
| white-papers | 20 |

## Known gaps and inconsistencies

- The ERP SOFTONE download linked by the white-paper directory returned HTTP 404. A second official content URL also failed. Keep it marked unavailable; do not infer its contents from a search snippet.
- Several old documentation paths return HTTP 200 with an HTML meta-refresh instead of content. Manifest records include `redirect_target`, and canonical target pages were retrieved separately.
- The 20.0 source-install guide contains a stale Python 3.10 note despite its explicit 3.12 requirement. The license page retains Odoo 19 headings.
- The ORM changelog reports removal of `_table_query` while the 20.0 custom-report guide still describes it. Verify matching core code before using that recipe.
- API notices contain calendar/version wording that can evolve; preserve the distinction between removed database services, deprecated common/object services and unaffected custom controllers.
- Certification listings and training outlines have their own version cadence. The existence of 20.0 documentation does not establish a 20.0 functional exam.
- Historical agreements, every locale-specific manual, all comparison landing pages, linked third-party materials and enrolled-only training content are outside this curated synthesis.

## Reuse and refresh

Keep this workspace directory as the only editable source. `~/.claude/skills/odoo-development` (Claude Code) and `~/.codex/skills/odoo-development` (Codex) are **symlinks** to it, so edits take effect without copying. Repository and personal agent instructions direct Odoo work to the skill. Codex implicit invocation is enabled in `agents/openai.yaml`.

1. When a new major ships, diff its ORM changelog and `odoo/upgrade_code/` directory against [version deltas](version-deltas.md) first. This is the highest-value refresh.
2. Verify exact APIs and changing requirements in matching official documentation and core source.
3. Run `python3 scripts/check_sources.py --category developer --limit 10` for a read-only sample, or raise the limit to check the whole category. JSON lines go to stdout and a summary to stderr; exit 1 means a retrieval failed, exit 2 means invalid arguments.
4. A changed hash is a review candidate, not proof of a semantic edit. HTTP checks do not establish technical correctness.
5. Update the synthesis, source metadata and retrieval date together when re-researching; do not merely replace the date.
6. Run the skill-creator validator, check internal links, and re-run `evals/evals.json` with and without the skill.

## Provenance files

- [Source manifest](source-manifest.json): requested/resolved URLs, titles/categories, retrieval state/date, response hash, PDF page count when applicable, use in written references and review scope.
- [Resource catalog](resource-catalog.json): discovered fixed-version official documentation links for targeted follow-up. It is a navigation index, not a content archive.
- No upstream manual, proprietary source, full PDF or course video is embedded in this skill; substantive guidance is paraphrased and linked.

## Entry points

- [Documentation portal](https://www.odoo.com/page/docs)
- [User Guides](https://www.odoo.com/documentation/latest/applications.html)
- [White Papers](https://www.odoo.com/page/odoo-white-paper)
- [Developer Guide](https://www.odoo.com/documentation/latest/developer.html)
- [Installation](https://www.odoo.com/documentation/latest/administration.html)
- [Training Center](https://www.odoo.com/slides/all/tag/odoo-tutorials-9)
- [Certifications](https://www.odoo.com/slides/all?slide_category=certification)
- [Legal](https://www.odoo.com/page/legal)
