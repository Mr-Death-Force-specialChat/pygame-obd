import obd
import time
import threading
import pygame

ports = obd.scan_serial()
print(ports)
conn = obd.OBD(input())
print("Sleep for: ")
sleep_time = float(input())
#sleep_time = float(0.5)
obd.logger.removeHandler(obd.console_handler)

#def print_data_old():
#    rpm = conn.query(obd.commands.RPM).value.magnitude
#    speed = conn.query(obd.commands.SPEED).value.magnitude
#    rpm0 = rpm+1
#    speed0 = speed+1
#    gear_value = rpm0/speed0
#    print(speed, " kmh\t@", rpm, "\tGV.", int(gear_value))

flag=0

def draw_text(text, font, color, x, y, screen, aa=True):
    img = font.render(text, aa, color)
    screen.blit(img, (x, y))

#def print_data():
    #print(f"{rpmstr:<16}{speedstr:<16}{throttlestr:<8}{rel_throttlestr:>10}{airflow:>8.2f} {space:<4} [RPM,SPEED,THROT,REL,MAF][{flags}]")
def draw_page0(screen, font, color, color2, x, y, y2, offset_per_char):
    flags=""
    try:
        if conn.supports(obd.commands.RPM):
            rpm = conn.query(obd.commands.RPM).value.magnitude
        else:
            raise AttributeError()
    except AttributeError:
        rpm = -1
        flags="RPM,"
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
        if conn.supports(obd.commands.INTAKE_PRESSURE):
            intake_psi = conn.query(obd.commands.INTAKE_PRESSURE).value.to("psi").magnitude
        else:
            raise AttributeError()
    except AttributeError:
        intake_psi = -1
        flags=flags+"INTAKE,"
    draw_text(f"{rpm:05.0f}", font, color, x, y, screen)
    draw_text(f"{speed:03.0f} kph", font, color, x+(offset_per_char*10), y, screen)
    draw_text(f"{throttle:06.2f}", font, color, x+(offset_per_char*26), y, screen)
    draw_text(f"{rel_throttle:06.2f}", font, color, x+(offset_per_char*42), y, screen)
    draw_text(f"{intake_psi:.2f} psi", font, color, x+(offset_per_char*55), y, screen)
    if flags != "":
        draw_text(f"[{flags}]", font, color2, x, y2, screen)

def draw_page1(screen, font, color, color2, x, y, y2, offset_per_char):
    flags2=""
    try:
        if conn.supports(obd.commands.COOLANT_TEMP):
            coolant_temprature = conn.query(obd.commands.COOLANT_TEMP).value.magnitude
        else:
            raise AttributeError()
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
    draw_text(f"{coolant_temprature:04.1f} C", font, color, x, y, screen)
    draw_text(f"{intake_temprature:04.1f} C", font, color, x+(offset_per_char*16), y, screen)
    draw_text(f"{ambiant_air_temprature:04.1f} C", font, color, x+(offset_per_char*30), y, screen)
    draw_text(f"{oil_temprature:04.1f} C", font, color, x+(offset_per_char*42), y, screen)
    if flags2 != "":
        draw_text(f"[{flags2}]", font, color2, x, y2, screen)

pygame.init()
screen = pygame.display.set_mode((640,420))
DATA_FONT = pygame.font.SysFont("Fira Code Retina", 32)
DATA_FONT2 = pygame.font.SysFont("Fira Code Retina", 32)

def prerender_text(text, font, color, aa=True):
    return font.render(text, aa, color)

def flag_set():
    global flag
    while flag != 16:
        keystroke=input()
        flag=int(keystroke)

n=threading.Thread(target=flag_set)
n.start()

run = True
BACKGROUND_COL=(16,16,16)
DATA_COL=(255,180,160)
DATA_COL2=(210,200,190)
ERR_COL=(255, 64, 64)
PAGE0=prerender_text("RPM  |    SPEED    |  THROTTLE  |  RELATIVE  |  AIRFLOW", DATA_FONT, DATA_COL)
PAGE1=prerender_text("COOLANT  |  INTAKE   |    AIR     |      OIL", DATA_FONT, DATA_COL)
while run:
    screen.fill((16,16,16))
    if flag == 0:
        screen.blit(PAGE0, (10, 10))
        screen.blit(PAGE1, (10, 116))
        draw_page0(screen, DATA_FONT2, DATA_COL2, ERR_COL, 10, 42, 74, 9)
        draw_page1(screen, DATA_FONT2, DATA_COL2, ERR_COL, 10, 148, 180, 9)
        time.sleep(sleep_time)
    elif flag == 16:
        run = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()
conn.close()
