# Shopify Change CI

**Shopify breaks two developer workflows on October 1, 2026. Check your repo before the deadline.**

Shopify Change CI catches risky Shopify API, ScriptTag, CLI, and checkout integration patterns before they become production incidents.

## October 1 preflight

Two confirmed Shopify changes make this check time-sensitive:

- **ScriptTag writes stop:** `scriptTagCreate`, `scriptTagUpdate`, and REST ScriptTag POST/PUT fail on every API version starting October 1. Pinning an older API version does not defer the change.
- **Old Shopify CLI auth stops for password-protected storefronts:** theme development flows require Shopify CLI `3.84.0+` starting October 1; `3.83.x` and earlier are no longer supported for those flows.

Run the free scanner now. If it finds risk and you want an interpreted migration plan, request the **$99 one-time compatibility audit** below.

## Run it in every pull request

Add this to `.github/workflows/shopify-change-ci.yml`:

```yaml
name: Shopify Change CI
on: [push, pull_request]
jobs:
  compatibility:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: Kovasandr/shopify-change-ci@main
```

No API key, account, package install, or Shopify credentials required. A HIGH-risk finding fails CI and the scanner can also generate a Markdown compatibility report.

## Local MVP
Zero-dependency Python scanner. Point it at a Shopify app repository and it reports risky files/lines and returns a failing CI exit code for high-severity findings.

```bash
python shopify_change_ci.py .
python shopify_change_ci.py . --json
python shopify_change_ci.py . --report compatibility-report.md
```

Currently checks for old API versions, legacy REST product/variant calls, PriceRule usage, Customer Account checkout assumptions, carrier-service integrations, checkout/customer-account extensions, ScriptTag create/update calls, outdated Shopify CLI versions, and September/October 2026 Shopify breaking-change patterns.

## Example audit
A real-world sample report generated from a public Shopify integration is available at [`examples/pod-autopilot-sample-report.md`](examples/pod-autopilot-sample-report.md). It shows the output buyers receive: overall risk, concrete file/line evidence, prioritized findings, remediation, next steps, and scope limitations.

## Why
Shopify evolves APIs continuously. This utility gives app developers a cheap preflight check they can run locally or in CI before a platform change becomes an incident.

## Status
Early MVP. Looking for Shopify app developers willing to test it on a real repository. Open an issue with false positives, missed breaking-change patterns, or a compatibility case you want covered.

## $99 Shopify Compatibility Audit
Need an interpreted result instead of raw scanner output? The first paid offer is a **$99 one-time repository compatibility audit**.

You receive:
- root-cause risk summary instead of duplicate scanner hits
- exact affected files/lines and code evidence
- prioritized HIGH/MEDIUM risks
- remediation guidance for each risk
- recommended regression-test scope
- a client-ready Markdown report you can keep with the repository

**Turnaround target:** within 1 business day after repository access is available.

### Request an audit
**[Request the $99 compatibility audit →](https://github.com/Kovasandr/shopify-change-ci/issues/new?template=audit-request.yml)**

The request form captures the repository, Shopify surface, current symptoms, and private-repository handling. Do not paste source code, tokens, credentials, or other secrets into a public issue.

Payment is arranged only after the repository is confirmed scannable. No payment is required to request the audit.

Planned recurring layer: continuous release monitoring + repository-specific compatibility checks + regression scenarios.
