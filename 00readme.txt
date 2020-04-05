## Evaluating the performance of different methods of implementing a flashing lamp.

Cf. [https://www.plctalk.net/qanda/showthread.php?t=124383](https://www.plctalk.net/qanda/showthread.php?t=124383)

Caveats

* This is not Structured Text
* The timings are in 100microsecond (100us) units, from a MicroLogix (1763-L16BBB), based on it's free running clock.
* I am most interested in the variation wrt the mean, not the mean itself; the timer-based result means can be tweaked by adjusting the .PREset values and/or modifying other pieces of the implementation

### A single repeating timer, running on a cycle of approximately 4000ms, flashing when the accumulator value is greater than 1999:

![](https://github.com/drbitboy/PLC_2s_lamp_flash/raw/master/doc/img/single_timer.png)

### Cascading/toggling timers, running on a cycle of approximately 4000ms, flashing when one timer is DoNe:

![](https://github.com/drbitboy/PLC_2s_lamp_flash/raw/master/doc/img/cascading_timers.png)

### Real-Time Clock, using Bit 1 of the seconds of minute:

![](https://github.com/drbitboy/PLC_2s_lamp_flash/raw/master/doc/img/rtc_bit_1.png)

### Free-running clock, using Bit 14 of a counter with a period of 100us, so the nominal flash time is 1.6384s

![](https://github.com/drbitboy/PLC_2s_lamp_flash/raw/master/doc/img/free_running_clock_bit_14.png)
