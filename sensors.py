import smbus2
import struct
import time

I2C_ADDR = 0x08
bus = smbus2.SMBus(1)

def read_float():
    data = bus.read_i2c_block_data(I2C_ADDR, 0, 4)
    return struct.unpack('f', bytes(data))[0]

def sensor_loop():
    while True:
        try:
            print("\n----- SENSOR DATA -----")
            pv_voltage = read_float()
            wind_voltage = read_float()
            pv_current = read_float()
            wind_current = read_float()

            print(f"PV Voltage:   {pv_voltage:.2f} V")
            print(f"Wind Voltage: {wind_voltage:.2f} V")
            print(f"PV Current:   {pv_current:.2f} A")
            print(f"Wind Current: {wind_current:.2f} A")
            print("------------------------\n")

        except Exception as e:
            print("⚠️ Sensor I2C read error:", e)

        time.sleep(0.5)
