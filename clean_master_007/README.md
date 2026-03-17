# CSV Data Cleaning Tool

## Overview

This tool cleans raw CSV order data and generates a structured Excel report.

It produces three sheets:

• results — cleaned data
• errors — invalid values and their locations
• summary — error count per field

---

## Requirements

Python 3.9+

Required packages:

pip install pandas xlsxwriter

---

## Usage

Clean a single file:

python clean.py input.csv output.xlsx

Example:

python clean.py data/raw/orders.csv data/output/orders_clean.xlsx

---

## Folder Structure

data/raw
Original client files (do not modify)

data/output
Cleaned output files

---

## Supported Cleaning Rules

Quantity:
• "10 pcs" → 10
• "2x4" → 8
• "7-9" → 8

Price:
• "$1200" → 1200
• "USD 450.50" → 450.5

Date:
• "2024/01/05" → 2024-01-05
• "2024.03.15" → 2024-03-15

Discount:
• "10%" → 0.1
• "0.15" → 0.15

---

## Output Example

results.xlsx contains:

results sheet
errors sheet
summary sheet

---

## Notes

Original files are never modified.

Always place client files in data/raw and export to data/output.

---

## Author

Rocky