# main.py — minimal Si5351 bring-up demo
# Wiring: SDA=GP4 (pin 6), SCL=GP5 (pin 7)

from machine import Pin, I2C
from SI5351userinput import SI5351

# Board/Chip Constants
SDA_PIN, SCL_PIN = 4, 5
I2C_ID = 0
I2C_FREQ = 400_000
SI5351_ADDR = 0x60
XTAL_HZ = 25_000_000

# PLLA: VCO = 32 * 25 MHz = 800 MHz
PLL_MULT, PLL_NUM, PLL_DENOM = 32, 0, 1

# CLK0: 800 MHz / (17 + 1/47) = 47 MHz
OUT_DIV, OUT_NUM, OUT_DENOM = 17, 1, 47


def main():
    i2c = I2C(I2C_ID, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=I2C_FREQ)
    
    # Check I2C connection
    found = i2c.scan()
    print("I2C scan:", [hex(a) for a in found])
    if SI5351_ADDR not in found:
        print(f"Si5351 NOT found at {hex(SI5351_ADDR)} - check power and wiring")
        return

    # Initialize SI5351
    si = SI5351(i2c, address=SI5351_ADDR, crystalFreq=XTAL_HZ)
    si.begin()

    # Configure PLL and output
    si.setupPLL(PLL_MULT, PLL_NUM, PLL_DENOM)
    si.setupMultisynth(0, OUT_DIV, OUT_NUM, OUT_DENOM, pllsource="A")
    si.PLLsoftreset()
    si.enableOutputs(True)

    print("CLK0 set to 47 MHz")


if __name__ == "__main__":
    main()