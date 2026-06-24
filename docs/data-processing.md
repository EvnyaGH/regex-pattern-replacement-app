# Data Processing

## Supported Input

- CSV files using pandas CSV parsing.
- XLSX files using pandas with openpyxl.
- Maximum upload size is controlled by `MAX_UPLOAD_BYTES`, default 5 MB.
- Display preview size is controlled by `MAX_PREVIEW_ROWS`, default maximum 200 rows.

## Preview

`POST /api/files/preview` parses the uploaded file and returns:

- filename;
- column names;
- total row count;
- the first requested preview rows.

The preview limit does not claim to contain the complete dataset.

## Full-File Replacement

`POST /api/files/process` receives the original file again with:

- target column;
- regex;
- replacement text;
- processed preview limit.

The backend parses all rows, applies replacement to the selected column, and calculates statistics across the complete file. Only the first processed rows up to `preview_limit` are returned for display.

This design remains stateless:

- no uploaded file is persisted;
- no database record or upload session is created;
- frontend state does not need to hold the complete dataset;
- each processing request is independently reproducible.

## Value Conversion

- Missing pandas values become JSON `null`.
- Date and datetime values become ISO-formatted strings.
- NumPy scalar values are converted to native Python values.
- Replacement converts non-null target values to strings before applying Python `re`.

## Current Limits

- Files are loaded into backend memory and are capped at 5 MB by default.
- Regex execution has compile validation but no execution timeout yet.
- The browser receives a result preview, not a downloadable processed file.
- CSV export will reuse the same full-file processing path in a later phase.
