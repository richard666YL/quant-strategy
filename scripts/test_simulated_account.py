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

return_code, accounts = trade_context.get_acc_list()

if return_code != RET_OK:
    print("账户读取失败")
    print(accounts)
    trade_context.close()
    raise SystemExit(1)

simulated_accounts = accounts[
    accounts["trd_env"] == TrdEnv.SIMULATE
]

if simulated_accounts.empty:
    print("没有找到美股模拟账户")
    trade_context.close()
    raise SystemExit(1)

account_id = int(simulated_accounts.iloc[0]["acc_id"])

print(f"模拟账户 ID：{account_id}")

return_code, funds = trade_context.accinfo_query(
    trd_env=TrdEnv.SIMULATE,
    acc_id=account_id,
)

if return_code == RET_OK:
    print("账户资金读取成功")
    print(
        funds[
            [
                "total_assets",
                "cash",
                "market_val",
                "power",
            ]
        ]
    )
else:
    print("账户资金读取失败")
    print(funds)

trade_context.close()