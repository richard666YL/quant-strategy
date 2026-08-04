from pathlib import Path

from quant_strategy.optimizer.ma_optimizer import (
    optimize_ma_parameters,
)
from quant_strategy.utils.data_loader import load_daily_data


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = PROJECT_ROOT / "reports"


data = load_daily_data("QQQ")

short_windows = list(range(5, 51, 5))
long_windows = list(range(20, 201, 10))

results = optimize_ma_parameters(
    price=data["Adj Close"],
    short_windows=short_windows,
    long_windows=long_windows,
    trading_cost=0.001,
)

REPORTS_DIR.mkdir(parents=True, exist_ok=True)

output_file = REPORTS_DIR / "ma_optimization_results.csv"
results.to_csv(output_file, index=False)

print("=== Sharpe Ratio 前 10 名 ===")
print(
    results.sort_values(
        by="sharpe_ratio",
        ascending=False,
    )
    .head(10)
    .to_string(index=False)
)

print()
print("=== CAGR 前 10 名 ===")
print(
    results.sort_values(
        by="cagr",
        ascending=False,
    )
    .head(10)
    .to_string(index=False)
)

print()
print(f"共测试有效组合：{len(results)}")
print(f"完整结果已保存到：{output_file}")