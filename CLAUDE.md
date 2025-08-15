# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This tool pre-processes Berliner Volksbank (BV) transaction CSV exports for import into GnuCash. It transforms the German-formatted bank statements into a standardized format that GnuCash can properly import.

## Development Commands

### Running the Script
```bash
# Using uv (recommended)
uv run python process.py

# Or directly with Python if dependencies are installed
python process.py
```

### Dependencies
The project uses:
- **uv** for virtual environment management
- **Poetry** for dependency management
- **Python 3.13+** runtime
- **pandas** for CSV processing
- **pandas-stubs** for type hints

To install dependencies:
```bash
uv venv
uv run poetry install
```

## Architecture

### Data Flow
1. **Input**: Berliner Volksbank CSV exports in `data/in/` directory
   - Files follow naming pattern: `{account-type}-Umsaetze_{IBAN}_{date}.csv`
   - Contains columns in German with semicolon separation
   - Account types: checking, savings, mastercard

2. **Processing**: `process.py` script
   - Reads all CSV files from `data/in/`
   - Maps German column names to GnuCash-compatible English columns
   - Transforms date formats (DD.MM.YYYY to datetime)
   - Combines payee information with IBAN when available
   - Creates Description and Memo fields from transaction details
   - Outputs only essential columns for GnuCash: Account, Date, Description, Memo, Amount, Currency, Balance

3. **Output**: GnuCash-ready CSV files in `data/out/` directory
   - Same filename as input
   - CSV format with all fields quoted for reliable GnuCash import

### Key Column Mappings
- `IBAN Auftragskonto` → `Account`
- `Valutadatum` → `Date` (converted from DD.MM.YYYY format)
- `Betrag` → `Amount`
- `Waehrung` → `Currency`
- `Saldo nach Buchung` → `Balance`
- Combined fields → `Description` (payee name + IBAN if available, otherwise booking text + purpose)
- `Buchungstext + Verwendungszweck` → `Memo` (when Description has payee info)