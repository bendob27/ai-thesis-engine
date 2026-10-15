#!/usr/bin/env python3
"""Read-only price check for the signal sweep.

Uses yfinance history() closes ONLY — the pre-computed info fields are banned
per CLAUDE.md ratio-pipe rules. Prints each close WITH its date (price-at-call
convention: always stamp the close's date).

Usage: python3 quote_check.py TICKER [TICKER ...]   (max 10)
"""
import sys


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: quote_check.py TICKER [TICKER ...]")
    import yfinance as yf
    for ticker in sys.argv[1:11]:
        try:
            hist = yf.Ticker(ticker).history(period="5d")
            if hist.empty:
                print(f"{ticker}: no data on yfinance")
                continue
            rows = hist.tail(2)
            parts = [f"{close:.2f} ({date.date()})" for date, close in zip(rows.index, rows["Close"])]
            line = f"{ticker}: close {parts[-1]}"
            if len(parts) > 1:
                line += f" · prev {parts[-2]}"
            print(line)
        except Exception as exc:
            print(f"{ticker}: error {exc}")


if __name__ == "__main__":
    main()
