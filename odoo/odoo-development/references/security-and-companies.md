# Security and companies

## Match the security system

**Odoo 20:** `ir.access` combines permission and record-domain definitions. Group entries grant listed operations for matching records. A blank group creates a global restriction, not an anonymous grant. Group grants union; global restrictions intersect. Operations use a subset of `crud` (create/read/update/delete). Example schema:

```csv
id,name,model_id,group_id/id,operation,domain
acme_case_company,Cases: multi-company,acme.case,,crud,"[('company_id', 'in', company_ids)]"
access_acme_case_user,Cases: own,acme.case,acme_case.group_acme_case_user,cru,"[('user_id', '=', user.id)]"
access_acme_case_manager,Cases: manager,acme.case,acme_case.group_acme_case_manager,crud,
```

As in core 20.0 (`addons/maintenance/security/ir.access.csv`), `model_id` holds the model's technical name, `group_id/id` holds the full XML ID, and a blank `domain` means all records. Domain variables are `user`, `company_id`, `company_ids` and `time`. 19.3 also added an `access` domain operator that checks permissions on the comodel. An old group ACL + group rule pair becomes one group row carrying the rule's domain. An old global rule becomes a blank-group row.

`odoo-bin upgrade_code --script 19.4-00-ir-access` converts existing `ir.model.access.csv` + `ir.rule` XML. It is not idempotent and needs the module's complete initial data. Review its output row by row. Never convert a blank-group old ACL by hand, because its meaning flips from "everyone may" to "everyone is restricted to". Field `groups` enforces access; hidden controls do not. Public methods receive untrusted IDs and arguments. Limit elevation to justified operations.

Source: [20 security](https://www.odoo.com/documentation/20.0/developer/reference/backend/security.html).

**Odoo 19 and earlier applicable branches:** `ir.model.access` grants CRUD additively; no grant denies access. Blank-group ACLs apply broadly, potentially including portal/public users. `ir.rule` filters records after model access; no applicable rule adds no restriction. Global rules intersect; applicable group rules union within global limits. Operation flags select checks rather than grant access. Example older schema:

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_acme_case_user,Case user,model_acme_case,acme.group_case_user,1,1,1,0
```

Groups on 19 and 20 attach to an app through a `res.groups.privilege` record (`privilege_id`), and list members in `user_ids` (18 and earlier used `category_id` and `users`). Full files: [scaffolds](scaffolds.md).

Source: [19 security](https://www.odoo.com/documentation/19.0/developer/reference/backend/security.html).

## Design roles and test boundaries

Define required operations, ownership and manager/user roles first. Load groups before permissions. Implied memberships and permissions from other modules can broaden access. Authorize model actions, controllers, attachments and reports on the server; action domains only filter the UI. Test ordinary users rather than only admin.

Source: [restrict access tutorial](https://www.odoo.com/documentation/20.0/developer/tutorials/restrict_data_access.html).

Recommended cases: allowed workflow, missing role, another owner's record, another company, direct method call with unexpected IDs, sensitive fields, and portal/public access where relevant. Include positive cases to catch over-restriction.

## Model company boundaries

Decide which records are shared or company-owned. Set `company_id`, defaults, company restrictions and consistent relations. Where automatic consistency is needed, use `_check_company_auto = True` and `check_company=True` on appropriate relations, **not on `company_id` itself**. Checks can reject a shared record linked to company-specific data.

Use `with_company()` for company-dependent values and appropriate context dependencies. Distinguish active companies from all companies authorized to the user. Test A/B selected, only A selected, shared records, cross-company links and restricted operations after company switches. `sudo()` can cross isolation boundaries.

Source: [multi-company guidelines](https://www.odoo.com/documentation/20.0/developer/howtos/company.html).

Verify functional company/branch configuration rather than inferring security from names or visibility.

Source: [companies](https://www.odoo.com/documentation/20.0/applications/general/companies.html).
