from moomoo import (
    OpenSecTradeContext,
    RET_OK,
    SecurityFirm,
    TrdEnv,
    TrdMarket,
)


def get_current_position(
    code: str,
    host: str = "127.0.0.1",
    port: int = 11111,
) -> int:
    """Return 1 when the simulated account holds the asset, otherwise 0."""

    trade_context = OpenSecTradeContext(
        filter_trdmarket=TrdMarket.US,
        host=host,
        port=port,
        security_firm=SecurityFirm.FUTUSECURITIES,
    )

    try:
        return_code, positions = trade_context.position_list_query(
            trd_env=TrdEnv.SIMULATE,
            code=code,
        )

        if return_code != RET_OK:
            raise RuntimeError(f"持仓读取失败：{positions}")

        if positions.empty:
            return 0

        quantity = float(positions.iloc[0]["qty"])

        if quantity > 0:
            return 1

        return 0

    finally:
        trade_context.close()