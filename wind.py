import time
import lgpio
from sensors import read_float  # reuse I2C function

STEP_PIN = 22
DIR_PIN = 23
CHIP = 0

STEP_DELAY = 0.002
STEP_ANGLE = 1.8
MICROSTEPPING = 1
DEG_PER_STEP = STEP_ANGLE / MICROSTEPPING
SCAN_STEP_DEGREES = 5
SCAN_STEPS = int(SCAN_STEP_DEGREES / DEG_PER_STEP)

def step(chip, steps, direction):
    lgpio.gpio_write(chip, DIR_PIN, direction)
    for _ in range(steps):
        lgpio.gpio_write(chip, STEP_PIN, 1)
        time.sleep(STEP_DELAY)
        lgpio.gpio_write(chip, STEP_PIN, 0)
        time.sleep(STEP_DELAY)

def wind_loop():
    chip = lgpio.gpiochip_open(CHIP)
    lgpio.gpio_claim_output(chip, STEP_PIN)
    lgpio.gpio_claim_output(chip, DIR_PIN)

    print("🌬️ Wind turbine tracking started...")

    while True:
        best_voltage = -1
        best_offset = 0

        for offset in range(-3, 4):
            steps = abs(offset) * SCAN_STEPS
            direction = 1 if offset > 0 else 0

            if offset != 0:
                step(chip, steps, direction)
                time.sleep(0.1)

            voltage = read_float()
            print(f"Offset {offset*SCAN_STEP_DEGREES:+}°, Voltage={voltage:.3f} V")

            if voltage > best_voltage:
                best_voltage = voltage
                best_offset = offset

        print(f"➡️ Best wind direction: {best_offset * SCAN_STEP_DEGREES:+}°")

        if best_offset != 0:
            step(chip, abs(best_offset) * SCAN_STEPS,
                 0 if best_offset > 0 else 1)

        time.sleep(10)
