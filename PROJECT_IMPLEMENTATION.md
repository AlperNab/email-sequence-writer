# Email Sequence Writer — Standalone Real GUI Implementation

This folder is now its own runnable project app. It does not depend on the root all-project dashboard at runtime.

## Run

```bash
./run_gui.sh
```

Windows:

```powershell
.\run_gui_windows.ps1
```

Default URL: `http://127.0.0.1:9119`

## What is inside this project folder

- `app/` — FastAPI backend for this project.
- `static/` — elegant browser GUI.
- `plugins/email-sequence-writer.json` — this project’s own feature/customization/input schema.
- `project_config.json` — readable copy of the same project-specific configuration.
- `data/` — local SQLite jobs, uploads, exports.
- `tests/` — verifies this project has a registered real local engine.

## Project-specific scope

- Domain: `Marketing / Lifecycle Email`
- Target user: `Domain operator, business owner, analyst, or team member who needs this workflow executed reliably.`
- Core job: Offer/persona → email sequence
- Suite: `General Automation Suite`

## Deep features applied

- sequence strategy
- segmentation
- subject A/B tests
- personalization tokens
- deliverability guard
- behavior branches
- ESP export

## Customization controls

- `execution_mode` — Execution mode (select)
- `goal` — goal (text)
- `funnel_stage` — funnel stage (text)
- `sequence_length` — sequence length (text)
- `tone` — tone (text)
- `brand_voice` — brand voice (text)
- `esp_format` — ESP format (select)
- `personalization_fields` — personalization fields (text)
- `send_cadence` — send cadence (text)
- `output_format` — output format (select)
- `language` — language (select)
- `privacy_mode` — privacy mode (select)
- `confidence_threshold` — Confidence threshold (slider)

## Input fields

- `offer` — Offer (text) required
- `persona` — persona (text) required
- `work_brief` — Work brief / source text / URL / instructions (textarea) required

## External data policy

The local deterministic core is real and executable. Live external systems are not simulated. If Shopify, ATS, ERP, OCR/STT, maps, SERP, market data, medical databases, tax/customs databases, or other live systems are required, this project reports the missing connector/API requirement instead of inventing data.

---

## Final UX/UI Layer

This project now uses the **Automation Command Center** pattern.

**UX workflow:** Brief/data intake → structured analysis → action plan → export

**Domain components:**
- Brief analyzer
- KPI cards
- Workflow board
- Decision checklist
- Report builder

**Quick actions:**
- Structure input
- Generate action plan
- Build scorecard
- Prepare final report

**No fake-data policy:** external/live actions require real connectors or API keys. Missing connectors are reported instead of simulated.
