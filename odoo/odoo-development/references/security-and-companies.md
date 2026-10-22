# Security and companies

## Match the security system

**Odoo 20:** `ir.access` combines permission and record-domain definitions. Group entries grant listed operations for matching records. A blank group creates a global restriction, not an anonymous grant. Group grants union; global restrictions intersect. Operations use a subset of `crud` (create/read/update/delete). Example schema:

```csv
id,name,model_id,group_id/id,operation,domain
access_acme_case_user,Case user,acme.case,acme.group_case_user,cru,[]
```

Verify target group privilege definitions and CSV converters. Never mechanically convert a blank-group old ACL: its meaning changes. Field `groups` enforces access; hidden controls do not. Public methods receive untrusted IDs/arguments. Limit elevation to justified operations.

Source: [20 security](https://www.odoo.com/documentation/20.0/developer/reference/backend/security.html).

**Odoo 19 and earlier applicable branches:** `ir.model.access` grants CRUD additively; no grant denies access. Blank-group ACLs apply broadly, potentially including portal/public users. `ir.rule` filters records after model access; no applicable rule adds no restriction. Global rules intersect; applicable group rules union within global limits. Operation flags select checks rather than grant access. Example older schema:

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_acme_case_user,Case user,model_acme_case,acme.group_case_user,1,1,1,0
```

These are version-specific illustrations, not universal scaffolds.

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
