# Shopify Change CI

Catch risky Shopify API and checkout integration patterns before they become production incidents.

## MVP
Zero-dependency Python scanner. Point it at a Shopify app repository and it reports risky files/lines and returns a failing CI exit code for high-severity findings.

```bash
python shopify_change_ci.py .
python shopify_change_ci.py . --json
python shopify_change_ci.py . --report compatibility-report.md
```

Currently checks for old API versions, legacy REST product/variant calls, PriceRule usage, Customer Account checkout assumptions, carrier-service integrations, and checkout/customer-account extensions.

## Example audit
A real-world sample report generated from a public Shopify integration is available at [`examples/pod-autopilot-sample-report.md`](examples/pod-autopilot-sample-report.md). It shows the output buyers receive: overall risk, concrete file/line evidence, prioritized findings, remediation, next steps, and scope limitations.

## Why
Shopify evolves APIs continuously. This utility gives app developers a cheap preflight check they can run locally or in CI before a platform change becomes an incident.

## Status
Early MVP. Looking for Shopify app developers willing to test it on a real repository. Open an issue with false positives, missed breaking-change patterns, or a compatibility case you want covered.

## Paid compatibility audit
For teams that want an interpreted deliverable rather than raw scanner output, the paid layer is a repository-specific compatibility audit: prioritized risks, evidence, remediation guidance, and recommended regression scope. The free scanner remains available as the acquisition wedge.

Planned recurring layer: continuous release monitoring + repository-specific compatibility checks + regression scenarios.
