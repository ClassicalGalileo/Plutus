import requests

def get_historical_cash_flows(symbol, api_key, years=5):
    url = f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    # Extracting annual cash flow data for specified years
    cash_flows = data['annualReports'][:years] if 'annualReports' in data and data['annualReports'] else []
    return [cf['operatingCashflow'] for cf in cash_flows if 'operatingCashflow' in cf]

def calculate_average_cash_flow(cash_flows):
    cash_flows = [int(cf) for cf in cash_flows]
    return sum(cash_flows) / len(cash_flows) if cash_flows else 0

def calculate_dcf(average_cash_flow, discount_rate, years):
    dcf_value = 0
    for year in range(1, years + 1):
        dcf_value += average_cash_flow / ((1 + discount_rate) ** year)
    return dcf_value

def main():
    api_key = 'API_KEY'
    stock_symbol = input("Enter the stock symbol (e.g., AAPL for Apple): ")
    historical_years = 5 # Number of years of historical data to consider
    projection_years = 10 # Number of years to project cash flows
    discount_rate = 0.1 # Discount rate (WACC)

    historical_cash_flows = get_historical_cash_flows(stock_symbol, api_key, historical_years)

    if historical_cash_flows:
        average_cash_flow = calculate_average_cash_flow(historical_cash_flows)
        dcf_value = calculate_dcf(average_cash_flow, discount_rate, projection_years)
        print(f"DCF Value for {stock_symbol}: {dcf_value}")
    else:
        print(f"No cash flow data available for {stock_symbol}.")

if __name__ == "__main__":
    main()
