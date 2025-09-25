#!/usr/bin/env python3
import json, sys, pathlib

REQ_KEYS = ["vendor_id","product_id","hw_rev","class","safety_class","power_budget","interfaces"]

def validate(fp):
    try:
        data = json.load(open(fp, "r", encoding="utf-8"))
    except Exception as e:
        print(f"[FAIL] {fp}: not valid JSON: {e}")
        return 1
    missing = [k for k in REQ_KEYS if k not in data]
    if missing:
        print(f"[FAIL] {fp}: missing keys: {', '.join(missing)}")
        return 1
    if data["class"] not in ["CM","RFM","DM","CAM","EPM","AUX"]:
        print(f"[FAIL] {fp}: invalid class {data['class']}")
        return 1
    if data["safety_class"] not in ["Basic","Elevated","Hazardous"]:
        print(f"[FAIL] {fp}: invalid safety_class {data['safety_class']}")
        return 1
    pb = data.get("power_budget", {})
    if not isinstance(pb.get("avg_w", None), (int, float)) or not isinstance(pb.get("peak_w", None), (int, float)):
        print(f"[FAIL] {fp}: power_budget.avg_w/peak_w must be numbers")
        return 1
    print(f"[OK]   {fp}")
    return 0

def main():
    if len(sys.argv) < 2:
        print("Usage: validate_manifest.py <manifest.json> [more.json ...]")
        sys.exit(2)
    rc = 0
    for arg in sys.argv[1:]:
        rc |= validate(arg)
    sys.exit(rc)

if __name__ == "__main__":
    main()
