# Shopify `scriptTagCreate` / `scriptTagUpdate` shutdown — October 1, 2026 migration guide

If a Shopify app still creates or updates ScriptTags, treat this as a release blocker before **October 1, 2026**.

## What to search for

Search your repository for GraphQL mutations and REST writes such as:

```text
scriptTagCreate
scriptTagUpdate
POST /admin/api/*/script_tags.json
PUT /admin/api/*/script_tags/
```

Do not assume that pinning an older Admin API version avoids the change.

## Fast repository check

From the repository root, run Shopify Change CI locally:

```bash
curl -fsSL https://raw.githubusercontent.com/Kovasandr/shopify-change-ci/main/shopify_change_ci.py -o /tmp/shopify_change_ci.py
python3 /tmp/shopify_change_ci.py . --report shopify-compatibility-report.md
```

The scanner runs locally. It requires no Shopify login, API key, package installation, or source-code upload.

## Migration decision

For storefront behavior currently injected with ScriptTags, evaluate a **theme app extension** (app block or app embed) as the replacement architecture. Do not mechanically replace the API call without checking when the script loads, which storefront surfaces require it, merchant enable/disable behavior, and uninstall cleanup.

For each detected write path, record:

1. the code path that creates or updates the ScriptTag;
2. what storefront behavior the injected script provides;
3. whether the behavior belongs in a theme app extension;
4. installation and upgrade behavior for existing merchants;
5. regression tests required before removing the old path.

## Minimum regression scope

Verify at least install, upgrade, theme activation, app enable/disable, storefront rendering, and uninstall behavior. Existing ScriptTags and new writes are different migration concerns, so test the actual merchant lifecycle rather than only checking that the replacement renders once.

## Need the repository mapped for you?

If the scanner reports HIGH or MEDIUM risk, request the **$99 one-time Shopify compatibility audit**:

https://github.com/Kovasandr/shopify-change-ci/issues/new?template=audit-request.yml

The audit returns affected files/lines, root-cause grouping, remediation guidance, and recommended regression-test scope. Payment is arranged only after the repository is confirmed scannable.
