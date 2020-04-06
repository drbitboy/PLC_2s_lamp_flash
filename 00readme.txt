## Evaluating the performance of different methods of implementing a flashing lamp.

### Summary results

Standard deviations for all methods are less than a ms (calibrated-eyeball estimate); largest deviations from the mean are around 2ms.

The approximate standard deviations for the methods are:
* 0.27ms for cascading (ping pong) timers
* 0.41ms for free running clock bit 14
* 0.57ms for single timer
* 0.76ms for RTC seconds bit 01

## TL;DR

Cf. [https://www.plctalk.net/qanda/showthread.php?t=124383](https://www.plctalk.net/qanda/showthread.php?t=124383)

### Caveats

* This is not Structured Text, as requested in the PLCtalk.net thread.
* The timings are in 100microsecond (100us) units, from a MicroLogix (1763-L16BBB), based on it's free running clock.
* I am most interested in the variation wrt the mean, not the mean itself.
  * The timer-based result means are around 1ms above ideal (~2.001s)
  * Those means could be tweaked by adjusting the .PREset values and/or modifying other pieces of the implementation.

The PNG images doc/img/*_plot.png, despite their labeling, are not UCL/LCL charts in the strict sense, as there has been no test for normality first; they do plot the data along with the mean and "mean+/-3 standard deviations" levels.

### A single repeating timer, running on a cycle of approximately 4000ms, flashing when the accumulator value is greater than 1999:

![](https://github.com/drbitboy/PLC_2s_lamp_flash/raw/master/doc/img/single_timer.png)

### Two cascading (ping-pong) timers, running on a cycle of approximately 4000ms, flashing when one timer is DoNe:

![](https://github.com/drbitboy/PLC_2s_lamp_flash/raw/master/doc/img/cascading_timers.png)

### Real-Time Clock, using Bit 1 of the seconds of minute:

![](https://github.com/drbitboy/PLC_2s_lamp_flash/raw/master/doc/img/rtc_bit_1.png)

### Free-running clock, using Bit 14 of a counter with a period of 100us, so the nominal flash time is 1.6384s

![](https://github.com/drbitboy/PLC_2s_lamp_flash/raw/master/doc/img/free_running_clock_bit_14.png)
