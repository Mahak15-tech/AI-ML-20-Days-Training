
import csv
from pathlib import Path


def count_csv_rows(file_path: str) -> int:
    """Return the number of data rows in a CSV file."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header
        return sum(1 for row in reader)


def main() -> None:
    """Run the CSV row-count command."""
    csv_path = Path(__file__).resolve().parent.parent / "data" / "sample.csv"

    try:
        row_count = count_csv_rows(str(csv_path))
        print(f"CSV file: {csv_path.name}")
        print(f"Total data rows: {row_count}")
    except (FileNotFoundError, OSError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
