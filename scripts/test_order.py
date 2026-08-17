import time

from moomoo import (
    OpenQuoteContext,
    OpenSecTradeContext,
    RET_OK,
    SecurityFirm,
    TrdEnv,
    TrdMarket,
    TrdSide,
)


# =========================
# 配置
# =========================

HOST = "127.0.0.1"
PORT = 11111

SYMBOL = "US.QQQ"
QUANTITY = 1

MAX_CHECKS = 5
CHECK_INTERVAL = 2

# True  = 创建一张新的模拟订单
# False = 不下新单，只查询 EXISTING_ORDER_ID
PLACE_NEW_ORDER = False

# PLACE_NEW_ORDER=False 时查询这张订单
EXISTING_ORDER_ID = "687700"


# =========================
# 1. 建立交易连接
# =========================

trade_context = OpenSecTradeContext(
    filter_trdmarket=TrdMarket.US,
    host=HOST,
    port=PORT,
    security_firm=SecurityFirm.FUTUINC,
)


# =========================
# 2. 决定是否创建新订单
# =========================

if PLACE_NEW_ORDER:

    # 2.1 建立行情连接
    quote_context = OpenQuoteContext(
        host=HOST,
        port=PORT,
    )

    # 2.2 获取 QQQ 当前价格
    return_code, quote_data = quote_context.get_market_snapshot(
        [SYMBOL]
    )

    if return_code != RET_OK:
        quote_context.close()
        trade_context.close()
        raise RuntimeError(f"读取行情失败：{quote_data}")

    last_price = float(
        quote_data["last_price"].iloc[0]
    )

    print(f"QQQ 当前价格：{last_price}")

    quote_context.close()

    # =========================
    # 第一层确认：提交模拟订单
    # =========================

    return_code, order_data = trade_context.place_order(
        price=last_price,
        qty=QUANTITY,
        code=SYMBOL,
        trd_side=TrdSide.BUY,
        trd_env=TrdEnv.SIMULATE,
    )

    if return_code != RET_OK:
        trade_context.close()
        raise RuntimeError(f"下单失败：{order_data}")

    # 自动取得刚刚生成的订单 ID
    order_id = str(
        order_data["order_id"].iloc[0]
    )

    print("✅ 第一层确认：模拟订单提交成功")
    print(f"订单 ID：{order_id}")

else:

    # 不创建新订单，直接查询已有订单
    order_id = EXISTING_ORDER_ID

    print("🚫 本次不会创建新订单")
    print(f"查询已有订单：{order_id}")


# =========================
# 3. 第二层确认：轮询订单状态
# =========================

for attempt in range(MAX_CHECKS):

    return_code, status_data = trade_context.order_list_query(
        order_id=order_id,
        trd_env=TrdEnv.SIMULATE,
    )

    if return_code != RET_OK:
        print("❌ 订单状态查询失败")
        print(status_data)
        break

    if status_data.empty:
        print(
            f"第 {attempt + 1} 次检查："
            "暂时没有查到订单"
        )

        time.sleep(CHECK_INTERVAL)
        continue

    order_status = status_data["order_status"].iloc[0]

    dealt_qty = float(
        status_data["dealt_qty"].iloc[0]
    )

    print(
        f"第 {attempt + 1} 次检查："
        f"status={order_status}, "
        f"dealt_qty={dealt_qty}"
    )

    # 订单仍在等待
    if order_status in [
        "SUBMITTING",
        "SUBMITTED",
    ]:
        time.sleep(CHECK_INTERVAL)
        continue

    # =========================
    # 订单已经进入最终状态
    # =========================

    print("✅ 第二层确认：订单已经进入最终状态")

    # =========================
    # 第三层确认：如果全部成交，检查实际持仓
    # =========================

    if order_status == "FILLED_ALL":

        print("✅ 订单已经全部成交")
        print("开始检查实际 QQQ 持仓...")

        return_code, position_data = trade_context.position_list_query(
            code=SYMBOL,
            trd_env=TrdEnv.SIMULATE,
        )

        if return_code != RET_OK:
            print("❌ 持仓查询失败")
            print(position_data)

        elif position_data.empty:
            print("⚠️ 没有找到 QQQ 持仓")

        else:
            current_qty = float(
                position_data["qty"].iloc[0]
            )

            print("✅ 第三层确认：持仓查询成功")
            print(f"当前 QQQ 持仓数量：{current_qty}")

    else:
        print(
            f"订单最终状态不是 FILLED_ALL：{order_status}"
        )

    break

else:
    print(
        "⏳ 订单暂时还没有最终结果，"
        "停止继续等待。"
    )


# =========================
# 4. 关闭交易连接
# =========================

trade_context.close()