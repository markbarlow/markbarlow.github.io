#!/usr/bin/env python3
"""
Vanguard Fund Tracker - Data Fetcher
Fetches historical price data from Yahoo Finance for UK Vanguard funds.
"""

import json
import math
import os
from datetime import datetime, timedelta

try:
    import yfinance as yf
except ImportError:
    print("Error: yfinance not installed. Run: pip install yfinance")
    exit(1)

# Fund definitions with Yahoo Finance tickers
FUNDS = [
    {"name": "S&P 500 UCITS ETF", "ticker": "VUAG.L", "short": "VUAG, 0.07%"},
    {"name": "ESG Global All Cap", "ticker": "V3AB.L", "short": "V3AB, 0.24%"},
    {"name": "ESG Developed Asia Pacific", "ticker": "V3PB.L", "short": "V3PB, 0.17%"},
    {"name": "ESG Emerging Markets", "ticker": "V3MB.L", "short": "V3MB, 0.19%"},
    {"name": "LifeStrategy 100%", "ticker": "0P0000TKZO.L", "short": "LS100, 0.20%"},
    {"name": "LifeStrategy 80%", "ticker": "0P0000TKZM.L", "short": "LS800, 0.20%"},
    {"name": "LifeStrategy 20%", "ticker": "0P0000TKZG.L", "short": "LS200, 0.20%"},
    {"name": "FTSE 100 Index", "ticker": "0P00018XAP.L", "short": "FTSE100, 0.06%"},
    {"name": "FTSE Dev Europe ex-UK", "ticker": "0P0000KSP8.L", "short": "EU, 0.12%"},
    # Yahoo retired the ISIN-style symbol IE00B50MZ948.IR in Sept 2026;
    # 0P0000KM1Y.L is the same GBP Acc share class.
    {"name": "Japan Stock Index", "ticker": "0P0000KM1Y.L", "short": "Japan, 0.16%"},
]

def load_previous(filepath):
    """Load the last saved data, keyed by ticker. Returns {} if unreadable."""
    try:
        with open(filepath) as handle:
            previous = json.load(handle)
        return {fund["ticker"]: fund for fund in previous.get("funds", [])}
    except (OSError, ValueError, KeyError):
        return {}


def fetch_fund_data(previous):
    """Fetch historical data for all funds.

    Returns (data, failed). A fund whose fetch fails is carried over from the
    previous run rather than dropped, so a ticker that stops resolving cannot
    silently remove a fund from the page. Failures are reported in `failed`.
    """
    print("Fetching Vanguard fund data from Yahoo Finance...")

    # Fetch 1 year + buffer of historical data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=400)  # Extra buffer for 1Y period

    all_data = {
        "last_updated": datetime.now().isoformat(),
        "funds": []
    }
    failed = []

    def carry_over(fund, reason):
        """Reuse the previous run's prices for a fund we could not fetch."""
        failed.append((fund, reason))
        stale = previous.get(fund["ticker"])
        if stale and stale.get("prices"):
            stale = dict(stale, name=fund["name"], short=fund["short"])
            all_data["funds"].append(stale)
            print(f"{reason} - keeping previous data "
                  f"(last {stale['prices'][-1]['date']})")
        else:
            print(f"{reason} - no previous data to fall back on")

    for fund in FUNDS:
        print(f"  Fetching {fund['name']} ({fund['ticker']})...", end=" ")

        try:
            ticker = yf.Ticker(fund["ticker"])
            hist = ticker.history(start=start_date, end=end_date)

            if hist.empty:
                carry_over(fund, "No data available")
                continue

            # Convert to list of {date, price} objects.
            # Yahoo sometimes returns rows with a NaN close (e.g. a partial
            # trading day). NaN is not valid JSON, so skip those rows.
            prices = []
            skipped = 0
            for date, row in hist.iterrows():
                close = row["Close"]
                if close is None or math.isnan(close):
                    skipped += 1
                    continue
                prices.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "price": round(float(close), 4)
                })

            if not prices:
                carry_over(fund, "No valid prices")
                continue

            fund_data = {
                "name": fund["name"],
                "ticker": fund["ticker"],
                "short": fund["short"],
                "prices": prices,
                "currency": "GBP"
            }

            all_data["funds"].append(fund_data)
            note = f", {skipped} skipped" if skipped else ""
            print(f"OK ({len(prices)} data points{note})")

        except Exception as e:
            carry_over(fund, f"Error: {e}")

    # Keep a stable order regardless of which funds fell back.
    order = {f["ticker"]: i for i, f in enumerate(FUNDS)}
    all_data["funds"].sort(key=lambda f: order.get(f["ticker"], len(order)))

    return all_data, failed

def save_json(data, filepath):
    """Save data to JSON file.

    allow_nan=False makes this raise rather than write NaN/Infinity, which
    are Python extensions that browsers reject when parsing the file.
    """
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2, allow_nan=False)
    print(f"\nData saved to {filepath}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    json_path = os.path.join(data_dir, "fund_data.json")

    # Fetch data, falling back to the last run for anything that fails
    previous = load_previous(json_path)
    data, failed = fetch_fund_data(previous)

    # Save to JSON
    save_json(data, json_path)

    print(f"\nFetched data for {len(data['funds'])} of {len(FUNDS)} funds")
    print("Open index.html in a browser to view the tracker")

    if failed:
        print(f"\n{len(failed)} fund(s) could not be fetched:")
        for fund, reason in failed:
            print(f"  - {fund['name']} ({fund['ticker']}): {reason}")
        print("Check whether these tickers are still valid on Yahoo Finance.")
        # Non-zero exit so the scheduled workflow goes red instead of
        # quietly publishing a page with a fund missing or frozen.
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
