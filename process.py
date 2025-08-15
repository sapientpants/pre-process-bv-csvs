import csv
import pandas as pd
import os

output_dir = 'data/out'
os.makedirs(output_dir, exist_ok=True)

# Bezeichnung Auftragskonto
# IBAN Auftragskonto
# BIC Auftragskonto
# Bankname Auftragskonto
# Buchungstag
# Valutadatum
# Name Zahlungsbeteiligter
# IBAN Zahlungsbeteiligter
# BIC (SWIFT-Code) Zahlungsbeteiligter
# Buchungstext
# Verwendungszweck
# Betrag
# WaehrungRun
# Saldo nach Buchung
# Bemerkung
# Kategorie
# Steuerrelevant
# Glaeubiger ID
# Mandatsreferenz

for file_name in os.listdir('data/in'):
    if file_name.endswith('.csv'):
        file_path = os.path.join('data/in', file_name)
        df = pd.read_csv(file_path, sep=';')

        df['Account'] = df['IBAN Auftragskonto']
        df['Date'] = pd.to_datetime(
            df['Valutadatum'],
            format='%d.%m.%Y',
            errors='coerce'
        )
        df['Amount'] = df['Betrag']
        df['Currency'] = df['Waehrung']
        df['Balance'] = df['Saldo nach Buchung']

        df['Description'] = df.apply(
            lambda row: (
                f"{row['Name Zahlungsbeteiligter']} "
                f"({row['IBAN Zahlungsbeteiligter']})"
                if pd.notna(row['Name Zahlungsbeteiligter'])
                and pd.notna(row['IBAN Zahlungsbeteiligter'])
                else row['Name Zahlungsbeteiligter']
                if pd.notna(row['Name Zahlungsbeteiligter'])
                else None
            ),
            axis=1
        )
        df["Memo"] = None
        df["Memo"] = df.apply(
            lambda row: (
                str(row["Buchungstext"]) + " " + str(row["Verwendungszweck"])
                if not (pd.isna(row["Description"]) or row["Description"].strip() == "")
                else row["Memo"]
            ),
            axis=1,
        )
        df["Description"] = df.apply(
            lambda row: (
                str(row["Buchungstext"]) + " " + str(row["Verwendungszweck"])
                if (pd.isna(row["Description"]) or row["Description"].strip() == "")
                else row["Description"]
            ),
            axis=1,
        )

        df = df.drop(
            columns=[
                'Name Zahlungsbeteiligter',
                'IBAN Zahlungsbeteiligter'
            ]
        )

        required_columns = [
            "Account",
            "Date",
            "Description",
            "Memo",
            "Amount",
            "Currency",
            "Balance",
        ]
        df = df[required_columns]
        output_path = os.path.join(output_dir, file_name)
        df.to_csv(output_path, index=False, quoting=csv.QUOTE_ALL)

print("Data processing complete.")
