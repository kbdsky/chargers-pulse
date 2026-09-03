---
name: chargers-pulse-ops
description: >-
  Autonomous Operations, Cloud Deployment, and Maintenance Runbook for ChargersPulse 2.0 (LA Chargers Intelligence System).
  Use when managing, testing, deploying, or auto-refreshing the Chargers news aggregation, Korean translation, and mobile PWA platform.
---

# ⚡ ChargersPulse Operations & Automation Skill

This skill provides automated runbooks and operational procedures for managing the LA Chargers News Intelligence System.

---

## 🛠️ Automated Commands Quick Reference

### 1. Full News Collection & Report Generation
```bash
# Collect all news, run NLP importance ranking, and produce Korean reports
python -m newspulse.cli generate --all

# Query specific topic
python -m newspulse.cli generate --query "Justin Herbert" --limit 30
```

### 2. Mobile PWA Launcher (Zero-Config Global Tunnel)
```bash
# Starts FastAPI server, creates Cloudflare HTTPS tunnel, prints smartphone QR code
python -m newspulse.mobile_launcher
```

### 3. Background Weekly Automation
```bash
# Python background scheduler (runs every 7 days)
python -m newspulse.scheduler --interval-days 7

# Register native Windows Task Scheduler (Mondays at 09:00 AM)
powershell -ExecutionPolicy Bypass -File .\scripts\setup_weekly_scheduler.ps1 -DayOfWeek Monday -Time 09:00
```

---

## ☁️ 24/7 Standalone Cloud Deployment

When deploying for 24/7 access without needing a local PC:
1. **GitHub Actions Workflow**: `.github/workflows/weekly_briefing.yml` automatically triggers every Monday at 09:00 KST, scrapes all news, and publishes the PWA to GitHub Pages.
2. **Render.com Web Service**: Uses `render.yaml` and `Procfile` with `uvicorn newspulse.mobile.server:app --host 0.0.0.0 --port $PORT`.

---

## 📋 Quality Guidelines
- **Proper Nouns**: Player names (`Justin Herbert`, `Jim Harbaugh`, `Tyler Biadasz`) and team names (`Chargers`, `49ers`) MUST remain in English.
- **Content Language**: Descriptions, takeaways, and analysis MUST be fluent, professional Korean.
- **Error Filtering**: Never output server error pages (`Error 500`, `Server Error`) in reports.
