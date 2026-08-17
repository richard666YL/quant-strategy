import pandas as pd

from quant_strategy.trader.decision import decide_action


def make_pending_orders(
    side: str | None = None,
) -> pd.DataFrame:
    """
    构造测试用 Pending Orders。

    side=None
        → 返回空 DataFrame

    side="BUY"
        → 模拟一个未完成 BUY 订单

    side="SELL"
        → 模拟一个未完成 SELL 订单
    """

    if side is None:
        return pd.DataFrame(
            columns=[
                "trd_side",
            ]
        )

    return pd.DataFrame(
        {
            "trd_side": [side],
        }
    )


# ============================================================
# 1. Target=0, Current=0, 没有 Pending
# → HOLD
# ============================================================

action = decide_action(
    target_position=0,
    current_position=0,
    pending_orders=make_pending_orders(),
)

print(
    "Test 1:",
    action,
)

assert action == "HOLD"


# ============================================================
# 2. Target=1, Current=0, 没有 Pending
# → BUY
# ============================================================

action = decide_action(
    target_position=1,
    current_position=0,
    pending_orders=make_pending_orders(),
)

print(
    "Test 2:",
    action,
)

assert action == "BUY"


# ============================================================
# 3. Target=0, Current=1, 没有 Pending
# → SELL
# ============================================================

action = decide_action(
    target_position=0,
    current_position=1,
    pending_orders=make_pending_orders(),
)

print(
    "Test 3:",
    action,
)

assert action == "SELL"


# ============================================================
# 4. Target=1, Current=1, 没有 Pending
# → HOLD
# ============================================================

action = decide_action(
    target_position=1,
    current_position=1,
    pending_orders=make_pending_orders(),
)

print(
    "Test 4:",
    action,
)

assert action == "HOLD"


# ============================================================
# 5. Target=1, Current=0, 已有 Pending BUY
# → HOLD
# 因为 BUY 已经在路上
# ============================================================

action = decide_action(
    target_position=1,
    current_position=0,
    pending_orders=make_pending_orders(
        "BUY"
    ),
)

print(
    "Test 5:",
    action,
)

assert action == "HOLD"


# ============================================================
# 6. Target=0, Current=0, 已有 Pending BUY
# → CANCEL_PENDING
# 因为已经空仓，但 BUY 会破坏目标仓位
# ============================================================

action = decide_action(
    target_position=0,
    current_position=0,
    pending_orders=make_pending_orders(
        "BUY"
    ),
)

print(
    "Test 6:",
    action,
)

assert action == "CANCEL_PENDING"


# ============================================================
# 7. Target=0, Current=1, 已有 Pending SELL
# → HOLD
# 因为 SELL 已经在路上
# ============================================================

action = decide_action(
    target_position=0,
    current_position=1,
    pending_orders=make_pending_orders(
        "SELL"
    ),
)

print(
    "Test 7:",
    action,
)

assert action == "HOLD"


# ============================================================
# 8. Target=1, Current=1, 已有 Pending SELL
# → CANCEL_PENDING
# 因为已经持仓正确，但 SELL 会破坏目标
# ============================================================

action = decide_action(
    target_position=1,
    current_position=1,
    pending_orders=make_pending_orders(
        "SELL"
    ),
)

print(
    "Test 8:",
    action,
)

assert action == "CANCEL_PENDING"


# ============================================================
# 9. Target=1, Current=0, 已有 Pending SELL
# → BUY
# Executor 后续负责先撤 SELL 再 BUY
# ============================================================

action = decide_action(
    target_position=1,
    current_position=0,
    pending_orders=make_pending_orders(
        "SELL"
    ),
)

print(
    "Test 9:",
    action,
)

assert action == "BUY"


# ============================================================
# 10. Target=0, Current=1, 已有 Pending BUY
# → SELL
# Executor 后续负责先撤 BUY 再 SELL
# ============================================================

action = decide_action(
    target_position=0,
    current_position=1,
    pending_orders=make_pending_orders(
        "BUY"
    ),
)

print(
    "Test 10:",
    action,
)

assert action == "SELL"


print("=" * 45)
print("✅ 所有 Decision + Pending 测试通过")
print("=" * 45)