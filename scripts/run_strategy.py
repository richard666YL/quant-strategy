from quant_strategy.broker.moomoo_orders import (
    get_pending_orders,
)
from quant_strategy.broker.moomoo_position import (
    get_current_position,
)
from quant_strategy.execution.executor import (
    execute_trade,
)
from quant_strategy.strategies.ma_target_position import (
    calculate_ma_target_position,
)
from quant_strategy.trader.decision import (
    decide_action,
)
from quant_strategy.utils.data_loader import (
    load_daily_data,
)


# ============================================================
# 配置
# ============================================================

DATA_TICKER = "QQQ"
TRADE_SYMBOL = "US.QQQ"

SHORT_WINDOW = 20
LONG_WINDOW = 50

ORDER_QUANTITY = 1

# 总交易开关
TRADING_ENABLED = False


# ============================================================
# 主程序
# ============================================================

def main() -> None:

    # --------------------------------------------------------
    # 1. 历史数据
    # --------------------------------------------------------

    data = load_daily_data(
        DATA_TICKER
    )

    # --------------------------------------------------------
    # 2. Target Position
    # --------------------------------------------------------

    target_position = (
        calculate_ma_target_position(
            prices=data["Adj Close"],
            short_window=SHORT_WINDOW,
            long_window=LONG_WINDOW,
        )
    )

    # --------------------------------------------------------
    # 3. Current Position
    # --------------------------------------------------------

    current_position = (
        get_current_position(
            TRADE_SYMBOL
        )
    )

    # --------------------------------------------------------
    # 4. Pending Orders
    # --------------------------------------------------------

    pending_orders = (
        get_pending_orders(
            TRADE_SYMBOL
        )
    )

    pending_order_count = len(
        pending_orders
    )

    # --------------------------------------------------------
    # 5. Decision
    # --------------------------------------------------------

    action = decide_action(
        target_position=target_position,
        current_position=current_position,
        pending_orders=pending_orders,
    )

    # --------------------------------------------------------
    # 6. 状态输出
    # --------------------------------------------------------

    print("=" * 50)
    print("MA20 / MA50 Trading Summary")
    print("=" * 50)

    print(
        f"Symbol           : "
        f"{TRADE_SYMBOL}"
    )

    print(
        f"Short MA         : "
        f"{SHORT_WINDOW}"
    )

    print(
        f"Long MA          : "
        f"{LONG_WINDOW}"
    )

    print(
        f"Target Position  : "
        f"{target_position}"
    )

    print(
        f"Current Position : "
        f"{current_position}"
    )

    print(
        f"Pending Orders   : "
        f"{pending_order_count}"
    )

    print(
        f"Decision         : "
        f"{action}"
    )

    print("=" * 50)

    # --------------------------------------------------------
    # Pending Order Details
    # --------------------------------------------------------

    if not pending_orders.empty:

        print("Pending Order Details:")

        print(
            pending_orders[
                [
                    "order_id",
                    "code",
                    "trd_side",
                    "qty",
                    "dealt_qty",
                    "price",
                    "order_status",
                ]
            ]
        )

        print("=" * 50)

    # --------------------------------------------------------
    # 7. Execution
    # --------------------------------------------------------

    if TRADING_ENABLED:

        execute_trade(
            action=action,
            symbol=TRADE_SYMBOL,
            quantity=ORDER_QUANTITY,
        )

    else:

        print("=" * 50)
        print("Execution Engine")
        print("=" * 50)

        print(
            "Trading Enabled : False"
        )

        print(
            "🔒 Trading disabled: "
            "no order will be submitted."
        )

        print("=" * 50)


# ============================================================
# 程序入口
# ============================================================

if __name__ == "__main__":
    main()