# Working Agreements

- This workspace stores AI skills grouped by domain. Keep each skill in `<domain>/<skill-name>/`, with its `SKILL.md` and supporting resources together; do not add an intermediate `skills/` directory.
- When you modify any Git-tracked files, include a suggested commit message in the final summary.
- Before every Odoo development, debugging, review, integration, installation, deployment or upgrade task, read `odoo/odoo-development/SKILL.md` and its relevant references. Establish the project's actual Odoo version, edition and hosting before applying version-specific guidance.
- The editable Odoo skill lives in `odoo/odoo-development`. `~/.claude/skills/odoo-development` and `~/.codex/skills/odoo-development` are symlinks to it, so do not copy files there. After changing it, validate it (skill-creator `quick_validate.py`) and check that its internal links resolve.
