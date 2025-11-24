import argparse
import csv
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Tuple


FileRecord = Tuple[str, str, int, str, str]


def collect_file_stats(base_dir: Path) -> List[FileRecord]:
    base_dir = base_dir.resolve()
    records: List[FileRecord] = []

    for path in sorted(base_dir.rglob('*')):
        if not path.is_file():
            continue

        stat_result = path.stat()
        last_modified = datetime.fromtimestamp(stat_result.st_mtime).isoformat()
        parent_name = path.parent.name
        base_name = base_dir.name

        records.append(
            (
                path.name,
                last_modified,
                stat_result.st_size,
                parent_name,
                base_name,
            )
        )

    return records


def write_csv(records: Iterable[FileRecord], output_path: Path) -> None:
    if output_path.parent:
        output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open('w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'file_name',
            'last_modified',
            'size_bytes',
            'parent_directory',
            'base_directory',
        ])
        for record in records:
            writer.writerow(record)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            'Collect file information (name, last modification date, size, '
            'parent directory, and base directory) from a base directory and '
            'its subdirectories, exporting the results as CSV.'
        )
    )
    parser.add_argument(
        'base_directory',
        type=Path,
        help='Path to the base directory to scan.',
    )
    parser.add_argument(
        '-o',
        '--output',
        type=Path,
        default=Path('file_stats.csv'),
        help='Path to the output CSV file (default: file_stats.csv).',
    )
    parser.add_argument(
        '-s',
        '--stats',
        action='store_true',
        help='Print counts of files by last modification year to stdout.',
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    base_dir: Path = args.base_directory

    if not base_dir.exists() or not base_dir.is_dir():
        raise SystemExit(f"Base directory '{base_dir}' does not exist or is not a directory.")

    records = collect_file_stats(base_dir)
    write_csv(records, args.output)
    print(f"Collected {len(records)} files from '{base_dir}' into '{args.output}'.")

    if args.stats:
        years = [datetime.fromisoformat(record[1]).year for record in records]
        year_counts = Counter(years)
        for year in sorted(year_counts):
            print(f"{year}: {year_counts[year]}")


if __name__ == '__main__':
    main()
