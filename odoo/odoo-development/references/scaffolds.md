# Scaffolds for 19.0 and 20.0

Minimal, working shapes for a custom addon `acme_case`. They are written for **19.0**, and a `20.0:` note marks each place where 20 differs. Rename everything and drop the parts you don't need. Before relying on a pattern, compare it with a nearby core module on the same branch (`addons/maintenance` is a compact reference). See [version deltas](version-deltas.md) for why each choice is made.

Contents: [manifest](#manifest) · [models](#models) · [security 19](#security-190) · [security 20](#security-200) · [views](#views-action-menus) · [wizard](#wizard) · [sequence/cron](#data-sequence-and-cron) · [controller](#controller) · [Owl widget](#owl-field-widget-190-owl-2) · [tests](#tests) · [upgrade script](#upgrade-script)

```text
acme_case/
├── __init__.py                 # from . import models, wizard, controllers
├── __manifest__.py
├── models/{__init__,acme_case,res_partner}.py
├── wizard/{__init__,acme_case_close}.py + acme_case_close_views.xml
├── controllers/{__init__,main}.py
├── security/acme_case_security.xml + ir.model.access.csv   (20.0: ir.access.csv)
├── data/acme_case_data.xml
├── views/acme_case_views.xml, res_partner_views.xml, acme_case_menus.xml
├── static/src/hours_badge/hours_badge_field.{js,xml}
├── static/tests/hours_badge_field.test.js
├── tests/{__init__,test_acme_case}.py
└── upgrades/19.0.1.1.0/pre-migrate.py
```

Every Python file must be imported from its package's `__init__.py`, and every XML/CSV file must be listed in the manifest. A missing entry fails silently: the model, view or access simply does not exist.

## Manifest

```python
{
    'name': 'Acme Cases',
    'version': '19.0.1.0.0',          # <series>.<x>.<y>.<z>; bump to run upgrade scripts
    'summary': 'Track customer cases',
    'category': 'Services',
    'author': 'Acme',                 # omitted → install-time warning
    'license': 'LGPL-3',              # match actual dependencies/distribution
    'depends': ['mail'],
    'data': [
        'security/acme_case_security.xml',      # groups before access rows
        'security/ir.model.access.csv',         # 20.0: 'security/ir.access.csv'
        'data/acme_case_data.xml',
        'wizard/acme_case_close_views.xml',     # actions before views/buttons that use %(xmlid)d
        'views/acme_case_views.xml',
        'views/res_partner_views.xml',
        'views/acme_case_menus.xml',            # menus last
    ],
    'assets': {
        'web.assets_backend': ['acme_case/static/src/**/*'],
        'web.assets_unit_tests': ['acme_case/static/tests/**/*'],
    },
    'application': True,
}
```

## Models

```python
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.fields import Command, Domain


class AcmeCase(models.Model):
    _name = 'acme.case'
    _description = 'Customer Case'            # required; omitting it logs a warning
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'priority desc, id desc'
    _check_company_auto = True

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='/')
    subject = fields.Char(required=True, tracking=True)
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    partner_id = fields.Many2one('res.partner', required=True, check_company=True, tracking=True)
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user, check_company=True)
    state = fields.Selection(
        [('new', 'New'), ('in_progress', 'In Progress'), ('done', 'Done'), ('cancel', 'Cancelled')],
        default='new', required=True, tracking=True,
    )
    priority = fields.Selection([('0', 'Normal'), ('1', 'High')], default='0')
    line_ids = fields.One2many('acme.case.line', 'case_id')
    hours_total = fields.Float(compute='_compute_hours_total', store=True, aggregator='sum')

    _name_company_uniq = models.Constraint(
        'unique(name, company_id)',
        'The reference must be unique per company.',
    )

    @api.depends('line_ids.hours')
    def _compute_hours_total(self):
        for case in self:
            case.hours_total = sum(case.line_ids.mapped('hours'))

    @api.constrains('state', 'line_ids')
    def _check_done_has_lines(self):
        for case in self:
            if case.state == 'done' and not case.line_ids:
                raise ValidationError(self.env._("Case %s needs at least one line before it is done.", case.name))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', '/') == '/':
                vals['name'] = self.env['ir.sequence'].next_by_code('acme.case') or '/'
        return super().create(vals_list)

    @api.ondelete(at_uninstall=False)
    def _unlink_except_done(self):
        if any(case.state == 'done' for case in self):
            raise UserError(self.env._("Done cases cannot be deleted."))

    def action_start(self):                    # public: callable from buttons and RPC
        if any(case.state != 'new' for case in self):
            raise UserError(self.env._("Only new cases can be started."))
        self.write({'state': 'in_progress'})

    @api.private                               # public name, but not callable over RPC
    def build_export_payload(self):
        return [{'ref': case.name, 'hours': case.hours_total} for case in self]

    @api.model
    def _cron_cancel_stale(self, limit=200):
        cutoff = fields.Datetime.subtract(fields.Datetime.now(), days=90)
        domain = Domain('state', '=', 'new') & Domain('create_date', '<', cutoff)
        cases = self.search(domain, limit=limit)
        cases.write({'state': 'cancel'})
        remaining = 0 if len(cases) < limit else self.search_count(domain)
        self.env['ir.cron']._commit_progress(len(cases), remaining=remaining)


class AcmeCaseLine(models.Model):
    _name = 'acme.case.line'
    _description = 'Case Line'

    case_id = fields.Many2one('acme.case', required=True, ondelete='cascade', index=True)
    company_id = fields.Many2one(related='case_id.company_id', store=True)
    description = fields.Char(required=True)
    hours = fields.Float()

    _hours_positive = models.Constraint('CHECK (hours >= 0)', 'Hours cannot be negative.')
```

Extending an existing model, with a grouped count through `_read_group`, which returns tuples whose many2one values are records:

```python
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    acme_case_count = fields.Integer(compute='_compute_acme_case_count')

    def _compute_acme_case_count(self):
        counts = dict(self.env['acme.case']._read_group(
            [('partner_id', 'in', self.ids)], ['partner_id'], ['__count'],
        ))
        for partner in self:
            partner.acme_case_count = counts.get(partner, 0)
```

Config parameters:

```python
batch = int(self.env['ir.config_parameter'].sudo().get_param('acme_case.batch', 200))   # 19.0
batch = self.env['ir.config_parameter'].sudo().get_int('acme_case.batch', 200)          # 20.0
```

## Security (19.0)

`security/acme_case_security.xml`:

```xml
<odoo>
    <record id="res_groups_privilege_acme_case" model="res.groups.privilege">
        <field name="name">Cases</field>
        <field name="category_id" ref="base.module_category_services"/>
    </record>
    <record id="group_acme_case_user" model="res.groups">
        <field name="name">User</field>
        <field name="sequence">10</field>
        <field name="privilege_id" ref="res_groups_privilege_acme_case"/>
        <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
    </record>
    <record id="group_acme_case_manager" model="res.groups">
        <field name="name">Manager</field>
        <field name="sequence">20</field>
        <field name="privilege_id" ref="res_groups_privilege_acme_case"/>
        <field name="implied_ids" eval="[(4, ref('group_acme_case_user'))]"/>
        <field name="user_ids" eval="[(4, ref('base.user_admin'))]"/>
    </record>

    <data noupdate="1">
        <!-- global rule (no groups): intersects with everything -->
        <record id="acme_case_rule_company" model="ir.rule">
            <field name="name">Cases: multi-company</field>
            <field name="model_id" ref="model_acme_case"/>
            <field name="domain_force">[('company_id', 'in', company_ids)]</field>
        </record>
        <record id="acme_case_rule_user" model="ir.rule">
            <field name="name">Cases: users see their own or unassigned</field>
            <field name="model_id" ref="model_acme_case"/>
            <field name="domain_force">['|', ('user_id', '=', user.id), ('user_id', '=', False)]</field>
            <field name="groups" eval="[(4, ref('group_acme_case_user'))]"/>
        </record>
        <record id="acme_case_rule_manager" model="ir.rule">
            <field name="name">Cases: managers see all</field>
            <field name="model_id" ref="model_acme_case"/>
            <field name="domain_force">[(1, '=', 1)]</field>
            <field name="groups" eval="[(4, ref('group_acme_case_manager'))]"/>
        </record>
    </data>
</odoo>
```

`security/ir.model.access.csv`. Every model, **including TransientModel wizards**, needs a row, or no non-superuser can use it:

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_acme_case_user,acme.case user,model_acme_case,group_acme_case_user,1,1,1,0
access_acme_case_manager,acme.case manager,model_acme_case,group_acme_case_manager,1,1,1,1
access_acme_case_line_user,acme.case.line user,model_acme_case_line,group_acme_case_user,1,1,1,1
access_acme_case_close_user,acme.case.close user,model_acme_case_close,group_acme_case_user,1,1,1,0
```

## Security (20.0)

The groups XML is the same as in 19.0 **without the `ir.rule` records**. Access rows and record rules merge into `security/ir.access.csv`. In this file, `model_id` is the model name, `group_id/id` is the full XML ID, `operation` is a subsequence of `crud`, and a blank group makes the row a **global restriction**:

```csv
id,name,model_id,group_id/id,operation,domain
acme_case_company,Cases: multi-company,acme.case,,crud,"[('company_id', 'in', company_ids)]"
access_acme_case_user,Cases: own or unassigned,acme.case,acme_case.group_acme_case_user,cru,"['|', ('user_id', '=', user.id), ('user_id', '=', False)]"
access_acme_case_manager,Cases: manager,acme.case,acme_case.group_acme_case_manager,crud,
access_acme_case_line_user,Case lines: user,acme.case.line,acme_case.group_acme_case_user,crud,
access_acme_case_close_user,Close wizard: user,acme.case.close,acme_case.group_acme_case_user,cru,
```

## Views, action, menus

```xml
<odoo>
    <record id="acme_case_view_list" model="ir.ui.view">
        <field name="name">acme.case.list</field>
        <field name="model">acme.case</field>
        <field name="arch" type="xml">
            <list>
                <field name="name"/>
                <field name="subject"/>
                <field name="partner_id"/>
                <field name="user_id" widget="many2one_avatar_user"/>
                <field name="state" widget="badge" decoration-success="state == 'done'"/>
                <field name="hours_total" sum="Total"/>
                <field name="company_id" groups="base.group_multi_company"/>
            </list>
        </field>
    </record>

    <record id="acme_case_view_form" model="ir.ui.view">
        <field name="name">acme.case.form</field>
        <field name="model">acme.case</field>
        <field name="arch" type="xml">
            <form>
                <header>
                    <button name="action_start" type="object" string="Start" class="btn-primary" invisible="state != 'new'"/>
                    <button name="%(acme_case_close_action)d" type="action" string="Close" invisible="state != 'in_progress'"/>
                    <field name="state" widget="statusbar" statusbar_visible="new,in_progress,done"/>
                </header>
                <sheet>
                    <div class="oe_title"><h1><field name="name"/></h1></div>
                    <group>
                        <group>
                            <field name="subject"/>
                            <field name="partner_id"/>
                        </group>
                        <group>
                            <field name="user_id"/>
                            <field name="company_id" groups="base.group_multi_company"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Lines" name="lines">
                            <field name="line_ids" readonly="state in ('done', 'cancel')">
                                <list editable="bottom">
                                    <field name="description"/>
                                    <field name="hours" widget="acme_hours_badge"/>
                                </list>
                            </field>
                        </page>
                    </notebook>
                </sheet>
                <chatter/>
            </form>
        </field>
    </record>

    <record id="acme_case_view_search" model="ir.ui.view">
        <field name="name">acme.case.search</field>
        <field name="model">acme.case</field>
        <field name="arch" type="xml">
            <search>
                <field name="name"/>
                <field name="partner_id"/>
                <filter name="my_cases" string="My Cases" domain="[('user_id', '=', uid)]"/>
                <filter name="open" string="Open" domain="[('state', 'in', ['new', 'in_progress'])]"/>
                <separator/>
                <filter name="group_state" string="Status" context="{'group_by': 'state'}"/>
            </search>
        </field>
    </record>

    <record id="acme_case_action" model="ir.actions.act_window">
        <field name="name">Cases</field>
        <field name="res_model">acme.case</field>
        <field name="view_mode">list,form</field>
        <field name="context">{'search_default_my_cases': 1}</field>
    </record>
</odoo>
```

`views/acme_case_menus.xml`:

```xml
<odoo>
    <menuitem id="acme_case_menu_root" name="Cases" sequence="50"
              web_icon="acme_case,static/description/icon.png"
              groups="acme_case.group_acme_case_user"/>
    <menuitem id="acme_case_menu_cases" parent="acme_case_menu_root" action="acme_case_action" sequence="10"/>
</odoo>
```

Inheriting a core view. Anchor on a stable `name` or attribute, never on a label string or position:

```xml
<record id="view_partner_form_inherit_acme_case" model="ir.ui.view">
    <field name="name">res.partner.form.inherit.acme_case</field>
    <field name="model">res.partner</field>
    <field name="inherit_id" ref="base.view_partner_form"/>
    <field name="arch" type="xml">
        <xpath expr="//field[@name='vat']" position="after">
            <field name="acme_case_count" groups="acme_case.group_acme_case_user"/>
        </xpath>
    </field>
</record>
```

Kanban (19 and 20): `<kanban><templates><t t-name="card">…</t></templates></kanban>`. In 20.0, a kanban view can instead point to a separate `<card>` view with `card_id="%(acme_case_view_card)d"`.

## Wizard

```python
from odoo import fields, models
from odoo.fields import Command


class AcmeCaseClose(models.TransientModel):
    _name = 'acme.case.close'
    _description = 'Close Cases'

    case_ids = fields.Many2many(
        'acme.case', default=lambda self: [Command.set(self.env.context.get('active_ids', []))],
    )
    resolution = fields.Text(required=True)

    def action_close(self):
        for case in self.case_ids:
            case.message_post(body=self.resolution)
        self.case_ids.write({'state': 'done'})
        return {'type': 'ir.actions.act_window_close'}
```

```xml
<odoo>
    <record id="acme_case_close_view_form" model="ir.ui.view">
        <field name="name">acme.case.close.form</field>
        <field name="model">acme.case.close</field>
        <field name="arch" type="xml">
            <form>
                <group><field name="resolution"/></group>
                <footer>
                    <button name="action_close" type="object" string="Close Cases" class="btn-primary"/>
                    <button special="cancel" string="Cancel"/>
                </footer>
            </form>
        </field>
    </record>
    <record id="acme_case_close_action" model="ir.actions.act_window">
        <field name="name">Close Cases</field>
        <field name="res_model">acme.case.close</field>
        <field name="view_mode">form</field>
        <field name="target">new</field>
        <field name="binding_model_id" ref="model_acme_case"/>
        <field name="binding_view_types">list</field>
    </record>
</odoo>
```

## Data: sequence and cron

```xml
<odoo>
    <data noupdate="1">
        <record id="seq_acme_case" model="ir.sequence">
            <field name="name">Case</field>
            <field name="code">acme.case</field>
            <field name="prefix">CASE/%(year)s/</field>
            <field name="padding">5</field>
            <field name="company_id" eval="False"/>
        </record>
        <record id="ir_cron_acme_case_cancel_stale" model="ir.cron">
            <field name="name">Cases: cancel stale cases</field>
            <field name="model_id" ref="model_acme_case"/>
            <field name="state">code</field>
            <field name="code">model._cron_cancel_stale()</field>
            <field name="user_id" ref="base.user_root"/>
            <field name="interval_number">1</field>
            <field name="interval_type">days</field>
        </record>
    </data>
</odoo>
```

## Controller

```python
from werkzeug.exceptions import NotFound

from odoo import http
from odoo.http import request


class AcmeCaseController(http.Controller):

    @http.route('/acme_case/<int:case_id>/summary', type='jsonrpc', auth='user', methods=['POST'])
    def case_summary(self, case_id):
        case = request.env['acme.case'].browse(case_id).exists()
        if not case:
            raise NotFound()
        case.check_access('read')              # browse() proves neither existence nor access
        return {'name': case.name, 'state': case.state, 'hours': case.hours_total}
```

When overriding a controller in another module, re-decorate the method with `@http.route()`. Without it the route is unpublished. Use `auth='bearer'` for API-key machine access. In 20.0, model code must not read `request`; pass the values in or use `self.env.website`.

## Owl field widget (19.0, Owl 2)

`static/src/hours_badge/hours_badge_field.js`:

```js
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class HoursBadgeField extends Component {
    static template = "acme_case.HoursBadgeField";
    static props = { ...standardFieldProps };

    get value() {
        return this.props.record.data[this.props.name] || 0;
    }
    get isHigh() {
        return this.value > 8;
    }
}

registry.category("fields").add("acme_hours_badge", {
    component: HoursBadgeField,
    supportedTypes: ["float"],
});
```

`static/src/hours_badge/hours_badge_field.xml`:

```xml
<templates xml:space="preserve">
    <t t-name="acme_case.HoursBadgeField">
        <span t-attf-class="badge {{ isHigh ? 'text-bg-warning' : 'text-bg-secondary' }}" t-out="value"/>
    </t>
</templates>
```

Services: `this.orm = useService("orm")` (`import { useService } from "@web/core/utils/hooks"`), then `await this.orm.searchCount("acme.case", [["state", "=", "new"]])`. For controllers, use `import { rpc } from "@web/core/network/rpc"` and `await rpc("/acme_case/1/summary", {})`.

**20.0 (Owl 3) changes to the same widget:**

```js
import { Component, useProps } from "@odoo/owl";
// …
export class HoursBadgeField extends Component {
    static template = "acme_case.HoursBadgeField";
    props = useProps({ ...standardFieldProps });   // `t` validators, not static props
    // getters unchanged; local state: this.state = proxy({}) instead of useState({})
}
```

```xml
<span t-attf-class="badge {{ this.isHigh ? 'text-bg-warning' : 'text-bg-secondary' }}" t-out="this.value"/>
```

`useService(...)` still works in 20.0, though the ORM service is marked as a temporary shim over an Owl plugin. Mirror a current core component on the target branch before writing new 20.0 frontend code.

## Tests

`tests/__init__.py`: `from . import test_acme_case`

```python
from odoo.exceptions import AccessError, UserError
from odoo.fields import Command
from odoo.tests import TransactionCase, tagged
from odoo.tests.common import new_test_user


@tagged('post_install', '-at_install')        # 19.0 default is at_install; 20.0 default is post_install
class TestAcmeCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env['res.partner'].create({'name': 'Customer'})
        cls.user = new_test_user(cls.env, login='case_user', groups='acme_case.group_acme_case_user')
        cls.other = new_test_user(cls.env, login='case_other', groups='acme_case.group_acme_case_user')

    def _new_case(self, user):
        return self.env['acme.case'].with_user(user).create({
            'subject': 'Broken pump',
            'partner_id': self.partner.id,
            'line_ids': [Command.create({'description': 'Diagnose', 'hours': 2})],
        })

    def test_sequence_and_total(self):
        case = self._new_case(self.user)
        self.assertNotEqual(case.name, '/')
        self.assertEqual(case.hours_total, 2)

    def test_start_only_from_new(self):
        case = self._new_case(self.user)
        case.action_start()
        with self.assertRaises(UserError):
            case.action_start()

    def test_user_cannot_read_other_users_case(self):
        case = self._new_case(self.other)
        with self.assertRaises(AccessError):
            case.with_user(self.user).read(['subject'])
```

Run: `odoo-bin -c dev.conf -d acme_test -i acme_case --test-tags /acme_case --stop-after-init`. Demo data is off by default on 19+, so the tests must create their own fixtures.

HOOT tests run in headless Chrome, so the runtime needs Chrome/Chromium and the `websocket-client` Python package. Without them the JS suites are skipped silently.
- **20.0:** `--test-tags /acme_case` also runs the module's HOOT tests (web's `WebSuite` filters by the selected module).
- **19.0:** add the suite explicitly: `--test-tags '/acme_case,/web:WebSuite.test_unit_desktop[@acme_case]'`.

`static/tests/hours_badge_field.test.js` (HOOT; run it from `/web/tests`):

```js
import { expect, test } from "@odoo/hoot";
import { defineMailModels } from "@mail/../tests/mail_test_helpers";
import { defineModels, fields, models, mountView } from "@web/../tests/web_test_helpers";

class AcmeCase extends models.Model {
    _name = "acme.case";
    hours_total = fields.Float();
    _records = [{ id: 1, hours_total: 12 }];
}
defineMailModels(); // the addon depends on mail: its services need mail's mock models
defineModels([AcmeCase]);

test("hours badge highlights long cases", async () => {
    await mountView({
        type: "form",
        resModel: "acme.case",
        resId: 1,
        arch: `<form><field name="hours_total" widget="acme_hours_badge"/></form>`,
    });
    expect(".o_field_widget .badge").toHaveClass("text-bg-warning");
});
```

## Upgrade script

After bumping the manifest to `19.0.1.1.0`, add `upgrades/19.0.1.1.0/pre-migrate.py` (the folder can also be named `migrations/`):

```python
from odoo.upgrade import util   # requires odoo/upgrade-util on the path


def migrate(cr, version):
    util.rename_field(cr, 'acme.case', 'hours', 'hours_total')
```

`pre-` scripts run before the module's models load, `post-` after the module, and `end-` after all modules. They only run on update (`-u acme_case`), never on a fresh install.
