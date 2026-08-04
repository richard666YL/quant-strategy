def decide_action(
    target_position: int,
    current_position: int,
) -> str:
    """Compare target and current positions and return an action."""

    if target_position == 1 and current_position == 0:
        return "BUY"

    if target_position == 0 and current_position == 1:
        return "SELL"

    return "HOLD"