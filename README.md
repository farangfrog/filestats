# filestats

A small Python CLI utility that walks a base directory (and all nested subdirectories) and writes a CSV report for every file it finds.

## Requirements
- Python 3.9+

## Usage
```
python filestats.py <base_directory> [-o OUTPUT] [-s]
```

### Arguments
- `base_directory`: Path to the folder you want to scan.
- `-o, --output`: Optional path for the generated CSV file. Defaults to `file_stats.csv` in the current working directory.
- `-s, --stats`: Also print a summary of file counts grouped by last modification year (sorted by year) to stdout.

### Output columns
- `file_name`
- `last_modified` (ISO timestamp)
- `size_bytes`
- `parent_directory`
- `base_directory`

Example:
```
python filestats.py ~/Documents -o documents_report.csv -s
```
