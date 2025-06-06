required_modules = ["yfinance", "pushbullet.py", "newsapi-python", "num2words", "python-dotenv"]
try:
    import yfinance as yf
    from pushbullet import Pushbullet
    from newsapi import NewsApiClient
    import time
    from datetime import datetime
    import os
    from num2words import num2words
    from dotenv import load_dotenv
    import sys

    # Initialize Pushbullet and News API
    if os.path.exists(".env"):
        load_dotenv()
        pb = Pushbullet(os.getenv("Pushbullet_API_KEY"))
        news_api = NewsApiClient(api_key=os.getenv("NewsApi_API_KEY"))

    else:
        print(f"\033[1;31m.env file not found, Create one and save it with your API Keys in the format as follows:\033[0m")
        print("\033[93mPushbullet_API_KEY='your_apikey_here'\nNewsApi_API_KEY='your_apikey_here'\033[0m")
        sys.exit()


    # Path to stocks.txt file
    stocks_file = "stocks.txt"

    # Dictionary to store the last known stock details
    last_details = []
    last_news = {}

    # Function to read stock symbols from a file
    def read_stocks_file():
        stocks = []

        # Check if the file exists
        if os.path.exists(stocks_file):
            print("\033[1;32mstocks.txt found, listing contents:\033[0m")

            with open(stocks_file, "r") as file:
                content = file.readlines()
                for line in content:
                    print(line.strip())  # Show stocks to the user
                edit_ask = input("\n\033[93mDo you wish to continue or edit the file? (continue/edit): \033[0m").strip().lower()

                if edit_ask == "continue":
                    stocks = [line.strip() for line in content if line.strip()]
                    if not stocks:
                        print("\033[1;31mstocks.txt is empty. Please add stock symbols.\033[0m")
                elif edit_ask == "edit":
                    print("\n\033[1;33mType the stock symbols, enter STOP to stop entering the content to the file:\033[0m\n")
                    with open(stocks_file, 'w') as file:
                        while True:
                            line = input()
                            if line.strip().upper() == "STOP":
                                break
                            file.write(line + "\n")
                    print(f"\033[1;34mContent has been saved to {stocks_file}.\033[0m\n")
                    # After editing, read the file again to return the updated list
                    with open(stocks_file, "r") as file:
                        stocks = [line.strip() for line in file.readlines() if line.strip()]
                else:
                    print("\033[1;31mInvalid choice. Please try again.\033[0m")
                    return read_stocks_file()  # Prompt user again for correct input
        else:
            # If file doesn't exist
            print(f"\033[1;31m{stocks_file} not found. Creating a new one.\033[0m")
            print("\nType the stock symbols, enter STOP to stop entering the content to the file:\n")
            with open(stocks_file, 'w') as file:
                while True:
                    line = input()
                    if line.strip().upper() == "STOP":
                        break
                    file.write(line + "\n")
            print(f"\033[1;34mContent has been saved to {stocks_file}.\033[0m\n")
            # Return the updated list
            with open(stocks_file, "r") as file:
                stocks = [line.strip() for line in file.readlines() if line.strip()]

        return stocks

    # Function to format number
    def format_number(number):
        # Convert to Indian number format
        num_str = str(number)[::-1]
        formatted_number = []

        # First group of three digits
        formatted_number.append(num_str[:3])

        # Remaining digits in groups of two
        num_str = num_str[3:]
        while len(num_str) > 0:
            formatted_number.append(num_str[:2])
            num_str = num_str[2:]

        # Join and reverse
        formatted_number = ','.join(formatted_number)[::-1]

        # Determine scale
        if number >= 10**7:
            scale = "crore"
            value = number / 10**7
        elif number >= 10**5:
            scale = "lakh"
            value = number / 10**5
        elif number >= 10**3:
            scale = "thousand"
            value = number / 10**3
        else:
            scale = ""
            value = number

        # Return the number with the scale only
        if scale:
            value_in_words = f"{int(value)} {scale}"
        else:
            value_in_words = str(number)

        return f"{formatted_number} ({value_in_words})"

    # Function to fetch company news
    def fetch_company_news(stock_symbol):
        try:
            news = news_api.get_everything(q=stock_symbol, language="en", sort_by="publishedAt", page_size=1)
            if news["articles"]:
                article = news["articles"][0]
                return {
                    "title": article["title"],
                    "description": article["description"],
                    "url": article["url"]
                }
            return None
        except Exception as e:
            print(f"Error fetching news for {stock_symbol}: {e}")
            return None

    def is_market_open():
        now = datetime.now()
        # Market timings: 9:15 AM to 3:30 PM (IST)
        market_open_time = now.replace(hour=9, minute=15, second=0, microsecond=0)
        market_close_time = now.replace(hour=15, minute=30, second=0, microsecond=0)
        return market_open_time <= now <= market_close_time

    def fetch_stock_details(stock_symbol):
        try:
            stock = yf.Ticker(stock_symbol + ".NS")  # Add .NS for NSE stocks
            data = stock.history(period="1d")
            info = stock.info

            if not data.empty:
                last_price = data["Close"].iloc[-1]
                volume = data["Volume"].iloc[-1]
                market_cap = info.get("marketCap", "N/A")
                pe_ratio = info.get("trailingPE", "N/A")
                sector = info.get("sector", "N/A")

                details = {
                    "Price": last_price,
                    "Volume": format_number(volume),
                    "Market Cap": format_number(market_cap) if market_cap != "N/A" else "N/A",
                    "P/E Ratio": pe_ratio if pe_ratio != "N/A" else "N/A",
                    "Sector": sector,
                }

                return details
            else:
                print(f"\033[1;31mNo data available for {stock_symbol}. The stock may be inactive.\033[0m")
                return None

        except Exception as e:
            print(f"\033[1;31mError fetching details for {stock_symbol}: {e}\033[0m")
            return None

    def send_stock_update_notification(stock_symbol, old_details, new_details):
            print(f"\033[1;32mStock Updates for {stock_symbol}:\033[0m")
            send_message = ""
            print_message = ""
            for key in new_details:
                old_value = old_details.get(key)
                new_value = new_details.get(key)
                if old_value != new_value:
                    print_message += f" \n \033[1;36m{key}: {old_value} → {new_value}\033[0m"
                    send_message += f"\n{key}: {old_value} → {new_value}"
            print(print_message)
            print("-" * 40)
            pb.push_note(f"Stock Updates for: {stock_symbol}", send_message)

    def send_initial_stock_notification(stock_symbol, details):
        print_message = ""
        send_message = ""
        for key, value in details.items():
            print_message += f"\n  \033[1;36m{key}: {value}\033[0m"
            send_message += f"\n{key}: {value}"
        print(print_message)  # Print the message to the console
        pb.push_note(f"Live Details for {stock_symbol}:", send_message)  # Send the message using Pushbullet


    def send_end_of_day_update(stock_symbol, details):
        print_message = ""
        send_message = ""
        for key, value in details.items():
            print_message += f"\n  \033[1;36m{key}: {value}\033[0m"
            send_message += f"\n{key}: {value}"

        print(print_message)  # Print the message to the console
        pb.push_note(f"End-of-Day Update: {stock_symbol}", send_message)

    # Function to monitor stocks and news
    def monitor_stocks():
        stocks = read_stocks_file()
        if not stocks:
            print("\033[1;31mNo stocks to monitor. Add symbols to stocks.txt.\033[0m")
            return
        if is_market_open():
            print("\n\033[1;36mMarket is open. Continuously updating stock details...\033[0m")
            print("-" * 40)
            try:
                for stock_symbol in stocks:
                    details = fetch_stock_details(stock_symbol)
                    if details:
                        print(f"\033[1;32mLive Details for {stock_symbol}:\033[0m")
                        send_initial_stock_notification(stock_symbol, details)
                        last_details.append((stock_symbol, details))
                        print("-" * 40)

                        time.sleep(1)
                time.sleep(10)

                while is_market_open():
                    for stock in stocks:
                        current_details = fetch_stock_details(stock)

                        # Check if this stock already has previous details stored in last_details
                        stock_found = False
                        for index, (symbol, old_details) in enumerate(last_details):
                            if symbol == stock:
                                # If details exist, send update notification
                                send_stock_update_notification(stock, old_details, current_details)
                                # Update the last details with the new details
                                last_details[index] = (stock, current_details)
                                stock_found = True
                                time.sleep(3)
                                break

                        # If the stock was not found in last_details, store its initial details
                        if not stock_found:
                            last_details.append((stock, current_details))
                     # Sleep for 10 seconds before checking the stocks again
                    time.sleep(10)

            except KeyboardInterrupt:
                print("\n\033[1;31mMonitoring stopped by user.\033[0m")
        else:
            print("\n\033[1;33mMarket is closed. Displaying end-of-day stock details:-\033[0m")
            print("-" * 40)
            for stock_symbol in stocks:
                details = fetch_stock_details(stock_symbol)
                if details:
                    print(f"\033[1;32mEnd-of-Day Details for {stock_symbol}:\033[0m")
                    send_end_of_day_update(stock_symbol, details)
                    print("-" * 40)
            print("\033[1;32m\nAll stock details fetched. Exiting...\033[0m\n")


    # Start monitoring
    monitor_stocks()
except ModuleNotFoundError:
    print("\033[1;32mRequired modules not installed, trying to install them...\033[0m")
    import subprocess
    import sys
    def install_package(package):
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    for module in required_modules:
        install_package(module)

    print("\033[1;32mModules installed successfully, Try running the program again.\033[0m")

