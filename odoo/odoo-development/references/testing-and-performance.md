# Testing, debugging and performance

## Choose tests by observable behavior

Use model tests for business invariants and permissions, HTTP/browser tests for routing and actual user flows, and JavaScript tests for frontend state/rendering. For meaningful addon logic or migrations, validate fresh installation and update against representative existing data. Do not add tests that merely restate a trivial static edit.

Current `TransactionCase` runs methods with savepoint isolation and rolls back the enclosing transaction. Reuse expensive fixtures through `setUpClass`. Import tests from `tests/__init__.py`; test methods start with `test_`. Use `with_user()` and company context for role-bound behavior. `Form` can exercise defaults/onchanges but does not replace browser verification. `HttpCase` supports browser flows. Current docs default tests to `standard, post_install`; older defaults differ. Clean up registry changes when tests add models/fields.

Source: [Python testing reference](https://www.odoo.com/documentation/20.0/developer/reference/backend/testing.html).

Adapt these source-install examples to the actual launcher, paths and disposable database:

```bash
python3 /path/to/odoo/odoo-bin -c /path/to/dev.conf -d acme_test -i acme_addon --test-enable --stop-after-init
python3 /path/to/odoo/odoo-bin -c /path/to/dev.conf -d acme_test -u acme_addon --test-tags /acme_addon --stop-after-init
```

Check `--help` for target flags and demo-data defaults. Select a tag/class/method that actually runs the changed behavior; successful startup with zero selected tests is not a test pass. Save the relevant command, selection, result and environment limits in delivery.

Sources: [CLI testing options](https://www.odoo.com/documentation/20.0/developer/reference/cli.html), [unit-test tutorial](https://www.odoo.com/documentation/20.0/developer/tutorials/unit_tests.html).

## Frontend tests

Current Odoo uses HOOT, web test helpers and a mock server. Put tests under `static/tests`, name executable tests `*.test.js`, include them in `web.assets_unit_tests`, and run the relevant `/web/tests` suite. `.hoot.js` files are shared global modules with different lifecycle constraints. Older branches may use QUnit; preserve the target runner.

Source: [JavaScript unit testing](https://www.odoo.com/documentation/20.0/developer/reference/frontend/unit_testing.html).

Use deterministic assertions around user interaction and resulting state, clean up patches/mocks, and mock only the relevant server contract. Test async failures and component destruction where they affect the feature. Use supported mounting/model helpers instead of inventing a parallel web environment.

Sources: [HOOT](https://www.odoo.com/documentation/20.0/developer/reference/frontend/unit_testing/hoot.html), [web helpers](https://www.odoo.com/documentation/20.0/developer/reference/frontend/unit_testing/web_helpers.html), [mock server](https://www.odoo.com/documentation/20.0/developer/reference/frontend/unit_testing/mock_server.html).

## Debug systematically

Recommended sequence: reproduce with exact version/data/user/company; capture the first relevant traceback; determine whether the failure is Python import, module data, view resolution, asset loading, access control or business logic; compare with matching core behavior; patch the smallest cause; rerun the failed path.

Distinguish a server restart from a module update: Python, stored data/views, schema and browser assets have different loading paths. Inspect network responses and browser console for UI failures, and use unbundled assets when necessary. Keep tokens and personal/business data out of shared traces.

Source: [JavaScript reference/debugging](https://www.odoo.com/documentation/20.0/developer/reference/frontend/javascript_reference.html).

## Profile before changing algorithms

Use representative volumes and measure with the target profiler. SQL and periodic collectors answer different questions and add overhead. Prefer batch creates/searches/aggregations and preserve recordset prefetch. Avoid a query per record, quadratic membership scans and unnecessary recomputations. Add indexes for demonstrated query patterns, considering write/storage cost. Use query-count assertions only when they establish a meaningful performance contract.

Source: [performance](https://www.odoo.com/documentation/20.0/developer/reference/backend/performance.html).

For reproducible volume data, inspect the target populate interface: Odoo 20 introduces a populate-script/blueprint approach, so older `_populate` recipes are version-sensitive. Do not benchmark against confidential production data when a generated representative dataset suffices.

Source: [populate](https://www.odoo.com/documentation/20.0/developer/reference/backend/populate.html).
