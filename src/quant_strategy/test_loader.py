from quant_strategy.utils.data_loader import load_daily_data


data = load_daily_data("QQQ")

print(data.head())

print()

print(data.tail())

print()

print(data.columns)