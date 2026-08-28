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
    {"name": "Japan Stock Index", "ticker": "IE00B50MZ948.IR", "short": "Japan, 0.16%"},
]

def fetch_fund_data():
    """Fetch historical data for all funds."""
    print("Fetching Vanguard fund data from Yahoo Finance...")

    # Fetch 1 year + buffer of historical data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=400)  # Extra buffer for 1Y period

    all_data = {
        "last_updated": datetime.now().isoformat(),
        "funds": []
    }

    for fund in FUNDS:
        print(f"  Fetching {fund['name']} ({fund['ticker']})...", end=" ")

        try:
            ticker = yf.Ticker(fund["ticker"])
            hist = ticker.history(start=start_date, end=end_date)

            if hist.empty:
                print("No data available")
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
                print("No valid prices")
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
            print(f"Error: {e}")

    return all_data

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

    # Fetch data
    data = fetch_fund_data()

    # Save to JSON
    json_path = os.path.join(data_dir, "fund_data.json")
    save_json(data, json_path)

    print(f"\nSuccessfully fetched data for {len(data['funds'])} funds")
    print("Open index.html in a browser to view the tracker")

if __name__ == "__main__":
    main()
