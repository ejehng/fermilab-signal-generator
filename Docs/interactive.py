from machine import Pin
import time
import select
import sys

led = Pin(25, Pin.OUT)

print("=== Pico 2 LED Control ===")
print("Commands:")
print("  on     - Turn LED on")
print("  off    - Turn LED off")
print("  blink  - Blink LED continuously")
print("  speed  - Change blink speed")
print("  quit   - Stop and exit")
print("===========================")

blinking = False
delay = 0.5

while True:
    if blinking:
        # Check if there's input waiting while blinking
        led.toggle()
        
        # Wait for delay, but check for input frequently
        start_time = time.time()
        while time.time() - start_time < delay:
            # Check if user has typed something
            ready = select.select([sys.stdin], [], [], 0)
            if ready and ready[0]:
                command = sys.stdin.readline().strip().lower()
                print(f"\nStopping blink. Command received: '{command}'" if command else "\nStopping blink.")
                blinking = False
                led.value(0)  # Turn off LED
                # Process the command immediately
                if command == "on":
                    led.value(1)
                    print("LED is ON")
                elif command == "off":
                    led.value(0)
                    print("LED is OFF")
                elif command == "quit":
                    led.value(0)
                    print("Goodbye!")
                    sys.exit()
                elif command == "speed":
                    try:
                        print("Enter blink delay in seconds (e.g., 0.1): ", end="")
                        new_speed = float(input())
                        if new_speed > 0:
                            delay = new_speed
                            print(f"Blink speed set to {delay} seconds")
                        else:
                            print("Speed must be positive")
                    except ValueError:
                        print("Please enter a valid number")
                elif command == "":
                    print("Blinking stopped.")
                break
    else:
        # Wait for command
        command = input("\nEnter command: ").strip().lower()
        
        if command == "on":
            led.value(1)
            print("LED is ON")
            
        elif command == "off":
            led.value(0)
            print("LED is OFF")
            
        elif command == "blink":
            blinking = True
            print(f"LED blinking every {delay} seconds")
            print("(Press Enter to stop blinking)")
            
        elif command == "speed":
            try:
                new_speed = float(input("Enter blink delay in seconds (e.g., 0.1): "))
                if new_speed > 0:
                    delay = new_speed
                    print(f"Blink speed set to {delay} seconds")
                else:
                    print("Speed must be positive")
            except ValueError:
                print("Please enter a valid number")
                
        elif command == "quit":
            led.value(0)
            print("Goodbye!")
            break
            
        else:
            print("Unknown command. Try: on, off, blink, speed, quit")