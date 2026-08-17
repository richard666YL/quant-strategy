def decide_action(
    target_position: int,
    current_position: int,
    pending_orders=None,
) -> str:
    """
    根据：

    1. 策略目标仓位
    2. 当前实际仓位
    3. 尚未完成的订单

    决定下一步动作。

    返回：
    BUY
    SELL
    HOLD
    CANCEL_PENDING
    """

    # ========================================================
    # 1. 参数检查
    # ========================================================

    if target_position not in [0, 1]:
        raise ValueError(
            f"非法 target_position：{target_position}"
        )

    if current_position not in [0, 1]:
        raise ValueError(
            f"非法 current_position：{current_position}"
        )

    # ========================================================
    # 2. 检查 Pending Orders
    # ========================================================

    has_pending_buy = False
    has_pending_sell = False

    if pending_orders is not None:

        if not pending_orders.empty:

            has_pending_buy = (
                pending_orders["trd_side"] == "BUY"
            ).any()

            has_pending_sell = (
                pending_orders["trd_side"] == "SELL"
            ).any()

    # ========================================================
    # 3. 已经达到目标仓位
    # ========================================================

    if target_position == current_position:

        # 仓位虽然已经正确，
        # 但仍有挂单可能破坏当前目标
        if has_pending_buy or has_pending_sell:
            return "CANCEL_PENDING"

        return "HOLD"

    # ========================================================
    # 4. 目标持有，但当前空仓
    # ========================================================

    if (
        target_position == 1
        and current_position == 0
    ):

        # 已经有 BUY 在路上
        if has_pending_buy:
            return "HOLD"

        # 没有 BUY，应该买
        #
        # 即使存在 SELL，
        # Executor 会负责先取消 SELL
        return "BUY"

    # ========================================================
    # 5. 目标空仓，但当前持有
    # ========================================================

    if (
        target_position == 0
        and current_position == 1
    ):

        # 已经有 SELL 在路上
        if has_pending_sell:
            return "HOLD"

        # 没有 SELL，应该卖
        #
        # 如果存在 BUY，
        # Executor 会先取消 BUY
        return "SELL"

    return "HOLD"