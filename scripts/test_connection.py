from moomoo import OpenQuoteContext, RET_OK


HOST = "127.0.0.1"
PORT = 11111


quote_context = OpenQuoteContext(
    host=HOST,
    port=PORT,
)

return_code, data = quote_context.get_market_snapshot(
    ["US.QQQ"]
)

if return_code == RET_OK:
    print("✅ 连接成功！")

    print(
        data[
            [
                "code",
                "name",
                "last_price",
                "open_price",
                "high_price",
                "low_price",
                "prev_close_price",
                "volume",
            ]
        ]
    )
else:
    print("❌ 连接失败")
    print(data)

quote_context.close()