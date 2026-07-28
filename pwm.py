from machine import Pin, PWM, Timer

def main():
    """
    Main loop that generates a square wave on GPIO 1 (GP1) based on user input.
    Uses hardware PWM for frequencies >= 8 Hz, and hardware timer for < 8 Hz
    (since hardware PWM has a minimum frequency limit).
    """
    
    while True:
        # try:
        user_input = (input("Enter target frequency in Hz (e.g. 8-10,000,000), or 'q' to quit: "))
        
        if user_input == 'q':
            print("Exiting program.")
            break

        target_freq = int(user_input)

        # For frequencies below 8 Hz, use hardware timer to toggle pin
        # (hardware PWM cannot go below ~8 Hz due to clock divider limits)
        if target_freq > 0 and target_freq < 8:
            # Configure GPIO 1 as output
            out = Pin(1, Pin.OUT)
            # Create a timer object using timer -1 (any available timer)
            tim = Timer(-1)
            # Calculate timer frequency: to get target_freq square wave,
            # we need to toggle the pin twice per cycle (high then low)
            # So timer_freq = 2 * target_freq
            timer_freq = 2 * target_freq
            # Initialize timer in periodic mode with calculated frequency
            # Callback toggles the output pin each time it fires
            tim.init(freq=timer_freq, mode=Timer.PERIODIC, callback=lambda t: out.toggle())
        
        # For frequencies 8 Hz to 10 MHz, use hardware PWM
        elif target_freq >= 8 and target_freq < 10_000_000:
            # Create PWM object on GPIO 1
            pwm = PWM(Pin(1))
            # Set the desired output frequency
            pwm.freq(target_freq)        # frequency in Hz
            # Set 50% duty cycle (32768/65535 = 50% of 16-bit range)
            # This produces a clean square wave
            pwm.duty_u16(32768)
        
        else:
            # Frequency outside valid range
            print("Out of range.")
            continue
        
        # Confirm output frequency
        print("CLK0 should now be " + str(target_freq) + " Hz.")

if __name__ == "__main__":
    main()


"""
PWM out on GPIO 1 — Raspberry Pi Pico (MicroPython).

GP1 -> BNC center pin, GND -> BNC shield.
Output is a 3.3 V logic-level square wave (hardware PWM, runs on its own).
Save as main.py on the Pico to run at boot.
"""


"""
1 Hz square wave on GPIO 1 — Raspberry Pi Pico (MicroPython).

GP1 -> BNC center pin, GND -> BNC shield.
3.3 V logic-level output, 50% duty.

Note: the Pico's hardware PWM can't go below ~8 Hz (125 MHz clock,
max divider 256, 16-bit counter -> min ~7.5 Hz), so pwm.freq(1) would
raise ValueError. For 1 Hz we toggle the pin from a hardware timer
instead — still fully autonomous, no busy loop.

Save as main.py on the Pico to run at boot.
"""


# To stop the output later:
#   tim.deinit(); out.value(0)