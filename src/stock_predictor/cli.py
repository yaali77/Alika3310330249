"""Command-line interface for the stock prediction prototype."""

from __future__ import annotations

import argparse

from stock_predictor.data import extract_closes, load_price_history
from stock_predictor.pipeline import generate_forecast


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a baseline stock forecast from a CSV file."
    )
    parser.add_argument("csv_path", help="Path to the CSV file with price history.")
    parser.add_argument(
        "--close-column",
        default="close",
        help="Column name that contains the close price. Default: close",
    )
    parser.add_argument(
        "--window",
        type=int,
        default=14,
        help="Window size for technical indicators. Default: 14",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    history = load_price_history(args.csv_path, close_column=args.close_column)
    closes = extract_closes(history)
    result = generate_forecast(closes, window=args.window)

    print("Baseline forecast")
    print(f"- Next value forecast: {result.forecast:.2f}")
    print(f"- SMA({args.window}): {result.sma:.2f}")
    print(f"- EMA({args.window}): {result.ema:.2f}")
    print(f"- RSI({args.window}): {result.rsi:.2f}")


if __name__ == "__main__":
    main()
