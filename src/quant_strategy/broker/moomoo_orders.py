from moomoo import (
    OpenSecTradeContext,
    RET_OK,
    SecurityFirm,
    TrdEnv,
    TrdMarket,
)


HOST = "127.0.0.1"
PORT = 11111

TRADING_ENV = TrdEnv.SIMULATE


PENDING_STATUSES = [
    "SUBMITTING",
    "SUBMITTED",
]


def get_pending_orders(
    symbol: str,
):
    """
    查询指定股票当前尚未完成的模拟订单。
    """

    trade_context = OpenSecTradeContext(
        filter_trdmarket=TrdMarket.US,
        host=HOST,
        port=PORT,
        security_firm=SecurityFirm.FUTUINC,
    )

    try:

        return_code, order_data = (
            trade_context.order_list_query(
                code=symbol,
                trd_env=TRADING_ENV,
            )
        )

        if return_code != RET_OK:
            raise RuntimeError(
                f"查询订单失败：{order_data}"
            )

        # 没有任何订单
        if order_data.empty:
            return order_data

        # 只保留尚未完成的订单
        pending_orders = order_data[
            order_data[
                "order_status"
            ].isin(PENDING_STATUSES)
        ]

        return pending_orders

    finally:
        trade_context.close()