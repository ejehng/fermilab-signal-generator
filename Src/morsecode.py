from machine import Pin
import time

led = Pin(25, Pin.OUT)

# Morse code dictionary (letters and numbers only)
MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    ' ': '/'
}

# Timing (seconds) - NOW LONGER
DOT = 0.25    # Dot duration (was 0.1)
DASH = 0.75   # Dash duration (was 0.3, 3x dot)
GAP = 0.25    # Gap between symbols

print("=== Morse Code Blinker ===")
print(f"Dot: {DOT}s | Dash: {DASH}s")
print("Enter a message to blink!")

while True:
    message = input("\nMessage (or 'quit'): ").upper().strip()
    
    if message == 'QUIT':
        led.value(0)
        break
    
    # Convert to Morse code
    morse = ''
    for char in message:
        if char in MORSE_CODE:
            morse += MORSE_CODE[char] + ' '
    
    if morse:
        print(f"Blinking: {morse}")
        
        # Blink the message
        for symbol in morse:
            if symbol == '.':
                led.on()
                time.sleep(DOT)
                led.off()
                time.sleep(GAP)
            elif symbol == '-':
                led.on()
                time.sleep(DASH)
                led.off()
                time.sleep(GAP)
            elif symbol == ' ':
                time.sleep(0.5)  # Letter gap
            elif symbol == '/':
                time.sleep(1.0)  # Word gap
        
        print("Done!")