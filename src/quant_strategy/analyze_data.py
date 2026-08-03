from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "qqq_daily.csv"


def main() -> None:
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            "找不到 qqq_daily.csv，请先运行 download_data.py。"
        )

    data = pd.read_csv(
        DATA_FILE,
        parse_dates=["Date"],
        index_col="Date",
    )

    print("=== 基本信息 ===")
    print(f"总行数: {len(data):,}")
    print(f"开始日期: {data.index.min().date()}")
    print(f"结束日期: {data.index.max().date()}")
    print()

    print("=== 列名 ===")
    print(list(data.columns))
    print()

    print("=== 数据类型 ===")
    print(data.dtypes)
    print()

    print("=== 缺失值 ===")
    print(data.isna().sum())
    print()

    print("=== 重复日期 ===")
    duplicate_count = data.index.duplicated().sum()
    print(f"重复日期数量: {duplicate_count}")
    print()

    print("=== 日期排序 ===")
    print(f"是否按日期升序排列: {data.index.is_monotonic_increasing}")
    print()

    print("=== 价格逻辑检查 ===")
    invalid_high = (data["High"] < data[["Open", "Close", "Low"]].max(axis=1)).sum()
    invalid_low = (data["Low"] > data[["Open", "Close", "High"]].min(axis=1)).sum()
    non_positive_prices = (
        data[["Open", "High", "Low", "Close", "Adj Close"]] <= 0
    ).any(axis=1).sum()
    negative_volume = (data["Volume"] < 0).sum()

    print(f"High 低于其他价格的异常行数: {invalid_high}")
    print(f"Low 高于其他价格的异常行数: {invalid_low}")
    print(f"价格小于等于 0 的行数: {non_positive_prices}")
    print(f"成交量小于 0 的行数: {negative_volume}")
    print()

    print("=== 收益率检查 ===")
    daily_return = data["Adj Close"].pct_change()

    print(f"平均日收益率: {daily_return.mean():.6f}")
    print(f"日收益率标准差: {daily_return.std():.6f}")
    print(f"最大单日上涨: {daily_return.max():.2%}")
    print(f"最大单日下跌: {daily_return.min():.2%}")
    print()

    print("=== 最大上涨日 ===")
    print(daily_return.nlargest(5))
    print()

    print("=== 最大下跌日 ===")
    print(daily_return.nsmallest(5))


if __name__ == "__main__":
    main()