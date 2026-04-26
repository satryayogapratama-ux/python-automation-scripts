#!/usr/bin/env python3
"""
Invoice Cross-Validator
Validates invoices against Purchase Orders.
Detects: overcharges, duplicates, missing PO, unapproved PO, vendor mismatch.
Relevant for: Finance Analyst, AP/AR, ERP, Procurement roles
"""

import json
from datetime import datetime

PURCHASE_ORDERS = {
    "PO-2026-001": {"vendor": "PT Bara Utama",       "amount": 255000.00, "approved": True},
    "PO-2026-002": {"vendor": "CV Energi Nusantara", "amount": 119250.00, "approved": True},
    "PO-2026-003": {"vendor": "PT Tambang Jaya",     "amount": 301000.00, "approved": True},
    "PO-2026-004": {"vendor": "PT Logistik Andalan", "amount": 45000.00,  "approved": False},
}

INVOICES = [
    {"invoice_id": "INV-8801", "po_ref": "PO-2026-001", "vendor": "PT Bara Utama",       "amount": 255000.00, "date": "2026-04-01"},
    {"invoice_id": "INV-8802", "po_ref": "PO-2026-002", "vendor": "CV Energi Nusantara", "amount": 121000.00, "date": "2026-04-03"},
    {"invoice_id": "INV-8803", "po_ref": "PO-2026-003", "vendor": "PT Tambang Jaya",     "amount": 301000.00, "date": "2026-04-05"},
    {"invoice_id": "INV-8804", "po_ref": "PO-2026-004", "vendor": "PT Logistik Andalan", "amount": 45000.00,  "date": "2026-04-06"},
    {"invoice_id": "INV-8805", "po_ref": "PO-2026-001", "vendor": "PT Bara Utama",       "amount": 255000.00, "date": "2026-04-08"},
    {"invoice_id": "INV-8806", "po_ref": "PO-9999-XXX", "vendor": "Unknown Vendor",      "amount": 15000.00,  "date": "2026-04-10"},
]

def validate():
    print("=" * 60)
    print("  INVOICE VALIDATION REPORT")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    seen_po = {}
    flags = []
    passed = 0

    for inv in INVOICES:
        issues = []
        po = PURCHASE_ORDERS.get(inv["po_ref"])

        if not po:
            issues.append("❌ No matching PO found")
        else:
            if po["vendor"] != inv["vendor"]:
                issues.append(f"❌ Vendor mismatch (PO: {po['vendor']})")
            if inv["amount"] > po["amount"]:
                issues.append(f"❌ Overcharge by ${inv['amount'] - po['amount']:,.2f}")
            if not po["approved"]:
                issues.append("❌ PO not approved")
            if inv["po_ref"] in seen_po:
                issues.append(f"❌ Duplicate — already paid via {seen_po[inv['po_ref']]}")
            else:
                seen_po[inv["po_ref"]] = inv["invoice_id"]

        status = "✅ PASS" if not issues else "🚨 FLAG"
        if not issues:
            passed += 1

        print(f"\n{status}  {inv['invoice_id']} | {inv['vendor']} | ${inv['amount']:,.2f}")
        for i in issues:
            print(f"       {i}")
        if issues:
            flags.append(inv["invoice_id"])

    print("\n" + "=" * 60)
    print(f"  SUMMARY: {passed}/{len(INVOICES)} passed | {len(flags)} flagged")
    print("=" * 60)

if __name__ == "__main__":
    validate()
