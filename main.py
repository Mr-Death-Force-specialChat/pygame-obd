import obd
import time
import threading

ports = obd.scan_serial()
print(ports)
conn = obd.OBD(input())
print("Sleep for: ")
sleep_time = float(input())
obd.logger.removeHandler(obd.console_handler)

#def print_data_old():
#    rpm = conn.query(obd.commands.RPM).value.magnitude
#    speed = conn.query(obd.commands.SPEED).value.magnitude
#    rpm0 = rpm+1
#    speed0 = speed+1
#    gear_value = rpm0/speed0
#    print(speed, " kmh\t@", rpm, "\tGV.", int(gear_value))

flag=0

def print_data():
    flags=""
    try:
        if conn.supports(obd.commands.RPM):
            rpm = conn.query(obd.commands.RPM).value.magnitude
        else:
            raise AttributeError()
    except AttributeError:
        rpm = -1
        flags="ERRRPM,"
    try:
        if conn.supports(obd.commands.SPEED):
            speed = conn.query(obd.commands.SPEED).value.magnitude
        else:
            raise AttributeError()
    except AttributeError:
        speed = -1
        flags=flags+"SPEED,"
    try:
        if conn.supports(obd.commands.THROTTLE_POS):
            throttle = conn.query(obd.commands.THROTTLE_POS).value.magnitude
        else:
            raise AttributeError()
    except AttributeError:
        throttle = -1
        flags=flags+"THROTTLE,"
    try:
        if conn.supports(obd.commands.RELATIVE_THROTTLE_POS):
            rel_throttle = conn.query(obd.commands.RELATIVE_THROTTLE_POS).value.magnitude
        else:
            raise AttributeError()
    except AttributeError:
        rel_throttle = -1
        flags=flags+"REL_THROTTLE,"
    try:
        if conn.supports(obd.commands.MAF):
            airflow = conn.query(obd.commands.MAF).value.magnitude
        else:
            raise AttributeError()
    except AttributeError:
        airflow = -1
        flags=flags+"AIRFLOW,"
    rpmstr=format(f"{rpm:>8.2f}")
    speedstr=format(f"{speed:>6} kph")
    throttlestr=format(f"{throttle:.2f}%")
    rel_throttlestr=format(f"{rel_throttle:.2f}%")
    space=" "
    print(f"{rpmstr:<16}{speedstr:<16}{throttlestr:<8}{rel_throttlestr:>10}{airflow:>8.2f} {space:<4} [RPM,SPEED,THROT,REL,MAF][{flags}]")

def print_data_2():
    flags2=""
    try:
        if conn.supports(obd.commands.COOLANT_TEMP):
            coolant_temprature = conn.query(obd.commands.COOLANT_TEMP).value.magnitude
    except AttributeError:
        coolant_temprature = -1
        flags2="COOLANT,"
    try:
        if conn.supports(obd.commands.INTAKE_TEMP):
            intake_temprature = conn.query(obd.commands.INTAKE_TEMP).value.magnitude
        else:
            raise AttributeError()
    except AttributeError:
        intake_temprature = -1
        flags2=flags2+"INTAKE,"
    try:
        if conn.supports(obd.commands.AMBIANT_AIR_TEMP):
            ambiant_air_temprature = conn.query(obd.commands.AMBIANT_AIR_TEMP).value.magnitude
        else:
            raise AttributeError()
    except AttributeError:
        ambiant_air_temprature = -1
        flags2=flags2+"AMBIANT_AIR,"
    try:
        if conn.supports(obd.commands.OIL_TEMP):
            oil_temprature = conn.query(obd.commands.OIL_TEMP).value.agnitude
        else:
            raise AttributeError()
    except AttributeError:
        oil_temprature = -1
        flags2=flags2+"OIL,"
    coolant_tempraturestr = format(f"{coolant_temprature:<4.1f} C")
    intake_tempraturestr = format(f"{intake_temprature:<4.1f} C")
    ambiant_air_tempraturestr = format(f"{ambiant_air_temprature:<4.1f} C")
    oil_tempraturestr = format(f"{oil_temprature:<4.1f} C")
    print(f" {coolant_tempraturestr:<12}{intake_tempraturestr:<12}{ambiant_air_tempraturestr:<12}{oil_tempraturestr:<12}[COOLANT,INTAKE,AMBIANT_AIR,OIL][{flags2}]")


def loop():
    if flag == 0:
        print_data()
    elif flag == 1:
        try:
            print(conn.query(obd.commands.GET_DTC))
        except AttributeError:
            print("ATTRIB_ERROR")
    elif flag == 2:
        print_data_2()

def flag_set():
    global flag
    while True:
        keystroke=input()
        flag=int(keystroke)

n=threading.Thread(target=flag_set)
n.start()

if sleep_time == 0:
    while True:
        loop()
else:
    while True:
        loop()
        time.sleep(sleep_time)
