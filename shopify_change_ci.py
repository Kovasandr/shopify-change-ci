#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path

RULES=[
 {"id":"old-api-version","severity":"high","pattern":r"(2024-(01|04|07|10)|2025-(01|04|07))","message":"Old Shopify API version detected. Upgrade and regression-test."},
 {"id":"rest-admin-products","severity":"high","pattern":r"/admin/api/[^/]+/(products|variants)(\\.json|/)","message":"Legacy REST product/variant Admin API usage detected. Migrate to GraphQL Admin API."},
 {"id":"legacy-price-rule","severity":"high","pattern":r"\\b(PriceRule|priceRule)\\b","message":"Legacy PriceRule surface detected; verify against the target Shopify API release."},
 {"id":"last-incomplete-checkout","severity":"high","pattern":r"\\blastIncompleteCheckout\\b","message":"Customer.lastIncompleteCheckout usage detected; verify target Customer Account API."},
 {"id":"carrier-service-assumption","severity":"medium","pattern":r"\\bcarrierService(Create|Update)?\\b|/carrier_services","message":"Carrier service integration detected; regression-test shipping-profile behavior."},
 {"id":"checkout-ui-extension","severity":"medium","pattern":r"(checkout_ui_extension|checkout\\.ui\\.render|customer-account-ui)","message":"Checkout/customer-account extension detected; verify current extension API."}
]
EXT={".js",".jsx",".ts",".tsx",".py",".rb",".php",".go",".java",".kt",".graphql",".gql",".json",".toml",".yml",".yaml",".md"}
def scan(root):
 out=[]
 for p in Path(root).rglob("*"):
  if not p.is_file() or p.suffix.lower() not in EXT or any(x in p.parts for x in ("node_modules",".git","vendor","dist","build")): continue
  try: text=p.read_text(errors="ignore")
  except Exception: continue
  for n,line in enumerate(text.splitlines(),1):
   for r in RULES:
    if re.search(r["pattern"],line,re.I):
     out.append({"rule":r["id"],"severity":r["severity"],"file":str(p.relative_to(root)),"line":n,"message":r["message"],"excerpt":line.strip()[:240]})
 return out
def main():
 ap=argparse.ArgumentParser(description="Shopify breaking-change static preflight scanner"); ap.add_argument("path",nargs="?",default="."); ap.add_argument("--json",action="store_true"); a=ap.parse_args()
 f=scan(a.path)
 if a.json: print(json.dumps({"findings":f,"count":len(f)},indent=2))
 else:
  for x in f: print(f'[{x["severity"].upper()}] {x["file"]}:{x["line"]} {x["rule"]}\n  {x["message"]}\n  {x["excerpt"]}')
  print(f"\n{len(f)} finding(s)")
 raise SystemExit(1 if any(x["severity"]=="high" for x in f) else 0)
if __name__=="__main__": main()
