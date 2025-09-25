# upx-agent API (draft)

- `GET /modules` → list enumerated modules + manifests
- `POST /module/<id>/enable` → requires owner auth + safety checks
- `POST /module/<id>/set` → module-specific config (e.g., power_percent)
- `GET /module/<id>/telemetry` → temps, faults, health
