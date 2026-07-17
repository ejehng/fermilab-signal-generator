"""
Pi Pico code to configure Si5351A clock generator for 75MHz output on CLK0

Si5351 Hardware Connections:
- Pin 5 (GP3/SCL) <-> SCL
- Pin 4 (GP2/SDA) <-> SDA
- Pin 36 (3V3 OUT) <-> VCC
- Pin 38 (GND) <-> GND

I2C Address: 0x60 (XA and XB grounded or unconnected)

For 75MHz on CLK0:
- PLLA = 900MHz (using 25MHz crystal, multiplier=36)
- CLK0 divider = 12 (integer, 900MHz / 12 = 75MHz)

The P1 formula for multisynth is: P1 = 128*a + b - 512
For a=12 (divider), b=0: P1 = 128*12 + 0 - 512 = 1024
"""

from machine import Pin, I2C
import time

# I2C configuration for Pi Pico
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)

SI5351_ADDRESS = 0x60

def si5351_write(reg, value):
    """Write a byte to Si5351 register"""
    try:
        i2c.writeto_mem(SI5351_ADDRESS, reg, bytes([value]))
        return True
    except:
        return False

def si5351_read(reg):
    """Read a byte from Si5351 register"""
    try:
        return i2c.readfrom_mem(SI5351_ADDRESS, reg, 1)[0]
    except:
        return None

def si5351_init():
    """Initialize Si5351A"""
    # Reset the device
    si5351_write(177, 0xAC)
    time.sleep_ms(10)
    
    # Disable all clock outputs
    si5351_write(3, 0xFF)
    
    # Configure PLLA for 900MHz (with 25MHz crystal)
    # F_vco = 25MHz * 36 = 900MHz
    # P1 = 128*36 - 512 = 4096 = 0x1000
    si5351_write(25, 0x80)   # PLLA source = XTAL, P3 = 128
    si5351_write(26, 0x10)   # P1[15:8] = 0x10
    si5351_write(27, 0x00)   # P1[7:0] = 0x00
    si5351_write(28, 0x00)   # P3[15:8]
    si5351_write(29, 0x01)   # P3[7:0]
    si5351_write(30, 0x00)   # P2[15:8]
    si5351_write(31, 0x00)   # P2[7:0]

def configure_clk0_75mhz():
    """Configure CLK0 to output 75MHz using PLLA at 900MHz"""
    # Divider = 900MHz / 75MHz = 12
    # P1 = 128*a + b - 512 = 128*12 + 0 - 512 = 1024 = 0x0400
    
    si5351_write(16, 0x04)   # P1[15:8] = 0x04
    si5351_write(17, 0x00)   # P1[7:0] = 0x00
    si5351_write(18, 0x00)   # P3[15:8] = 0x00
    si5351_write(19, 0x80)   # P3[7:0] = 0x80
    si5351_write(20, 0x00)   # P2[15:8] = 0x00
    si5351_write(21, 0x00)   # P2[7:0] = 0x00
    
    # Clock control register for CLK0 (register 165)
    # MS0_INT = 1 (integer mode), MS0_PLL = 0 (PLLA)
    si5351_write(165, 0x40)
    
    # Enable CLK0 output
    si5351_write(3, 0xFE)

# Main execution
if __name__ == "__main__":
    si5351_init()
    configure_clk0_75mhz()