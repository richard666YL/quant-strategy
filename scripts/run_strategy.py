from quant_strategy.broker.moomoo_position import get_current_position
from quant_strategy.execution.executor import execute_trade
from quant_strategy.strategies.ma_target_position import (
    calculate_ma_target_position,
)
from quant_strategy.trader.decision import decide_action
from quant_strategy.utils.data_loader import load_daily_data


# ============================================================
# 配置
# ============================================================

# 历史数据使用的 ticker
DATA_TICKER = "QQQ"

# Moomoo API 使用的股票代码
TRADE_SYMBOL = "US.QQQ"

# MA 参数
SHORT_WINDOW = 20
LONG_WINDOW = 50

# 每次交易数量
ORDER_QUANTITY = 1

# 总交易开关
#
# False = 只计算策略和交易决策，不允许提交订单
# True  = 允许进入 Execution Engine
#
# 注意：
# executor.py 目前仍然锁定为 SIMULATE 模拟交易
TRADING_ENABLED = False


# ============================================================
# 主程序
# ============================================================

def main() -> None:

    # --------------------------------------------------------
    # 1. 读取 QQQ 历史日线数据
    # --------------------------------------------------------

    data = load_daily_data(DATA_TICKER)


    # --------------------------------------------------------
    # 2. 根据 MA20 / MA50 生成目标仓位
    # --------------------------------------------------------

    target_position = calculate_ma_target_position(
        prices=data["Adj Close"],
        short_window=SHORT_WINDOW,
        long_window=LONG_WINDOW,
    )


    # --------------------------------------------------------
    # 3. 从 Moomoo 模拟账户读取当前 QQQ 仓位
    # --------------------------------------------------------

    current_position = get_current_position(
        TRADE_SYMBOL
    )


    # --------------------------------------------------------
    # 4. 比较目标仓位和当前仓位
    #    生成 BUY / SELL / HOLD
    # --------------------------------------------------------

    action = decide_action(
        target_position=target_position,
        current_position=current_position,
    )


    # --------------------------------------------------------
    # 5. 打印策略结果
    # --------------------------------------------------------

    print("=" * 45)
    print("MA20 / MA50 Trading Summary")
    print("=" * 45)

    print(f"Symbol           : {TRADE_SYMBOL}")
    print(f"Short MA         : {SHORT_WINDOW}")
    print(f"Long MA          : {LONG_WINDOW}")
    print(f"Target Position  : {target_position}")
    print(f"Current Position : {current_position}")
    print(f"Decision         : {action}")

    print("=" * 45)


    # --------------------------------------------------------
    # 6. Execution
    # --------------------------------------------------------

    if TRADING_ENABLED:

        execute_trade(
            action=action,
            symbol=TRADE_SYMBOL,
            quantity=ORDER_QUANTITY,
        )

    else:

        print("=" * 45)
        print("Execution Engine")
        print("=" * 45)

        print("Trading Enabled : False")
        print(
            "🔒 Trading disabled: "
            "no order will be submitted."
        )

        print("=" * 45)


# ============================================================
# 程序入口
# ============================================================

if __name__ == "__main__":
    main()