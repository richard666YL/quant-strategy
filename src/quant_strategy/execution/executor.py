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
# Execution 配置
# =========================

HOST = "127.0.0.1"
PORT = 11111

TRADING_ENV = TrdEnv.SIMULATE

MAX_ORDER_QUANTITY = 1

MAX_CHECKS = 5
CHECK_INTERVAL = 2


def execute_trade(
    action: str,
    symbol: str,
    quantity: int,
) -> None:

    print("=" * 45)
    print("Execution Engine")
    print("=" * 45)

    print(f"Action   : {action}")
    print(f"Symbol   : {symbol}")
    print(f"Quantity : {quantity}")

    # =========================
    # 0. HOLD 不需要交易
    # =========================

    if action == "HOLD":
        print("HOLD：不需要提交订单")
        return

    # =========================
    # 安全检查
    # =========================

    if TRADING_ENV != TrdEnv.SIMULATE:
        raise RuntimeError(
            "Live trading is disabled."
        )

    if quantity > MAX_ORDER_QUANTITY:
        raise RuntimeError(
            f"订单数量超过安全限制：{quantity}"
        )

    if action not in ["BUY", "SELL"]:
        raise ValueError(
            f"未知交易动作：{action}"
        )

    # =========================
    # 1. 获取当前价格
    # =========================

    quote_context = OpenQuoteContext(
        host=HOST,
        port=PORT,
    )

    return_code, quote_data = (
        quote_context.get_market_snapshot(
            [symbol]
        )
    )

    if return_code != RET_OK:
        quote_context.close()

        raise RuntimeError(
            f"读取行情失败：{quote_data}"
        )

    last_price = float(
        quote_data["last_price"].iloc[0]
    )

    quote_context.close()

    print(f"Current Price : {last_price}")

    # =========================
    # 2. 建立交易连接
    # =========================

    trade_context = OpenSecTradeContext(
        filter_trdmarket=TrdMarket.US,
        host=HOST,
        port=PORT,
        security_firm=SecurityFirm.FUTUINC,
    )

    # =========================
    # 3. BUY / SELL
    # =========================

    if action == "BUY":
        trade_side = TrdSide.BUY
    else:
        trade_side = TrdSide.SELL

    # =========================
    # 第一层确认：提交订单
    # =========================

    return_code, order_data = (
        trade_context.place_order(
            price=last_price,
            qty=quantity,
            code=symbol,
            trd_side=trade_side,
            trd_env=TRADING_ENV,
        )
    )

    if return_code != RET_OK:
        trade_context.close()

        raise RuntimeError(
            f"订单提交失败：{order_data}"
        )

    order_id = str(
        order_data["order_id"].iloc[0]
    )

    print("✅ 第一层确认：订单提交成功")
    print(f"Order ID : {order_id}")

    # =========================
    # 第二层确认：轮询订单
    # =========================

    for attempt in range(MAX_CHECKS):

        return_code, status_data = (
            trade_context.order_list_query(
                order_id=order_id,
                trd_env=TRADING_ENV,
            )
        )

        if return_code != RET_OK:
            print("❌ 查询订单状态失败")
            print(status_data)
            break

        if status_data.empty:
            print(
                f"第 {attempt + 1} 次检查："
                "暂时没有找到订单"
            )

            time.sleep(CHECK_INTERVAL)
            continue

        order_status = (
            status_data["order_status"].iloc[0]
        )

        dealt_qty = float(
            status_data["dealt_qty"].iloc[0]
        )

        print(
            f"第 {attempt + 1} 次检查："
            f"status={order_status}, "
            f"dealt_qty={dealt_qty}"
        )

        # 订单还在处理中
        if order_status in [
            "SUBMITTING",
            "SUBMITTED",
        ]:
            time.sleep(CHECK_INTERVAL)
            continue

        print(
            "✅ 第二层确认："
            f"订单进入最终状态 {order_status}"
        )

        # =========================
        # 第三层确认：检查持仓
        # =========================

        if order_status == "FILLED_ALL":

            return_code, position_data = (
                trade_context.position_list_query(
                    code=symbol,
                    trd_env=TRADING_ENV,
                )
            )

            if return_code != RET_OK:
                print("❌ 查询持仓失败")
                print(position_data)

            elif position_data.empty:
                print(
                    "⚠️ 订单显示成交，"
                    "但没有找到对应持仓"
                )

            else:
                current_qty = float(
                    position_data["qty"].iloc[0]
                )

                print(
                    "✅ 第三层确认：持仓查询成功"
                )

                print(
                    f"Current Position : "
                    f"{current_qty}"
                )

        else:
            print(
                "订单没有全部成交，"
                "不进行第三层持仓确认。"
            )

        break

    else:
        print(
            "⏳ 订单仍未进入最终状态，"
            "停止轮询。"
        )

    # =========================
    # 关闭交易连接
    # =========================

    trade_context.close()