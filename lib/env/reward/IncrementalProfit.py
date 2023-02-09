import pandas as pd

from typing import List, Callable

from lib.env.reward.BaseRewardStrategy import BaseRewardStrategy


class IncrementalProfit(BaseRewardStrategy):
    last_bought: int = 0
    last_sold: int = 0

    def __init__(self):
        pass

    def reset_reward(self):
        pass

    def get_reward(self,
                   current_step: int,
                   current_price: Callable[[str], float],
                   observations: pd.DataFrame,
                   account_history: pd.DataFrame,
                   net_worths: List[float]) -> float:
        reward = 0

        curr_balance = account_history['balance'].values[-1]
        prev_balance = account_history['balance'].values[-2] if len(account_history['balance']) > 1 else curr_balance

        #此为非卖空模型
        #当前balance大于前一个,必然为平仓所得,reward为worth[-1] - 买入点worh
        if curr_balance > prev_balance:
            reward = net_worths[-1] - net_worths[self.last_bought]
            self.last_sold = current_step
        #当前balance小于前一个,必然为开仓过程,reward为平仓点是否高于当前价,诱导agent在高位平仓
        elif curr_balance < prev_balance:
            reward = observations['Close'].values[self.last_sold] - current_price()
            self.last_bought = current_step

        return reward
