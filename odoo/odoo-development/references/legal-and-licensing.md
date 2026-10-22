# Legal and licensing for development

Apply this reference when selecting dependencies, distributing addons, handling Enterprise code, making support promises or designing personal-data workflows. These notes identify development implications; the applicable license text and signed contract control.

## Software licenses

The researched license page describes Community 9–19 under LGPLv3 and version 8 under AGPLv3. Enterprise use/modification requires valid entitlement under its Enterprise license; authorized partner development/testing has defined conditions. Distribution of Enterprise copies or modified copies is prohibited. Odoo-authored Apps/themes default to the Odoo Proprietary License unless stated otherwise. Dependent modules may use compatible licenses under the stated conditions; that does not authorize copying protected code/assets. Third-party addon licenses must be checked individually. Choose a manifest license consistent with actual dependencies and distribution.

The `/20.0/` page still labels current edition sections 19; inspect the actual 20 source license rather than assuming this heading proves 20 coverage. Preserve required copyright/license notices.

Source: [licenses](https://www.odoo.com/documentation/20.0/legal/licenses.html).

## Contract and support boundaries

The retrieved Enterprise Agreement is version 13, dated 2026-09-24. It distinguishes Users, Light Users, portal users, Extra Modules and Covered Extra Modules. Do not assume custom addons are automatically covered for bug fixes or upgrades. Confirm maintenance ownership, subscription plan, version coverage and hosting terms before promising service. Do not disable subscription-verification mechanisms or infer that bots/employees are unbillable solely from their UI access.

Source: [Enterprise Agreement](https://www.odoo.com/documentation/20.0/legal/terms/enterprise.html).

Partnership terms govern partner privileges/obligations; they do not automatically authorize production Enterprise use or redistribution. Terms of sale affect purchases and commercial commitments. Check applicable executed terms before offering certification, hosting, support or third-party services on someone's behalf.

Sources: [Partnership Agreement](https://www.odoo.com/documentation/20.0/legal/terms/partnership.html), [Terms of Sale](https://www.odoo.com/documentation/20.0/legal/terms/terms_of_sale.html).

Cloud SLA and acceptable-use conditions constrain hosting expectations and workload behavior. Read the current service scope/exclusions before quoting availability, backup retention or guaranteed performance. Keep custom integration load bounded and account for service restrictions.

Sources: [Cloud SLA](https://www.odoo.com/cloud-sla), [acceptable use](https://www.odoo.com/acceptable-use).

## Personal data and localization

Map where personal data enters, who can access it, downstream processors/integrations, exports, retention and deletion behavior. Apply least privilege and avoid retaining secrets or personal payloads in logs and test fixtures. Reconcile deletion/anonymization requirements with legitimate accounting/audit retention rather than deleting business records indiscriminately. Confirm controller/processor responsibilities and applicable agreements for the actual hosting/integration.

Sources: [privacy policy](https://www.odoo.com/privacy), [GDPR guide](https://www.odoo.com/gdpr).

Odoo's country guides can inform localization setup but do not certify every customization or establish current legal compliance. Use the relevant country documentation and current authoritative legal/accounting requirements for jurisdiction-specific development. Do not reproduce a country tax rule from an old white paper as a universal requirement.

Sources: [legal portal](https://www.odoo.com/documentation/20.0/legal.html), [fiscal localizations](https://www.odoo.com/documentation/20.0/applications/finance/fiscal_localizations.html).

## Upstream contribution and source reuse

Check the contributor agreement and code-contribution requirements before submitting upstream. Signing an agreement is a distinct action, not implied by writing a patch. Verify ownership/permission for customer code and preserve notices when reusing source. These skill notes summarize and link official material; they do not relicense upstream documentation or include copies of proprietary modules.

Sources: [CLA](https://www.odoo.com/documentation/20.0/legal/cla.html), [contribution guide](https://www.odoo.com/documentation/20.0/contributing/development.html).
