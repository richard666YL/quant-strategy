from quant_strategy.trader.decision import decide_action


print(decide_action(target_position=1, current_position=0))
print(decide_action(target_position=0, current_position=1))
print(decide_action(target_position=1, current_position=1))
print(decide_action(target_position=0, current_position=0))