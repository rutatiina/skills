# UI and frontend

## Views and actions

Inherit views by external ID with narrow, stable selectors. Parent chains, priority, groups and installed extensions affect the final architecture. Inspect the resolved view when selectors fail; avoid translated labels and arbitrary positions.

Source: [view records](https://www.odoo.com/documentation/20.0/developer/reference/user_interface/view_records.html).

Current architecture uses `<list>`, `<chatter/>`, kanban `<t t-name="card">` and Python expressions for `invisible`/`readonly`/`required`/`column_invisible`. Fields referenced by expressions must be available in the view; add them with `invisible="1"` when a modifier needs them. `column_invisible` hides a list column, while `invisible` hides a cell. In 20.0 a kanban can delegate its card to a separate `<card>` view via `card_id`. Domains and default contexts guide UI behavior, not authorization.

Source: [view architectures](https://www.odoo.com/documentation/20.0/developer/reference/user_interface/view_architectures.html).

Window actions specify models/views, client actions use registry tags, and reports use report actions. Preserve returned action contracts and load actions before referencing menus.

Source: [actions](https://www.odoo.com/documentation/20.0/developer/reference/backend/actions.html).

## Owl and web-client extensions

Use native imports and target `@addon/path` names. Current Odoo transpiles files under `static/src` and `static/tests` automatically; other folders can require an opt-in header. Do not prescribe a magic header or `odoo.define` for every version.

Source: [JavaScript modules](https://www.odoo.com/documentation/20.0/developer/reference/frontend/javascript_modules.html).

Use Owl `setup()`, hooks, explicit props and addon-prefixed templates (`acme_case.HoursBadgeField`). Include JavaScript/XML/styles in the correct bundle. Reuse framework components, and handle reactive state and asynchronous work through the component lifecycle.

**The Owl major depends on the Odoo version.** 19.0 ships Owl 2: `static props = {...}`, `useState`, templates referencing `props.x` and `state.y`. 20.0 ships Owl 3: `props = useProps({...})` with `t` validators, `proxy()`/`signal()`/`computed()` reactivity, `useEffect(fn)` tracking what it reads, templates referencing `this.props.x` and `this.state.y`, and services implemented as plugins (`useService` still available). `odoo-bin upgrade_code --script owl3-migration` rewrites much of an Owl 2 addon. Check the result against a current core component. Owl 3 docs: `github.com/odoo/owl/tree/master/doc/v3`.

Source: [Owl components](https://www.odoo.com/documentation/20.0/developer/reference/frontend/owl_components.html).

Prefer registry extension points for fields, views, services and client actions. Obtain dependencies through service hooks. Use ORM services for models and the target RPC mechanism for controller calls. Server authorization remains mandatory.

Sources: [registries](https://www.odoo.com/documentation/20.0/developer/reference/frontend/registries.html), [services](https://www.odoo.com/documentation/20.0/developer/reference/frontend/services.html), [hooks](https://www.odoo.com/documentation/20.0/developer/reference/frontend/hooks.html).

When necessary, current `patch(target, extension)` supports native method `super`. Patch prototypes for instance methods and classes for static methods. Patch `setup()` rather than constructors. Repeated patches need fresh extension objects; retain unpatch functions for test cleanup. Older signatures differ.

Source: [patching](https://www.odoo.com/documentation/20.0/developer/reference/frontend/patching_code.html).

Reuse standard field props/update contracts, match controller/renderer/model definitions for custom views, and register the exact client action tag used by its record.

Sources: [fields](https://www.odoo.com/documentation/20.0/developer/howtos/javascript_field.html), [views](https://www.odoo.com/documentation/20.0/developer/howtos/javascript_view.html), [client actions](https://www.odoo.com/documentation/20.0/developer/howtos/javascript_client_action.html).

## Assets and styling

Select backend, frontend, report and test bundles by execution context. Asset before/after/replace directives require existing targets and correct dependency ordering. For stale code, check bundle membership, module update, browser cache, load errors and `debug=assets`.

Source: [assets](https://www.odoo.com/documentation/20.0/developer/reference/frontend/assets.html).

Respect SCSS variable order; scope component styles and use CSS variables for contextual changes. Avoid broad selectors. Verify responsive/RTL layouts. Use the target's icons: 20.0 uses Material Symbols (`<i class="oi" data-icon="person"/>`), while 19.0 still accepts Font Awesome (`fa fa-user`) and `oi` icons.

Sources: [SCSS inheritance](https://www.odoo.com/documentation/20.0/developer/reference/user_interface/scss_inheritance.html), [SCSS tips](https://www.odoo.com/documentation/20.0/developer/howtos/scss_tips.html), [icons](https://www.odoo.com/documentation/20.0/developer/reference/user_interface/icons.html).

## QWeb and reports

Prefer escaped `t-out`; do not mark user text safe or insert untrusted HTML. Check template scope and Python/JavaScript QWeb differences before sharing helpers.

Source: [QWeb](https://www.odoo.com/documentation/20.0/developer/reference/frontend/qweb.html).

Reports connect model, action, template and paper format. A custom report-values implementation must provide expected `docs`, `doc_ids`, `doc_model` values when needed. Put fonts in report assets. Verify language, headers/footers, page breaks and permissions in generated output as well as HTML. Match the deployed PDF engine/dependencies to the release.

Sources: [reports](https://www.odoo.com/documentation/20.0/developer/reference/backend/reports.html), [PDF tutorial](https://www.odoo.com/documentation/20.0/developer/tutorials/pdf_reports.html), [reporting models](https://www.odoo.com/documentation/20.0/developer/howtos/create_reports.html).

## Website and portal

Use website templates/snippets/editor extensions and account for language, publication, multi-website visibility and anonymous access. Public Owl components need the website/portal integration. Standalone Owl needs its own assets/page/environment; backend services are not automatically available.

Sources: [themes](https://www.odoo.com/documentation/20.0/developer/howtos/website_themes.html), [theme setup](https://www.odoo.com/documentation/20.0/developer/howtos/website_themes/setup.html), [standalone Owl](https://www.odoo.com/documentation/20.0/developer/howtos/standalone_owl_application.html), [website/portal Owl](https://www.odoo.com/documentation/20.0/developer/howtos/frontend_owl_components.html).
