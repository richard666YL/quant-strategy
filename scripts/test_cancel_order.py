import time

from moomoo import (
    ModifyOrderOp,
    OpenSecTradeContext,
    RET_OK,
    SecurityFirm,
    TrdEnv,
    TrdMarket,
)


# ============================================================
# 配置
# ============================================================

HOST = "127.0.0.1"
PORT = 11111

TRADING_ENV = TrdEnv.SIMULATE

# 我们要取消的模拟订单
ORDER_ID = "687750"


# ============================================================
# 1. 建立交易连接
# ============================================================

trade_context = OpenSecTradeContext(
    filter_trdmarket=TrdMarket.US,
    host=HOST,
    port=PORT,
    security_firm=SecurityFirm.FUTUINC,
)


# ============================================================
# 2. 撤单之前，先查询一次订单
# ============================================================

return_code, order_data = trade_context.order_list_query(
    order_id=ORDER_ID,
    trd_env=TRADING_ENV,
)

if return_code != RET_OK:
    trade_context.close()

    raise RuntimeError(
        f"查询订单失败：{order_data}"
    )


if order_data.empty:
    trade_context.close()

    raise RuntimeError(
        f"没有找到订单：{ORDER_ID}"
    )


order_status = order_data["order_status"].iloc[0]

print("=" * 45)
print("Cancel Order Test")
print("=" * 45)

print(f"Order ID       : {ORDER_ID}")
print(f"Current Status : {order_status}")


# ============================================================
# 3. 只有未完成订单才尝试取消
# ============================================================

PENDING_STATUSES = [
    "SUBMITTING",
    "SUBMITTED",
]


if order_status not in PENDING_STATUSES:

    print(
        "订单已经不是待处理状态，"
        "不需要取消。"
    )

    trade_context.close()

    raise SystemExit(0)


# ============================================================
# 4. 调用 Moomoo 撤单 API
# ============================================================

print("准备取消订单...")

return_code, cancel_data = trade_context.modify_order(
    ModifyOrderOp.CANCEL,
    ORDER_ID,
    0,
    0,
    trd_env=TRADING_ENV,
)


# ============================================================
# 5. 第一层确认：撤单请求是否被接受
# ============================================================

if return_code != RET_OK:

    print("❌ 撤单请求失败")
    print(cancel_data)

    trade_context.close()

    raise SystemExit(1)


print("✅ 撤单请求提交成功")


# ============================================================
# 6. 等待一下，让订单状态更新
# ============================================================

time.sleep(2)


# ============================================================
# 7. 第二层确认：重新查询订单状态
# ============================================================

return_code, updated_data = trade_context.order_list_query(
    order_id=ORDER_ID,
    trd_env=TRADING_ENV,
)


if return_code != RET_OK:

    print("❌ 撤单后查询订单失败")
    print(updated_data)

else:

    if updated_data.empty:

        print(
            "⚠️ 撤单后暂时没有查询到该订单"
        )

    else:

        new_status = (
            updated_data["order_status"].iloc[0]
        )

        dealt_qty = float(
            updated_data["dealt_qty"].iloc[0]
        )

        print("=" * 45)
        print("Cancel Result")
        print("=" * 45)

        print(f"Order ID    : {ORDER_ID}")
        print(f"New Status  : {new_status}")
        print(f"Dealt Qty   : {dealt_qty}")


# ============================================================
# 8. 关闭连接
# ============================================================

trade_context.close()