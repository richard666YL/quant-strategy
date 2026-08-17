from quant_strategy.broker.moomoo_orders import (
    get_pending_orders,
)


SYMBOL = "US.QQQ"


pending_orders = get_pending_orders(
    SYMBOL
)


if pending_orders.empty:

    print("✅ 当前没有 QQQ 未完成订单")

else:

    print("⚠️ 当前存在 QQQ 未完成订单")

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