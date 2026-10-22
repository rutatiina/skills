# Functional workflows and acceptance cases

These are recommended development checks derived from the app guides. They help select the business behavior to preserve; they do not replace version-specific manuals or establish country-specific compliance.

## Scope the business change

Record actors, source documents, required configuration, state transitions, generated documents and reporting effects. Determine what standard modules already provide. Exercise a successful flow plus relevant partial, cancellation, return, duplicate and cross-company cases. Prefer standard business methods over directly modifying derived state, balances or quantities.

| Domain | Invariants and useful acceptance cases | Official guide |
| --- | --- | --- |
| CRM | Lead/opportunity ownership, team access, activity deadlines, stage changes and conversion into a quotation; distinguish pipeline reporting from confirmed sales. | [CRM](https://www.odoo.com/documentation/20.0/applications/sales/crm.html) |
| Sales | Quotation → confirmation → delivery/service → invoice/payment; preserve prices, discounts, UoM, fiscal position, tax and company context. | [Sales](https://www.odoo.com/documentation/20.0/applications/sales/sales.html) |
| Invoicing policy | Ordered versus delivered quantities change when and how much can be invoiced. Include partial delivery, down payment, refund and cancellation where affected. | [Invoicing policy](https://www.odoo.com/documentation/20.0/applications/sales/sales/invoicing/invoicing_policy.html) |
| Purchase | RFQ → PO → receipt → vendor bill; test partial receipts, units, lead times and purchase/billing controls. | [Purchase](https://www.odoo.com/documentation/20.0/applications/inventory_and_mrp/purchase.html) |
| Inventory | Products, locations, routes, reservations, moves, lots/serials, packages, owners and UoM influence stock. Test partials/backorders, returns and traceability; preserve valuation effects. | [Inventory](https://www.odoo.com/documentation/20.0/applications/inventory_and_mrp/inventory.html) |
| Manufacturing | BoM, component availability/consumption, work orders, finished goods, scrap/byproducts and costing; check subcontracting or variant behavior when relevant. | [Manufacturing](https://www.odoo.com/documentation/20.0/applications/inventory_and_mrp/manufacturing.html) |
| Quality/PLM | Quality checks and failures, engineering changes, BoM revisions and approval effects; prevent bypassing controlled transitions. | [Quality](https://www.odoo.com/documentation/20.0/applications/inventory_and_mrp/quality.html), [PLM](https://www.odoo.com/documentation/20.0/applications/inventory_and_mrp/plm.html) |
| Maintenance/repairs | Equipment maintenance scheduling and repair consumption/returns affect operations and stock; test resource and material availability. | [Maintenance](https://www.odoo.com/documentation/20.0/applications/inventory_and_mrp/maintenance.html), [Repairs](https://www.odoo.com/documentation/20.0/applications/inventory_and_mrp/repairs.html) |
| POS | Session/order lifecycle, payments/refunds, stock, accounting and peripherals; verify reconnect/offline synchronization where the change touches it. | [POS](https://www.odoo.com/documentation/20.0/applications/sales/point_of_sale.html) |
| Website/eCommerce | Publication, websites/languages, variants, cart/pricelist/tax/shipping, payment status and fulfillment; test anonymous/portal access separately. | [Website](https://www.odoo.com/documentation/20.0/applications/websites/website.html), [eCommerce](https://www.odoo.com/documentation/20.0/applications/websites/ecommerce.html) |
| Project/timesheets/helpdesk | Tasks/tickets, team/customer access, timesheets, analytic accounts, billable rates and service invoicing; verify approvals and SLA measurements when affected. | [Project](https://www.odoo.com/documentation/20.0/applications/services/project.html), [Timesheets](https://www.odoo.com/documentation/20.0/applications/services/timesheets.html), [Helpdesk](https://www.odoo.com/documentation/20.0/applications/services/helpdesk.html) |
| HR | Employee/private contact visibility, contracts, attendance/time off and payroll inputs; validate effective dates and role/company boundaries. Payroll rules are localization-specific. | [Employees](https://www.odoo.com/documentation/20.0/applications/hr/employees.html), [Payroll](https://www.odoo.com/documentation/20.0/applications/hr/payroll.html), [Time off](https://www.odoo.com/documentation/20.0/applications/hr/time_off.html) |
| Marketing | Audience, consent/unsubscribe, campaign triggers, duplication and outbound side effects; test on neutralized or sandbox data. | [Email marketing](https://www.odoo.com/documentation/20.0/applications/marketing/email_marketing.html), [Automation](https://www.odoo.com/documentation/20.0/applications/marketing/marketing_automation.html) |
| Productivity | Shared documents/knowledge and spreadsheets can expose linked business data; verify ownership, sharing and live-data permissions. | [Knowledge](https://www.odoo.com/documentation/20.0/applications/productivity/knowledge.html), [Spreadsheet](https://www.odoo.com/documentation/20.0/applications/productivity/spreadsheet.html) |

## Accounting deserves explicit invariants

Establish company, chart of accounts, journals, taxes, fiscal positions, currency and opening data before evaluating a customization. Preserve balanced double-entry postings, document sequence/state, receivable/payable behavior and valuation links. Reconcile opening entries and balances when importing existing operations.

Sources: [accounting overview](https://www.odoo.com/documentation/20.0/applications/finance/accounting.html), [getting started](https://www.odoo.com/documentation/20.0/applications/finance/accounting/get_started.html).

Distinguish draft/posted invoices and bills from payments and reconciliation. Test payment terms, partial payments, credit notes/refunds, exchange differences and taxes when affected. Never infer a paid accounting state merely from a web callback or a field assignment.

Sources: [customer invoices](https://www.odoo.com/documentation/20.0/applications/finance/accounting/customer_invoices.html), [vendor bills](https://www.odoo.com/documentation/20.0/applications/finance/accounting/vendor_bills.html), [payments](https://www.odoo.com/documentation/20.0/applications/finance/accounting/payments.html), [taxes](https://www.odoo.com/documentation/20.0/applications/finance/accounting/taxes.html).

Select the actual jurisdiction's fiscal localization and verify its current requirements separately. Localizations provide country-specific configuration; they are not proof that an arbitrary customization, report or deployment is compliant. Country-specific payroll, e-invoicing and accounting changes require current authoritative verification.

Sources: [fiscal localizations](https://www.odoo.com/documentation/20.0/applications/finance/fiscal_localizations.html), [localization development](https://www.odoo.com/documentation/20.0/developer/howtos/accounting_localization.html).

## Studio and data imports

Evaluate whether configuration or Studio meets the business requirement within the selected hosting/plan. Studio can alter fields, views, automations, reports and security; exportable customization and arbitrary server Python addons have different capabilities. For a code-managed addon, inspect existing Studio changes before introducing overlapping fields/views or duplicate automations.

Sources: [Studio](https://www.odoo.com/documentation/20.0/applications/studio.html), [models/modules/apps](https://www.odoo.com/documentation/20.0/applications/studio/models_modules_apps.html), [automation rules](https://www.odoo.com/documentation/20.0/applications/studio/automated_actions.html).

Use stable external IDs for repeatable imports and relational mapping; distinguish database IDs from external IDs. Validate field mapping, date formats, units, currencies, companies and required reference data. Test representative rows before a bulk import and verify updates do not create duplicates. Imports can trigger real workflow/notification effects and are not automatically reversible.

Source: [export/import](https://www.odoo.com/documentation/20.0/applications/general/odoo_basics/export-data.html).

Use developer mode to inspect technical metadata while reproducing the actual user's permissions; developer mode itself is not a role or permission bypass.

Sources: [developer mode](https://www.odoo.com/documentation/20.0/applications/general/developer_mode.html), [access-rights administration](https://www.odoo.com/documentation/20.0/applications/general/users/access_rights.html).
