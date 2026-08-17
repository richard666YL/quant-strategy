from moomoo import (
    OpenSecTradeContext,
    RET_OK,
    SecurityFirm,
    TrdEnv,
    TrdMarket,
)


HOST = "127.0.0.1"
PORT = 11111

ORDER_ID = "687698"


trade_context = OpenSecTradeContext(
    filter_trdmarket=TrdMarket.US,
    host=HOST,
    port=PORT,
    security_firm=SecurityFirm.FUTUINC,
)


return_code, order_data = trade_context.order_list_query(
    order_id=ORDER_ID,
    trd_env=TrdEnv.SIMULATE,
)


if return_code == RET_OK:
    print("✅ 订单查询成功")

    if order_data.empty:
        print("没有找到这个订单")
    else:
        print(
            order_data[
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

else:
    print("❌ 订单查询失败")
    print(order_data)


trade_context.close()