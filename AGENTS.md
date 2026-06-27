# FamilyFinance - Agent Guide

## Project Overview
Flask web app for family finance management (Chinese UI). Tracks financial product purchases and redemptions with profit calculations.

## Architecture
- **Two entry points**: `app.py` (web, port 5000) and `main.py` (CLI)
- **Data storage**: Single JSON file `finance_data.json` (no database)
- **Templates**: Jinja2 in `templates/` with `base.html` layout
- **Static**: Single `style.css` file

## Key Commands

### Run Web App
```bash
python app.py
# Starts on http://0.0.0.0:5000 with debug=True
```

### Run CLI Interface
```bash
python main.py
# Interactive menu-driven CLI
```

### Install Dependencies
```bash
pip install -r requirements.txt
# Only: flask, uuid, datetime (uuid/datetime are stdlib)
```

### Build Executable (PyInstaller)
```bash
pyinstaller FamilyFinance.spec
# Output in dist/FamilyFinance/
```

### Docker Build
```bash
docker build -t familyfinance .
docker run -p 5000:5000 familyfinance
```

## Data Model

Records in `finance_data.json` have two types:

**Purchase records**:
- `id`: UUID string
- `type`: "purchase"
- `product_name`, `amount`, `annual_rate` (decimal, e.g. 0.0474 = 4.74%), `duration` (days)
- `purchase_date`, `end_date`: YYYY-MM-DD format

**Redeem records**:
- `id`: UUID string  
- `type`: "redeem"
- `purchase_record_id`: Links to purchase UUID
- `redeem_amount`, `redeem_date`, `actual_profit`
- `profit_calc`: "auto" or "manual"

## Profit Calculation Logic

Two calculation modes:
1. **Auto**: Compound interest using daily rate = `(1 + annual_rate)^(1/365) - 1`
2. **Manual**: User-provided `actual_profit` value

Real rate formula: `(actual_profit / redeem_amount) * (365 / days_held) * 100`

## Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Dashboard with all records and statistics |
| `/add` | GET/POST | Add purchase or redeem record |
| `/edit/<id>` | GET/POST | Edit purchase record |
| `/delete/<id>` | GET | Delete record |
| `/redeem` | GET/POST | Redeem purchase (creates redeem record) |
| `/statistics` | GET | Charts for monthly/yearly profits and product distribution |

## Gotchas

- **No authentication**: App is completely open
- **No database**: All data in single JSON file, no concurrent access protection
- **Hardcoded secret key**: `app.secret_key = 'your_secret_key'` in app.py
- **Port 5000**: May conflict with macOS AirDrop
- **Debug mode**: Enabled by default in app.py
- **No tests**: No test files or test framework present
- **No linting/formatting**: No config files for code quality tools
- **Mixed ID types**: Web app uses UUID strings, CLI uses sequential integers

## File Structure
```
├── app.py                      # Flask web application (main entry)
├── main.py                     # CLI interface
├── finance_manager.py          # CLI business logic (not used by web app)
├── finance_data.json           # Data file (gitignored for Docker)
├── templates/                  # Jinja2 templates
├── static/style.css            # Single stylesheet
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container config
├── FamilyFinance.spec          # PyInstaller config
├── build/dist/                 # Build outputs
└── docs/                       # Documentation
    ├── IMPROVEMENT_PLAN.md     # Feature improvement plan
    └── DEVELOPMENT_PLAN.md     # Full development plan
```

## Development Notes

- **No hot reload**: `use_reloader=False` in app.py
- **Signal handling**: Custom SIGINT/SIGTERM handlers for clean shutdown
- **Error handling**: Flash messages for user feedback
- **Date format**: Always YYYY-MM-DD strings
- **Currency**: Amounts in yuan (元), no currency formatting
