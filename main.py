import threading
import time

from sensors import sensor_loop
from wind_tracker import wind_loop
from solar_tracker import solar_loop

print("\n=====================================")
print("main.py STARTED — ALL SYSTEMS RUNNING")
print("=====================================\n")

t1 = threading.Thread(target=sensor_loop, daemon=True)
t2 = threading.Thread(target=wind_loop, daemon=True)
t3 = threading.Thread(target=solar_loop, daemon=True)

t1.start()
t2.start()
t3.start()

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\n🛑 Stopping system...")
    time.sleep(1)
    print("Done.")
