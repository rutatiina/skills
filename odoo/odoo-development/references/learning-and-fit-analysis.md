# Learning, certification and white-paper fit analysis

## Developer learning route

For a new Odoo developer, use the setup guide and Server Framework 101: architecture, addon/package, models/fields, security, UI, relationships, computation, actions, constraints, inheritance and cross-module behavior. Then use dedicated tutorials for data, access restrictions, tests, mixins and reports. Learn the installed version's conventions through a working addon rather than assembling examples from unrelated releases.

Sources: [setup](https://www.odoo.com/documentation/20.0/developer/tutorials/setup_guide.html), [Server Framework 101](https://www.odoo.com/documentation/20.0/developer/tutorials/server_framework_101.html), [tutorial catalog](https://www.odoo.com/documentation/20.0/developer/tutorials.html).

For web work, study Owl components and a dashboard through Discover the Web Framework, then use task-specific field/view/client-action and website-theme guides. Build an extension against the target branch, register its assets and validate it in the actual web client.

Source: [web-framework tutorials](https://www.odoo.com/documentation/20.0/developer/tutorials/discover_js_framework.html).

## Functional Training Center

The researched tutorial directory listed 33 courses over three pages. Public outlines were retrieved; this research did not watch every video, complete exercises or access enrolled-only material. Use the courses to establish standard behavior and vocabulary, and use developer docs/source for technical contracts.

Directory: [page 1](https://www.odoo.com/slides/all/tag/odoo-tutorials-9), [page 2](https://www.odoo.com/slides/tag/odoo-tutorials-9/page/2), [page 3](https://www.odoo.com/slides/tag/odoo-tutorials-9/page/3).

| Work area | Useful public course |
| --- | --- |
| Initial setup and concepts | [Getting Started](https://www.odoo.com/slides/getting-started-15) |
| Commercial pipeline | [CRM](https://www.odoo.com/slides/crm-16), [Sales](https://www.odoo.com/slides/sales-17) |
| Finance | [Accounting and Invoicing](https://www.odoo.com/slides/accounting-and-invoicing-19) |
| Logistics | [Inventory](https://www.odoo.com/slides/inventory-24), [Purchase](https://www.odoo.com/slides/purchase-23) |
| Manufacturing | [MRP / Shop Floor](https://www.odoo.com/slides/mrp-manufacturing-shop-floor-29) |
| Retail and web commerce | [POS](https://www.odoo.com/slides/point-of-sale-28), [Website/eCommerce](https://www.odoo.com/slides/website-ecommerce-25) |
| Services | [Project/Timesheets](https://www.odoo.com/slides/project-timesheets-21) |
| People and approvals | [Human Resources](https://www.odoo.com/slides/human-resources-32), [Sign](https://www.odoo.com/slides/sign-61) |

Other discovered course links, titles and retrieval metadata are in `source-manifest.json` under `training`. Do not hardcode course duration or assume every course is updated to the newest server release.

## Certifications

The public listing contained versioned functional certifications. The researched Odoo 19 page describes 120 questions, 90 minutes, a 70% pass threshold, +1 correct, −0.5 incorrect and 0 unanswered. Subjects include website/eCommerce, survey/marketing/AI, CRM/sales/purchase, projects/timesheets, accounting, stock/MRP, HR, spreadsheet/knowledge, POS and Studio. The exam is tied to the account and final submission is irreversible. Recheck the current page before booking or advising on its rules.

Sources: [certification listing](https://www.odoo.com/slides/all?slide_category=certification), [19 functional certification](https://www.odoo.com/slides/odoo-19-functional-certification-502).

The Odoo 18 listing describes 125 questions; do not apply 19 rules to all exams or infer a 20 certification because documentation is at 20. Functional certification is a business-product curriculum, not evidence that custom code passed technical, security or upgrade validation. Use its subjects to identify learning gaps; do not collect paid exam answers or claim certification completion.

Source: [18 functional certification](https://www.odoo.com/slides/odoo-18-functional-certification-442).

## White papers: convert capabilities into requirements

The portal's white papers are vendor comparisons, useful as discovery prompts and gap-analysis categories. Publication dates, editions, country assumptions, feature checkmarks and prices can age independently from developer documentation. Confirm a claimed capability in the target app/version and installed modules before choosing standard configuration, Studio, an addon or an integration.

Source: [white-paper directory](https://www.odoo.com/page/odoo-white-paper).

All 18 downloads linked by the researched directory were attempted. Seventeen PDFs yielded extractable text (597 pages total); the ERP SOFTONE download was unavailable. The following table records the documents and **recommended engineering questions**, not endorsements of their current comparison claims. Exact download URLs, page counts and hashes are in `source-manifest.json` under `white-papers`.

| Paper / observed publication | Recommended requirements to investigate |
| --- | --- |
| [Accounting, 2023](https://odoocdn.com/openerp_website/static/src/pdf/WP/whitepaper-2023-accounting.pdf) | Journals, taxes, reconciliation, currencies, reporting and workflow integration. |
| [Netherlands accounting (Exact/AFAS), 2025](https://odoocdn.com/web/content/75286597?unique=7c3845c0ce605182dece952b688db4d94f1ebf24&download=true) | Local accounting workflows, electronic documents and integration boundaries. |
| [Project Management, 2026](https://www.odoo.com/web/content/130350337?unique=cf053fc5f5cd841d5764423b17550eb0cdf0c063&preview=true) | Tasks/resources, time/budget controls, collaboration and role-based reporting. |
| [CRM vs Salesforce, 2024](https://download.odoocdn.com/static/whitepaper/whitepaper-2024-crm.pdf) | Lead ownership, activities, reporting, automation and shared customer data. |
| [eCommerce, 2023](https://odoocdn.com/openerp_website/static/src/pdf/WP/whitepaper-2023-ecom.pdf) | Product/catalog, stock, prices, checkout, delivery, payment and fulfillment. |
| [Middle East eCommerce (Salla/Zid), 2024](https://odoocdn.com/web/content/53300005?unique=0fb5ed840c75cdf603ab97ee622c6556af453298&download=true) | Regional selling/payment workflows and integration requirements. |
| [Helpdesk vs Help Scout, 2024](https://download.odoocdn.com/static/whitepaper/whitepaper-2024-helpdesk.pdf) | Ticket assignment, inboxes, customer access and service workflows. |
| [HR, 2023](https://odoocdn.com/openerp_website/static/src/pdf/WP/whitepaper-2023-hr.pdf) | Employee/recruitment/time-off data, payroll scope and sensitive-field access. |
| [Inventory vs Zoho, 2024](https://download.odoocdn.com/static/whitepaper/whitepaper-2024-inventory.pdf) | Location/stock control, traceability and replenishment integration. |
| [Sales vs Salesforce, 2023](https://download.odoocdn.com/static/whitepaper/whitepaper-2023-sales.pdf) | Quotation/order conversion and connected sales processes. |
| [ERP comparison, June 2018](https://odoocdn.com/openerp_website/static/src/pdf/erp_comparison_en.pdf) | Cross-department process coverage; treat pricing/features as historical. |
| [France financial management vs Pennylane, 2026](https://odoocdn.com/web/content/131535547?unique=4d38e97bb9166a32faf0ac120f3fc2535f949659&preview=true) | Localization/e-invoicing integration; independently verify current legal requirements. |
| [India accounting vs Tally/Zoho, 2024](https://odoocdn.com/web/content/85721765?unique=e6a182ddaa178c1ec3a944c400d1bc5aad0bd79a&download=true) | Local tax/accounting workflows, reporting and supporting integrations. |
| [POS, 2023](https://odoocdn.com/openerp_website/static/src/pdf/WP/whitepaper-2023-pos.pdf) | Retail/restaurant workflow, devices, stock, accounting and payment integration. |
| [India POS, 2024](https://download.odoocdn.com/static/whitepaper/whitepaper-2024-pos-india.pdf) | Local restaurant/retail workflow, hardware and payment/tax dependencies. |
| [MRP, 2023](https://odoocdn.com/openerp_website/static/src/pdf/WP/whitepaper-2023-mrp.pdf) | BoM, planning, production, quality, stock and costing dependencies. |
| [Middle East POS (Foodics/Sapaad), 2024](https://drive.google.com/uc?export=download&id=1RQKoVyC_RKEYqgd0TaxMqWkzn41rL9E4) | Hospitality workflow, device ecosystem and integration ownership. |
| ERP SOFTONE, unavailable | Retain the discovery link; inspect the document once available before drawing conclusions. |

Recommended fit record: business need → source workflow → target-version capability → configuration/module dependency → observed gap → proposed implementation → acceptance evidence. This prevents a comparison-table feature from becoming an unnecessary custom development.
