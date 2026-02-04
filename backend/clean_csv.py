import re
from pathlib import Path

SRC = Path(__file__).parent / 'SME_Financial_Health_Dataset.csv'
OUT = Path(__file__).parent / 'SME_Financial_Health_Dataset_clean.csv'

text = SRC.read_text(encoding='utf-8', errors='ignore')

# Normalize line endings
text = text.replace('\r\n', '\n').replace('\r', '\n')

# Ensure header is first line
lines = text.split('\n')
if len(lines) < 2:
    print('File too small or unreadable')
    raise SystemExit(1)

header = lines[0].strip()
rest = '\n'.join(lines[1:])

# Many records appear to run together. Split heuristically on occurrences of '\nSME_' or ' SME_' preceded by a comma or linebreak.
# First, ensure we have a marker 'SME_' for each record; insert newline before 'SME_' when not at start of line
rest_fixed = re.sub(r'(?<!\n)(SME_\d+)', r'\n\1', rest)
# Also split on patterns like '\tSME_' or multiple spaces followed by SME_
rest_fixed = re.sub(r'\s+(SME_\d+)', r'\n\1', rest_fixed)

# Reconstruct candidate lines, remove empty lines, and ensure each line has same number of commas as header (best-effort)
candidates = [l.strip() for l in rest_fixed.split('\n') if l.strip()]
clean_lines = [header]

for c in candidates:
    # If candidate already starts with SME_, assume it's a record
    if c.startswith('SME_'):
        clean_lines.append(c)
    else:
        # Attach to previous line (likely a wrapped continuation)
        if len(clean_lines) >= 2:
            clean_lines[-1] = clean_lines[-1] + ' ' + c
        else:
            clean_lines.append(c)

# Write cleaned output
OUT.write_text('\n'.join(clean_lines), encoding='utf-8')
print('Wrote cleaned CSV to', OUT)
