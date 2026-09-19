# Shopify Change CI

Catch risky Shopify API and checkout integration patterns before they become production incidents.

## MVP
Zero-dependency Python scanner. Point it at a Shopify app repository and it reports risky files/lines and returns a failing CI exit code for high-severity findings.

```bash
python shopify_change_ci.py .
python shopify_change_ci.py . --json
```

Currently checks for old API versions, legacy REST product/variant calls, PriceRule usage, Customer Account checkout assumptions, carrier-service integrations, and checkout/customer-account extensions.

## Why
Shopify evolves APIs continuously. This utility gives app developers a cheap preflight check they can run locally or in CI before a platform change becomes an incident.

## Status
Early MVP. Looking for Shopify app developers willing to test it on a real repository. Open an issue with false positives, missed breaking-change patterns, or a compatibility case you want covered.

## Planned paid layer
Continuous release monitoring + repository-specific compatibility checks + regression scenarios. The free scanner stays useful as the acquisition wedge.
