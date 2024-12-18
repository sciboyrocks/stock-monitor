# Stock Monitor and News Fetcher for Indian Stock Markets

## Overview
This project is a Python-based stock monitoring and news-fetching tool designed specifically for the Indian stock markets. It allows users to track real-time stock data and receive notifications via Pushbullet. The application continuously updates stock details such as price, volume, market capitalization, P/E ratio, and sector. Additionally, it fetches the latest news articles related to the stocks and provides them in a user-friendly format.

The project uses APIs like Yahoo Finance (`yfinance`), News API (`newsapi-python`), and Pushbullet (`pushbullet.py`) to deliver real-time data, making it an efficient way to track and stay informed about the Indian stock market movements.

## Features
### 1. **Real-Time Stock Monitoring (Indian Markets)**
   - **Live Stock Details**: Fetches live stock data such as the current price, volume, market cap, P/E ratio, and sector from the National Stock Exchange (NSE) of India using Yahoo Finance API. This project is tailored for Indian stocks by appending `.NS` to the stock symbol to ensure accurate data retrieval.
   - **Indian Number Formatting**: Displays values in Indian numbering format (lakh, crore) for easy understanding of large numbers.

### 2. **Latest Stock News**
   - **Stock-Related News**: Fetches the latest news articles related to the monitored Indian stock symbols from the News API.
   - **News Display**: Displays relevant news articles, including the title, description, and URL to the full article.

### 3. **Push Notifications**
   - **Pushbullet Integration**: Sends push notifications to your devices (mobile, desktop, etc.) for significant stock updates, ensuring you're always informed.

### 4. **Stock Symbol Management**
   - **Interactive File Handling**: Reads stock symbols from a `stocks.txt` file. If the file doesn't exist or is empty, the program will prompt the user to input and edit stock symbols manually.
   - **User-Editable**: Users can add or remove stock symbols from the `stocks.txt` file interactively while the program is running.

### 5. **Market Time Management**
   - **Market Status Detection**: The application determines whether the Indian stock market is open or closed (9:15 AM to 3:30 PM IST). During open hours, stock details are continuously updated; outside market hours, end-of-day data is displayed.

### 6. **Error Handling**
   - **Error Messages**: Provides clear error messages if data for a stock is unavailable or if the required modules are not installed. The program attempts to install missing dependencies automatically.

### 7. **User-Friendly Interface**
   - **Terminal Interface**: Designed to run in the terminal, the program provides colored outputs and prompts to guide the user through editing the stock symbols and viewing real-time data.

## Installation

### Prerequisites
Ensure you have Python 3.x installed on your system. You can download it from [here](https://www.python.org/downloads/).

### Steps
1. **Clone or Download the Repository**
   ```bash
   git clone https://github.com/yourusername/stock-monitor.git
   cd stock-monitor
