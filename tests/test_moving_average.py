from quant_strategy.indicators.moving_average import sma
from quant_strategy.utils.data_loader import load_daily_data

data = load_daily_data("QQQ")

data["MA20"] = sma(data["Adj Close"], 20)
data["MA50"] = sma(data["Adj Close"], 50)

print(data[["Adj Close", "MA20", "MA50"]].tail())