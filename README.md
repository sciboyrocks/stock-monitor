# Stock Monitor and Notification System

This project is a **real-time stock monitoring and notification system** designed specifically for **Indian stocks**. It fetches live stock data, provides real-time updates, and sends notifications for stock price changes and end-of-day summaries. The application also retrieves the latest news about the tracked companies, keeping you updated with their recent developments.

---

## Features
- **Live Stock Updates**: Fetches and displays live stock details like price, volume, market cap, P/E ratio, and sector.
- **End-of-Day Summaries**: Provides a final summary of stock performance after the market closes.
- **Push Notifications**: Sends updates via Pushbullet for stock changes and end-of-day details.
- **Company News**: Fetches the latest news articles related to the tracked companies.
- **Interactive File Editing**: Lets users dynamically manage the list of tracked stocks.

---

## Requirements
The following modules are required to run the application:
- `yfinance`
- `pushbullet.py`
- `newsapi-python`
- `num2words`
- `python-dotenv`

The program will automatically attempt to install these modules if they are not already installed.

---

## Indian Stocks
- The application is tailored for **Indian stocks** traded on the National Stock Exchange (NSE).
- To monitor Indian stocks, enter their stock symbols as listed on NSE, followed by `.NS` (e.g., `RELIANCE.NS`, `TCS.NS`) in the `stocks.txt` file.

---

## Setup

1. Clone the repository or download the code.
2. Create a `.env` file in the root directory with the following format:
   ```plaintext
   Pushbullet_API_KEY='your_pushbullet_api_key'
   NewsApi_API_KEY='your_newsapi_api_key'
