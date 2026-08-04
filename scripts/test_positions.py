from moomoo import (
    OpenSecTradeContext,
    RET_OK,
    SecurityFirm,
    TrdEnv,
    TrdMarket,
)


HOST = "127.0.0.1"
PORT = 11111


trade_context = OpenSecTradeContext(
    filter_trdmarket=TrdMarket.US,
    host=HOST,
    port=PORT,
    security_firm=SecurityFirm.FUTUSECURITIES,
)

return_code, positions = trade_context.position_list_query(
    trd_env=TrdEnv.SIMULATE,
)

if return_code == RET_OK:
    print("模拟持仓读取成功")

    if positions.empty:
        print("当前没有任何持仓")
    else:
        print(
            positions[
                [
                    "code",
                    "stock_name",
                    "qty",
                    "can_sell_qty",
                    "cost_price",
                    "nominal_price",
                    "market_val",
                    "pl_val",
                    "pl_ratio",
                ]
            ]
        )
else:
    print("持仓读取失败")
    print(positions)

trade_context.close()