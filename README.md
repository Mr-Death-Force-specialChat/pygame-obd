# pygame-obd
Doesn't use pygame _yet._.
# Usage
Run the program<br>
`python3 main.py`
> [`...`]<br>

It'll show available serial connections for obd in this list, using pyobd.<br>
Type a path to one of these or any path you want, to start connecting.<br>
In the case that the engine is _off_, you might need to reconnect again after turning the engine _on_.
- _This is not filtered, rouge data will not be detected._
> Sleep for:<br>

Again, it's asking for input, this time it's a delay between prints, 0 will disable it all together,<br>
 higher than 0 will set a wait time.
- _This is not filtered, rouge data will not be detected._
> numbers and numbers [F,M,T][E,RR,O,R]<br>

This is the output, FMT specifies the format of the numbers.<br>
While ERROR, specifies which one of these values raised an exception,<br>
 this will also set the value to -1. EG.
- 4096 64 kph -1% [RPM,SPEED,THROT][THROTTLE,]<br>
The _THROTTLE_, in ERROR shows that the script couldn't retreive the THROTTLE value.<br>
The _-1%_, also does that.<br>
The _RPM,SPEED,THROT_ shows:
1. 1st Number (4096) is the       RPM     (int)
2. 2nd Number (64)   is the       speed   (kph)
3. 3rd Number (-1)   is the       THROTTLE  (%)
- _These numbers are padded when printed_
- _This example is an incomplete version of PAGE 0_
### Pages
If you press a number then enter, it'll switch to that page.<br>
Page 0 shows RPM SPEED THROTTLE RELATIVE_THROTTLE MASS_AIRFLOW. <br>
Page 1 is an untested raw array of DTCs.<br>
Page 2 shows COOLANT INTAKE AMBIANT_AIR OIL temperatures.<br>
Page 16 exits the script.<br>
- _Pressing an invalid page number will display nothing._
- _This is not filtered, rouge data will not be detected._
### Exiting
Press CTRL-C twice.
# Using pygame
Run the program<br>
`python3 test.py`
> [`...`]<br>

It'll show available serial connections for obd in this list, using pyobd.<br>
Type a path to one of these or any path you want, to start connecting.<br>
In the case that the engine is _off_, you might need to reconnect again after turning the engine _on_.
- _This is not filtered, rouge data will not be detected._
> Sleep for:<br>

Again, it's asking for input, this time it's a delay between prints, 0 will disable it all together,<br>
 higher than 0 will set a wait time.
- _This is not filtered, rouge data will not be detected._
> window<br>

Window showing data.<br>
Similar format to `main.py`, First line is the FMT, second is data, third is unavailable data.<br>
The window shows subpages 0 and 1 at once, however the original subpage 1 [DTC] is removed.<br>
Only one page is available, being page 0, changing to a different page is simple,<br>
 in the console write the page number, then press enter, <br>
 only one page is available.<br>
Exiting is as simple as pressing 16 then enter, or closing the window.<br>
