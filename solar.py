import time
import lgpio
import datetime
from astral import LocationInfo
from astral.sun import azimuth, elevation

HORIZ_PIN = 17
VERT_PIN = 18
MIN_PW = 500
MAX_PW = 2500

CHIP = 0

city = LocationInfo(
    name="Tunis",
    region="Tunisia",
    timezone="Africa/Tunis",
    latitude=36.8065,
    longitude=10.1815
)

def angle_to_pulse(angle):
    angle = max(0, min(180, angle))
    return MIN_PW + (MAX_PW - MIN_PW) * (angle / 180.0)

def move_servo(chip, pin, angle):
    pulse = angle_to_pulse(angle)
    duty = (pulse / 20000.0) * 100.0
    lgpio.tx_pwm(chip, pin, 50, duty)
    time.sleep(0.35)
    lgpio.tx_pwm(chip, pin, 50, 0)

def solar_loop():
    chip = lgpio.gpiochip_open(CHIP)
    lgpio.gpio_claim_output(chip, HORIZ_PIN)
    lgpio.gpio_claim_output(chip, VERT_PIN)

    print("🌞 Solar tracking started...")

    move_servo(chip, HORIZ_PIN, 90)
    move_servo(chip, VERT_PIN, 45)

    while True:
        now = datetime.datetime.now()
        az = azimuth(city.observer, now)
        el = elevation(city.observer, now)

        print(f"Sun → Az={az:.2f}°  El={el:.2f}°")

        horiz = max(0, min(180, az))
        vert = max(0, min(90, el))

        move_servo(chip, HORIZ_PIN, horiz)
        move_servo(chip, VERT_PIN, vert)

        time.sleep(60)
