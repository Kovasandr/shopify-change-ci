# Shopify Breaking-Change Compatibility Report

**Target:** `jdoseph/pod-autopilot` — `src/analytics.py`
**Overall risk:** HIGH
**Findings:** 5 high

## Executive summary

The scanned Shopify integration pins Admin API `2025-07` in three production request paths. Two of those paths also use legacy REST product endpoints. This creates a concrete upgrade risk: the integration should move to a supported Shopify Admin API version and the product operations should be migrated to GraphQL, then regression-tested before production deployment.

## Prioritized findings

### 1. Unsupported API version — HIGH
**Location:** `src/analytics.py:29`
**Evidence:** `/admin/api/2025-07/products.json`
**Action:** Upgrade the integration to a supported stable Admin API version and regression-test product reads.

### 2. Legacy REST product endpoint — HIGH
**Location:** `src/analytics.py:29`
**Evidence:** `/admin/api/2025-07/products.json`
**Action:** Replace the REST product read with the corresponding GraphQL Admin API query.

### 3. Unsupported API version — HIGH
**Location:** `src/analytics.py:38`
**Evidence:** `/admin/api/2025-07/orders.json`
**Action:** Upgrade the version-pinned request and regression-test order retrieval and pagination behavior.

### 4. Unsupported API version — HIGH
**Location:** `src/analytics.py:59`
**Evidence:** `/admin/api/2025-07/products/{id}.json`
**Action:** Upgrade the integration and regression-test the product status update workflow.

### 5. Legacy REST product endpoint — HIGH
**Location:** `src/analytics.py:59`
**Evidence:** `/admin/api/2025-07/products/{id}.json`
**Action:** Replace the REST product update with the corresponding GraphQL Admin API mutation.

## Recommended next steps

1. Move all three version-pinned calls to a currently supported stable Admin API version.
2. Migrate product read/update operations from REST to GraphQL Admin API.
3. Regression-test product reads, order reads, pagination, authentication/scopes, and the product status update path.
4. Add Shopify Change CI to pull requests so unsupported versions and legacy product REST usage cannot silently return.

## Scope and limitations

This is a static compatibility preflight against the referenced source file. It does not prove runtime failure and does not test Shopify store configuration, access scopes, external systems, or live API responses. A production migration should include runtime regression testing.
