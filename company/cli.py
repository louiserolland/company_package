import argparse
import datetime
from company import Company


def display_info(ticker):
    """
    Displays basic company information.
    """
    company = Company(name="N/A", ticker=ticker)
    company.display_info()



def get_stock_price_difference(ticker, interval, stop_date):
    """
    Retrieves the stock price difference over the specified interval up to the stop date.
    """
    company = Company(name="N/A", ticker=ticker)
    stop_date = datetime.datetime.strptime(stop_date, "%Y-%m-%d")
    
    # Retrieve stock data
    stock_data = company.get_stock_info(period=interval)
    if stock_data is None:
        print("No stock data available.")
        return

    # Make stock_data.index timezone-naive by removing timezone
    stock_data.index = stock_data.index.tz_localize(None)

    # Filter stock data up to the specified stop date
    stock_data = stock_data[stock_data.index <= stop_date]
    if stock_data.empty:
        print("No data available for the given period and stop date.")
        return

    start_price = stock_data['Close'].iloc[0]
    end_price = stock_data['Close'].iloc[-1]
    price_difference = end_price - start_price

    print(f"Stock price difference for {ticker} over {interval} ending {stop_date.date()}: {price_difference}")


def main():
    """
    Main function for the CLI tool.
    """
    parser = argparse.ArgumentParser(description="Company CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Sub-command for displaying company info
    parser_info = subparsers.add_parser("display_info", help="Display company information")
    parser_info.add_argument("--ticker", type=str, required=True, help="Stock ticker symbol (e.g., AAPL).")


    # Sub-command for getting stock price difference
    parser_diff = subparsers.add_parser("get_stock_price_difference", help="Get stock price difference")
    parser_diff.add_argument("--ticker", type=str, required=True, help="Stock ticker symbol (e.g., AAPL).")
    parser_diff.add_argument("--interval", type=str, default="1y", help="Time period (e.g., '1y', '6mo', '2y').")
    parser_diff.add_argument("--stop_date", type=str, required=True, help="End date in YYYY-MM-DD format.")


    args = parser.parse_args()

    if args.command == "display_info":
        display_info(args.ticker)

    if args.command == "get_stock_price_difference":
        get_stock_price_difference(args.ticker, args.interval, args.stop_date)


if __name__ == "__main__":
    main()
