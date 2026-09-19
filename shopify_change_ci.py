#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path

RULES = [
    {"id":"old-api-version","severity":"high","pattern":r"2024-(?:01|04|07|10)|2025-(?:01|04|07)","message":"Unsupported Shopify API version detected. Upgrade and regression-test."},
    {"id":"api-version-near-retirement","severity":"medium","pattern":r"2025-10","message":"Shopify API 2025-10 is near retirement (October 2026). Plan upgrade and regression-test now."},
    {"id":"rest-admin-products","severity":"high","pattern":r"/admin/api/[^/]+/(?:products|variants)(?:[.]json|/)","message":"Legacy REST product/variant Admin API usage detected. Migrate to GraphQL Admin API."},
    {"id":"legacy-price-rule","severity":"high","pattern":r"(?<![A-Za-z0-9_])(?:PriceRule|priceRule)(?![A-Za-z0-9_])","message":"Legacy PriceRule surface detected; verify against the target Shopify API release."},
    {"id":"last-incomplete-checkout","severity":"high","pattern":r"(?<![A-Za-z0-9_])lastIncompleteCheckout(?![A-Za-z0-9_])","message":"Customer.lastIncompleteCheckout usage detected; verify target API and migration path."},
    {"id":"carrier-service-assumption","severity":"medium","pattern":r"(?<![A-Za-z0-9_])carrierService(?:Create|Update)?(?![A-Za-z0-9_])|/carrier_services","message":"Carrier service integration detected; regression-test shipping-profile behavior."},
    {"id":"checkout-ui-extension","severity":"medium","pattern":r"checkout_ui_extension|checkout[.]ui[.]render|customer-account-ui","message":"Checkout/customer-account extension detected; verify current extension API."},
]
EXT={".js",".jsx",".ts",".tsx",".py",".rb",".php",".go",".java",".kt",".dart",".cs",".graphql",".gql",".json",".toml",".yml",".yaml",".md"}

def scan(root):
    out=[]
    root=Path(root)
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in EXT or any(x in p.parts for x in ("node_modules",".git","vendor","dist","build")):
            continue
        try:
            text=p.read_text(errors="ignore")
        except Exception:
            continue
        for n,line in enumerate(text.splitlines(),1):
            for rule in RULES:
                if re.search(rule["pattern"],line,re.I):
                    out.append({"rule":rule["id"],"severity":rule["severity"],"file":str(p.relative_to(root)),"line":n,"message":rule["message"],"excerpt":line.strip()[:240]})
    return out

def write_report(findings, output_file):
    counts={severity:sum(1 for x in findings if x["severity"]==severity) for severity in ("high","medium")}
    risk="HIGH" if counts["high"] else ("MEDIUM" if counts["medium"] else "LOW")
    lines=[
        "# Shopify Breaking-Change Compatibility Report",
        "",
        f"**Overall risk:** {risk}",
        f"**Findings:** {len(findings)} ({counts['high']} high, {counts['medium']} medium)",
        "",
        "## Executive summary",
        "This static preflight identifies Shopify API/version and integration patterns that should be reviewed before platform changes reach production.",
        "",
        "## Prioritized findings",
    ]
    if not findings:
        lines += ["No configured compatibility risks were detected.", ""]
    for i,x in enumerate(findings,1):
        lines += [
            f"### {i}. {x['rule']} — {x['severity'].upper()}",
            f"**Location:** `{x['file']}:{x['line']}`",
            f"**Why it matters:** {x['message']}",
            f"**Evidence:** `{x['excerpt']}`",
            "**Recommended action:** Upgrade or migrate the affected Shopify surface, then regression-test the impacted workflow against the target stable API version.",
            "",
        ]
    lines += [
        "## Recommended next steps",
        "1. Resolve HIGH findings before the next production release.",
        "2. Validate MEDIUM findings in a Shopify development store or equivalent regression environment.",
        "3. Add this scanner to CI so the same risk patterns cannot silently return.",
        "",
        "## Scope and limitations",
        "This is a static compatibility preflight, not proof that an integration will fail. Runtime behavior, Shopify configuration, scopes, app-specific business logic, and external systems require separate regression testing.",
    ]
    Path(output_file).write_text("\n".join(lines)+"\n",encoding="utf-8")

def main():
    ap=argparse.ArgumentParser(description="Shopify breaking-change static preflight scanner")
    ap.add_argument("path",nargs="?",default=".")
    ap.add_argument("--json",action="store_true")
    ap.add_argument("--report",metavar="FILE",help="Write a client-ready Markdown compatibility report")
    a=ap.parse_args()
    findings=scan(a.path)
    if a.report:
        write_report(findings,a.report)
    if a.json:
        print(json.dumps({"findings":findings,"count":len(findings)},indent=2))
    else:
        for x in findings:
            print(f'[{x["severity"].upper()}] {x["file"]}:{x["line"]} {x["rule"]}\\n  {x["message"]}\\n  {x["excerpt"]}')
        print(f"\\n{len(findings)} finding(s)")
    raise SystemExit(1 if any(x["severity"]=="high" for x in findings) else 0)

if __name__=="__main__":
    main()
