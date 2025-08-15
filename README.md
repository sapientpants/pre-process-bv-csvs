# Berliner Volksbank CSV Pre-processor for GnuCash

A Python tool that pre-processes transaction CSV exports from Berliner Volksbank for seamless import into GnuCash accounting software.

## Purpose

Berliner Volksbank exports transaction data in a German-formatted CSV that isn't directly compatible with GnuCash's import requirements. This tool transforms these exports into a standardized format that GnuCash can properly import, handling:

- German to English column name mapping
- Date format conversion (DD.MM.YYYY to standard datetime)
- Payee information consolidation
- Field formatting for reliable import

## Features

- **Batch Processing**: Processes all CSV files in the input directory at once
- **Multiple Account Types**: Handles checking, savings, and credit card (Mastercard) accounts
- **Smart Description Building**: Combines payee names with IBANs when available
- **Preserves Transaction Details**: Maintains both description and memo fields for complete transaction information
- **GnuCash-Ready Output**: Generates properly quoted CSV files that import cleanly into GnuCash

## Requirements

- Python 3.13+
- uv (for virtual environment management)
- Poetry (for dependency management)
- pandas

## Installation

1. Clone this repository:
```bash
git clone https://github.com/sapientpants/pre-process-bv-csvs.git
cd pre-process-bv-csvs
```

2. Create and activate the virtual environment with uv:
```bash
uv venv
```

3. Install dependencies with Poetry:
```bash
uv run poetry install
```

## Usage

1. Export your transaction data from Berliner Volksbank online banking as CSV files

2. Place the exported CSV files in the `data/in/` directory
   - Files should follow the naming pattern: `{account-type}-Umsaetze_{IBAN}_{date}.csv`
   - Example: `checking-Umsaetze_XXXXXXXXXX_2025.04.30.csv`

3. Run the processing script:
```bash
uv run python process.py
```

4. Find the processed files in the `data/out/` directory with the same filenames

5. Import the processed CSV files into GnuCash using its import wizard

## How It Works

The tool performs the following transformations:

### Column Mappings

| German (Input) | English (Output) | Notes |
|---------------|------------------|-------|
| IBAN Auftragskonto | Account | Account identifier |
| Valutadatum | Date | Converted from DD.MM.YYYY format |
| Betrag | Amount | Transaction amount |
| Waehrung | Currency | Currency code (typically EUR) |
| Saldo nach Buchung | Balance | Balance after transaction |
| Name Zahlungsbeteiligter + IBAN | Description | Combined payee information |
| Buchungstext + Verwendungszweck | Memo/Description | Transaction details |

### Processing Logic

1. **Description Field**: 
   - If payee name and IBAN are available: `"Payee Name (IBAN)"`
   - Otherwise: Combines booking text and purpose fields

2. **Memo Field**:
   - Contains booking text and purpose when Description has payee info
   - Provides additional transaction context for GnuCash

3. **Date Handling**:
   - Converts German date format (DD.MM.YYYY) to standard datetime
   - Uses Valutadatum (value date) for transaction dating

## File Structure

```
pre-process-bv-csvs/
├── data/
│   ├── in/          # Place Berliner Volksbank CSV exports here
│   └── out/         # Processed GnuCash-ready files appear here
├── process.py       # Main processing script
├── pyproject.toml   # Project configuration
└── README.md        # This file
```

## Example

Input (Berliner Volksbank format):
```csv
"Bezeichnung Auftragskonto";"IBAN Auftragskonto";"Valutadatum";"Name Zahlungsbeteiligter";"Betrag";"Waehrung"
"Girokonto";"DEXXXXXXXXXXXXXXXXXX";"01.01.2025";"Example Payee";"−XX,XX";"EUR"
```

Output (GnuCash-ready format):
```csv
"Account","Date","Description","Memo","Amount","Currency","Balance"
"DEXXXXXXXXXXXXXXXXXX","2025-01-01","Example Payee","","−XX,XX","EUR",""
```

## License

This project is provided as-is for personal use with Berliner Volksbank exports and GnuCash.

## Contributing

Feel free to submit issues or pull requests if you encounter problems or have suggestions for improvements.