"""Convert units.csv to units.json using the CSV's own header row.

parser.py labelled columns with a fixed header list in the modern Vega Strike
order, which does not match Privateer Gemini Gold's units.csv, so most fields
after the first difference were shifted or lost (and the first data row was
skipped). This keys every value by its real column name instead.

usage: python csv_to_json.py [units.csv] [units.json]
"""
import csv
import json
import sys

src = sys.argv[1] if len(sys.argv) > 1 else 'units.csv'
dst = sys.argv[2] if len(sys.argv) > 2 else 'units.json'

with open(src, encoding='latin-1', newline='') as f:
    rows = list(csv.reader(f))

header = rows[0]
units = []
for row in rows[2:]:          # row 1 holds the column types
    if not row or not row[0]:
        continue
    unit = {}
    for name, value in zip(header, row):
        if value != '':
            unit[name] = value
    units.append(unit)

with open(dst, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(units, f, indent=4, ensure_ascii=False)
    f.write('\n')
print('%d units written to %s' % (len(units), dst))
