# Vanguard Fund Tracker

A local HTML dashboard to track 10 UK Vanguard investments with charts and percentage changes over selectable time periods.

## Funds tracked

| Fund | Ticker |
|------|--------|
| S&P 500 UCITS ETF | `VUAG.L` |
| ESG Global All Cap | `V3AB.L` |
| ESG Developed Asia Pacific | `V3PB.L` |
| ESG Emerging Markets | `V3MB.L` |
| LifeStrategy 100% | `0P0000TKZO.L` |
| LifeStrategy 80% | `0P0000TKZM.L` |
| LifeStrategy 20% | `0P0000TKZG.L` |
| FTSE 100 Index | `0P00018XAP.L` |
| FTSE Dev Europe ex-UK | `0P0000KSP8.L` |
| Japan Stock Index | `0P0000KM1Y.L` |

## Setup

Install the required Python library:

```bash
pip install yfinance
```

## Usage

### Fetch latest data

```bash
python3 fetch_data.py
```

This downloads ~1 year of historical price data from Yahoo Finance and saves it to `data/fund_data.json`.

### View the tracker

**Option 1: Local server (recommended)**

```bash
python3 -m http.server 8080
# Open http://localhost:8080
```

**Option 2: GitHub Pages**

Once pushed to GitHub, available at: https://markbarlow.github.io/vanguard-tracker/

## Features

- **Time periods:** 1 week, 1 month, 3 months, 6 months, 1 year
- **Percentage change:** Displayed with green/red colour coding
- **Sparkline charts:** Update with period selection
- **Offline capable:** Works without internet once data is fetched

## File structure

```
vanguard-tracker/
├── fetch_data.py     # Python script to download data
├── index.html        # Dashboard page
├── data/
│   └── fund_data.json    # Historical prices
└── README.md
```

## Maintenance

Prices refresh automatically on weekdays via the `Update Fund Data` GitHub
Action. Run `python3 fetch_data.py` yourself whenever you want them sooner.

### When a ticker stops working

Yahoo occasionally retires a symbol — it did this to the Japan fund's old
`IE00B50MZ948.IR` in September 2026. When that happens the fetch keeps the
fund's previous prices rather than dropping it from the page, prints which
tickers failed, and exits non-zero so the scheduled job goes red. Look up the
fund's current symbol on Yahoo Finance and update the `FUNDS` list in
`fetch_data.py`. UK Vanguard OEICs are usually listed under a `0P….L` symbol.
