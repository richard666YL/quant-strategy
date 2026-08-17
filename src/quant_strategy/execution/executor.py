import time

from moomoo import (
    ModifyOrderOp,
    OpenQuoteContext,
    OpenSecTradeContext,
    RET_OK,
    SecurityFirm,
    TrdEnv,
    TrdMarket,
    TrdSide,
)


# ============================================================
# Execution 配置
# ============================================================

HOST = "127.0.0.1"
PORT = 11111

TRADING_ENV = TrdEnv.SIMULATE

MAX_ORDER_QUANTITY = 1

MAX_CHECKS = 5
CHECK_INTERVAL = 2

PENDING_ORDER_STATUSES = [
    "SUBMITTING",
    "SUBMITTED",
]


# ============================================================
# 等待撤单完成
# ============================================================

def wait_for_cancel(
    trade_context,
    order_id: str,
) -> bool:

    for attempt in range(MAX_CHECKS):

        return_code, order_data = (
            trade_context.order_list_query(
                order_id=order_id,
                trd_env=TRADING_ENV,
            )
        )

        if return_code != RET_OK:

            print("❌ 查询撤单状态失败")
            print(order_data)

            return False

        if order_data.empty:

            print(
                f"第 {attempt + 1} 次撤单检查："
                "暂时没有找到订单"
            )

            time.sleep(CHECK_INTERVAL)
            continue

        order_status = (
            order_data["order_status"].iloc[0]
        )

        print(
            f"第 {attempt + 1} 次撤单检查："
            f"status={order_status}"
        )

        if order_status == "CANCELLED_ALL":

            print("✅ 已确认旧订单全部取消")
            return True

        if order_status not in PENDING_ORDER_STATUSES:

            print(
                "⚠️ 订单进入其他最终状态："
                f"{order_status}"
            )

            return False

        time.sleep(CHECK_INTERVAL)

    print("⏳ 撤单确认超时")

    return False


# ============================================================
# 取消指定订单
# ============================================================

def cancel_order(
    trade_context,
    order_id: str,
) -> bool:

    print(
        f"准备取消订单：{order_id}"
    )

    return_code, cancel_data = (
        trade_context.modify_order(
            ModifyOrderOp.CANCEL,
            order_id,
            0,
            0,
            trd_env=TRADING_ENV,
        )
    )

    if return_code != RET_OK:

        print("❌ 撤单请求失败")
        print(cancel_data)

        return False

    print("✅ 撤单请求提交成功")

    return wait_for_cancel(
        trade_context,
        order_id,
    )


# ============================================================
# 主执行函数
# ============================================================

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

    # ========================================================
    # 0. HOLD
    # ========================================================

    if action == "HOLD":

        print("HOLD：不需要提交订单")
        return

    # ========================================================
    # 1. 安全检查
    # ========================================================

    if TRADING_ENV != TrdEnv.SIMULATE:

        raise RuntimeError(
            "Live trading is disabled."
        )

    if quantity <= 0:

        raise ValueError(
            f"非法订单数量：{quantity}"
        )

    if quantity > MAX_ORDER_QUANTITY:

        raise RuntimeError(
            f"订单数量超过安全限制：{quantity}"
        )

    if action not in [
        "BUY",
        "SELL",
        "CANCEL_PENDING",
    ]:

        raise ValueError(
            f"未知交易动作：{action}"
        )

    # ========================================================
    # 2. 建立交易连接
    # ========================================================

    trade_context = OpenSecTradeContext(
        filter_trdmarket=TrdMarket.US,
        host=HOST,
        port=PORT,
        security_firm=SecurityFirm.FUTUINC,
    )

    # ========================================================
    # 3. 查询 Pending Orders
    # ========================================================

    return_code, existing_orders = (
        trade_context.order_list_query(
            code=symbol,
            trd_env=TRADING_ENV,
        )
    )

    if return_code != RET_OK:

        trade_context.close()

        raise RuntimeError(
            f"查询已有订单失败："
            f"{existing_orders}"
        )

    if existing_orders.empty:

        pending_orders = existing_orders

    else:

        pending_orders = existing_orders[
            existing_orders[
                "order_status"
            ].isin(PENDING_ORDER_STATUSES)
        ]

    # ========================================================
    # 4. CANCEL_PENDING
    # ========================================================

    if action == "CANCEL_PENDING":

        if pending_orders.empty:

            print(
                "✅ 当前没有需要取消的未完成订单"
            )

            trade_context.close()
            return

        print(
            "⚠️ 当前仓位已经达到策略目标，"
            "但仍存在未完成订单。"
        )

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

        for _, row in pending_orders.iterrows():

            order_id = str(
                row["order_id"]
            )

            cancel_success = cancel_order(
                trade_context,
                order_id,
            )

            if not cancel_success:

                print(
                    "❌ 无法确认订单取消，"
                    "停止后续处理。"
                )

                trade_context.close()
                return

        print(
            "✅ 所有多余 Pending Orders "
            "已经处理完成"
        )

        trade_context.close()
        return

    # ========================================================
    # 5. BUY / SELL
    # ========================================================

    if action == "BUY":

        trade_side = TrdSide.BUY
        opposite_side = "SELL"

    else:

        trade_side = TrdSide.SELL
        opposite_side = "BUY"

    # ========================================================
    # 6. 同方向订单检查
    # ========================================================

    if not pending_orders.empty:

        same_side_orders = pending_orders[
            pending_orders[
                "trd_side"
            ] == action
        ]

        if not same_side_orders.empty:

            print(
                "⚠️ 已存在同方向未完成订单，"
                "本次不重复下单。"
            )

            trade_context.close()
            return

    # ========================================================
    # 7. 反方向订单检查
    # ========================================================

    if not pending_orders.empty:

        opposite_orders = pending_orders[
            pending_orders[
                "trd_side"
            ] == opposite_side
        ]

        if not opposite_orders.empty:

            print(
                "⚠️ 检测到反方向未完成订单"
            )

            for _, row in opposite_orders.iterrows():

                old_order_id = str(
                    row["order_id"]
                )

                dealt_qty = float(
                    row["dealt_qty"]
                )

                # --------------------------------------------
                # 已经部分成交
                # --------------------------------------------

                if dealt_qty > 0:

                    print(
                        "⚠️ 反方向订单已经部分成交"
                    )

                    print(
                        f"Order ID  : "
                        f"{old_order_id}"
                    )

                    print(
                        f"Dealt Qty : "
                        f"{dealt_qty}"
                    )

                    print(
                        "现实仓位可能已经发生变化。"
                    )

                    print(
                        "停止本轮执行，"
                        "请重新运行策略。"
                    )

                    trade_context.close()
                    return

                # --------------------------------------------
                # 完全没成交 → 自动取消
                # --------------------------------------------

                cancel_success = cancel_order(
                    trade_context,
                    old_order_id,
                )

                if not cancel_success:

                    print(
                        "❌ 无法确认反方向订单取消，"
                        "停止执行。"
                    )

                    trade_context.close()
                    return

        print(
            "✅ 没有阻止新交易的未完成订单"
        )

    else:

        print(
            "✅ 当前没有未完成订单"
        )

    # ========================================================
    # 8. 获取当前价格
    # ========================================================

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
        trade_context.close()

        raise RuntimeError(
            f"读取行情失败：{quote_data}"
        )

    last_price = float(
        quote_data["last_price"].iloc[0]
    )

    quote_context.close()

    print(
        f"Current Price : {last_price}"
    )

    # ========================================================
    # 9. 第一层确认：提交新订单
    # ========================================================

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

    print(
        "✅ 第一层确认：订单提交成功"
    )

    print(
        f"Order ID : {order_id}"
    )

    # ========================================================
    # 10. 第二层确认：轮询订单
    # ========================================================

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
            status_data[
                "order_status"
            ].iloc[0]
        )

        dealt_qty = float(
            status_data[
                "dealt_qty"
            ].iloc[0]
        )

        print(
            f"第 {attempt + 1} 次检查："
            f"status={order_status}, "
            f"dealt_qty={dealt_qty}"
        )

        if order_status in PENDING_ORDER_STATUSES:

            time.sleep(CHECK_INTERVAL)
            continue

        print(
            "✅ 第二层确认："
            f"订单进入最终状态 "
            f"{order_status}"
        )

        # ====================================================
        # 11. 第三层确认：检查持仓
        # ====================================================

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
                    position_data[
                        "qty"
                    ].iloc[0]
                )

                print(
                    "✅ 第三层确认："
                    "持仓查询成功"
                )

                print(
                    f"Current Position : "
                    f"{current_qty}"
                )

        else:

            print(
                "订单没有全部成交，"
                "不进行第三层确认。"
            )

        break

    else:

        print(
            "⏳ 订单仍未进入最终状态，"
            "停止轮询。"
        )

    trade_context.close()