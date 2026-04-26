#!/usr/bin/env python3
"""
Supply Chain Performance Analyzer
Analyzes supplier delivery performance, cost variances, and flags risk.
Relevant for: Operations Manager, Supply Chain Analyst, Procurement roles
"""

import json
from datetime import datetime
from collections import defaultdict

SAMPLE_DATA = [
    {"supplier": "PT Tambang Jaya", "order_id": "PO-001", "ordered_qty": 5000, "delivered_qty": 4800, "order_date": "2026-01-05", "delivery_date": "2026-01-15", "expected_date": "2026-01-14", "unit_price": 85.5},
    {"supplier": "PT Bara Utama", "order_id": "PO-002", "ordered_qty": 3000, "delivered_qty": 3000, "order_date": "2026-01-08", "delivery_date": "2026-01-20", "expected_date": "2026-01-18", "unit_price": 82.0},
    {"supplier": "PT Tambang Jaya", "order_id": "PO-003", "ordered_qty": 4000, "delivered_qty": 3500, "order_date": "2026-02-01", "delivery_date": "2026-02-14", "expected_date": "2026-02-10", "unit_price": 86.0},
    {"supplier": "CV Energi Nusantara", "order_id": "PO-004", "ordered_qty": 2000, "delivered_qty": 2000, "order_date": "2026-02-10", "delivery_date": "2026-02-22", "expected_date": "2026-02-25", "unit_price": 79.5},
    {"supplier": "PT Bara Utama", "order_id": "PO-005", "ordered_qty": 6000, "delivered_qty": 5800, "order_date": "2026-03-01", "delivery_date": "2026-03-18", "expected_date": "2026-03-15", "unit_price": 83.0},
    {"supplier": "CV Energi Nusantara", "order_id": "PO-006", "ordered_qty": 1500, "delivered_qty": 1500, "order_date": "2026-03-05", "delivery_date": "2026-03-20", "expected_date": "2026-03-22", "unit_price": 80.0},
]

def parse_date(d):
    return datetime.strptime(d, "%Y-%m-%d")

def analyze():
    suppliers = defaultdict(lambda: {"orders": 0, "on_time": 0, "late_days_total": 0, "qty_ordered": 0, "qty_delivered": 0, "total_value": 0, "shortfalls": 0})

    for row in SAMPLE_DATA:
        s = row["supplier"]
        delay = (parse_date(row["delivery_date"]) - parse_date(row["expected_date"])).days
        suppliers[s]["orders"] += 1
        suppliers[s]["qty_ordered"] += row["ordered_qty"]
        suppliers[s]["qty_delivered"] += row["delivered_qty"]
        suppliers[s]["total_value"] += row["delivered_qty"] * row["unit_price"]
        if delay > 0:
            suppliers[s]["late_days_total"] += delay
        else:
            suppliers[s]["on_time"] += 1
        if row["delivered_qty"] < row["ordered_qty"]:
            suppliers[s]["shortfalls"] += 1

    print("=" * 60)
    print("  SUPPLY CHAIN PERFORMANCE REPORT")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    risky = []
    for name, d in suppliers.items():
        on_time_rate = (d["on_time"] / d["orders"]) * 100
        fill_rate = (d["qty_delivered"] / d["qty_ordered"]) * 100
        avg_delay = d["late_days_total"] / d["orders"]
        risk = "🔴 HIGH" if on_time_rate < 70 or fill_rate < 90 else "🟡 MEDIUM" if on_time_rate < 90 else "🟢 LOW"
        print(f"\n📦 {name}")
        print(f"   Orders: {d['orders']} | On-Time: {on_time_rate:.0f}% | Fill Rate: {fill_rate:.1f}%")
        print(f"   Avg Delay: {avg_delay:.1f} days | Value: ${d['total_value']:,.0f}")
        print(f"   Risk: {risk}")
        if "HIGH" in risk:
            risky.append(name)

    print("\n" + "=" * 60)
    if risky:
        for r in risky:
            print(f"  ⚠️  Action required: {r}")
    else:
        print("  ✅ All suppliers within acceptable range.")

if __name__ == "__main__":
    analyze()
