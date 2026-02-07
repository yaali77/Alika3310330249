"""Data loading utilities for the stock prediction prototype."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class PricePoint:
    date: str
    close: float


def load_price_history(csv_path: str | Path, close_column: str = "close") -> list[PricePoint]:
    """Load price history from a CSV file.

    Expected columns include a date column and a close column. The date column can
    be named "date" or "Date".
    """
    path = Path(csv_path)
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        points: list[PricePoint] = []
        for row in reader:
            date_value = row.get("date") or row.get("Date")
            if date_value is None:
                raise ValueError("CSV must include a 'date' or 'Date' column.")
            close_value = row.get(close_column)
            if close_value is None:
                raise ValueError(f"CSV must include a '{close_column}' column.")
            points.append(PricePoint(date=date_value, close=float(close_value)))
    if not points:
        raise ValueError("CSV does not contain any price rows.")
    return points


def extract_closes(history: Iterable[PricePoint]) -> list[float]:
    """Extract closing prices from a price history."""
    return [point.close for point in history]
