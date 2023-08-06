# zeroinger
一些可以加速的python编码的常用轮子
### RaceTimer
```
from zeroinger.time.race_timer import RaceTimer
import time
timer = RaceTimer.create_instance()
time.sleep(1)
print(timer.snapshot())
time.sleep(1)
print(timer.duriation())
timer.reset()
time.sleep(1)
print(timer.duriation())
pass
#--------------------------------
1000
2002
1003
```
