import machine
import time


def main():
    # Use the internal temperature sensor
    sensor_temp = machine.ADC(machine.ADC.CORE_TEMP)

    # Conversion factor for the internal temperature sensor
    # The RP2350 temperature sensor outputs 0.706V at 27°C, with a slope of -1.721 mV/°C
    conversion_factor = 3.3 / (65535)

    while True:
        # Read the sensor value (12-bit ADC)
        reading = sensor_temp.read_u16()
        
        # Convert to voltage
        voltage = reading * conversion_factor
        
        # Convert to temperature in °C
        # Temperature = 27 - (voltage - 0.706) / 0.001721
        temperature = 27 - (voltage - 0.706) / 0.001721
        # hello
        print(f"Temperature: {temperature:.2f}°C")
        
        time.sleep(1)


if __name__ == "__main__":
    main()
