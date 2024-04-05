from ManualStrategy import ManualStrategy
from StrategyLearner import StrategyLearner
from experiment1 import compare
from experiment2 import evaluate_e2
import time
import datetime as dt
def author(self):
    return 'szhou401'
if __name__ == '__main__':
 
    ms = ManualStrategy()
    ms.evaluate_ms()
# experiment 1
    print('--------experiment 1---------')
    compare()
    print('--------experiment 2---------')
    evaluate_e2()
