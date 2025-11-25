# SunWhirl IoT Node

This project implements an IoT control node for a hybrid solar and wind energy system. It runs on a single board computer (like a Raspberry Pi) and communicates with an Arduino-based sensor node via I2C.

## Features

- **Solar Tracking**: Calculates sun position (Azimuth/Elevation) for Tunis and adjusts servos to orient solar panels for maximum efficiency.
- **Wind Tracking**: Rotates a wind turbine using a stepper motor to find the optimal direction based on voltage output (MPPT-like scanning).
- **Sensor Monitoring**: Reads voltage and current data for both solar and wind inputs from an I2C-connected Arduino.
- **Multi-threaded**: Runs tracking and monitoring loops concurrently.

## Project Structure

- `main.py`: Entry point. Initializes and starts the sensor, wind, and solar threads.
- `solar.py`: Handles sun position calculation (using `astral`) and servo control (using `lgpio`).
- `wind.py`: Manages stepper motor control and the wind direction search algorithm.
- `sensors.py`: Reads float data from the I2C bus.
- `arduino_sensors.ino`: Arduino sketch for reading analog sensors and serving data over I2C.

## Hardware Requirements

- Raspberry Pi (or compatible SBC with `lgpio` support)
- Arduino (configured as I2C slave at address `0x08`)
- Stepper Motor & Driver (for wind turbine)
- 2x Servos (for solar panel dual-axis tracking)
- Voltage & Current Sensors

## Dependencies

Install the required Python libraries:

```bash
pip install lgpio smbus2 astral
```

## Usage

Run the main script to start all systems:

```bash
python main.py
```
