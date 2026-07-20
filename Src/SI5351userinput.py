from machine import I2C
import math

SI5351_REGISTER_0_DEVICE_STATUS                       = 0
SI5351_REGISTER_1_INTERRUPT_STATUS_STICKY             = 1
SI5351_REGISTER_2_INTERRUPT_STATUS_MASK               = 2
SI5351_REGISTER_3_OUTPUT_ENABLE_CONTROL               = 3
SI5351_REGISTER_9_OEB_PIN_ENABLE_CONTROL              = 9
SI5351_REGISTER_15_PLL_INPUT_SOURCE                   = 15
SI5351_REGISTER_16_CLK0_CONTROL                       = 16
SI5351_REGISTER_17_CLK1_CONTROL                       = 17
SI5351_REGISTER_18_CLK2_CONTROL                       = 18
SI5351_REGISTER_19_CLK3_CONTROL                       = 19
SI5351_REGISTER_20_CLK4_CONTROL                       = 20
SI5351_REGISTER_21_CLK5_CONTROL                       = 21
SI5351_REGISTER_22_CLK6_CONTROL                       = 22
SI5351_REGISTER_23_CLK7_CONTROL                       = 23
SI5351_REGISTER_24_CLK3_0_DISABLE_STATE               = 24
SI5351_REGISTER_25_CLK7_4_DISABLE_STATE               = 25
SI5351_REGISTER_42_MULTISYNTH0_PARAMETERS_1           = 42
SI5351_REGISTER_43_MULTISYNTH0_PARAMETERS_2           = 43
SI5351_REGISTER_44_MULTISYNTH0_PARAMETERS_3           = 44
SI5351_REGISTER_45_MULTISYNTH0_PARAMETERS_4           = 45
SI5351_REGISTER_46_MULTISYNTH0_PARAMETERS_5           = 46
SI5351_REGISTER_47_MULTISYNTH0_PARAMETERS_6           = 47
SI5351_REGISTER_48_MULTISYNTH0_PARAMETERS_7           = 48
SI5351_REGISTER_49_MULTISYNTH0_PARAMETERS_8           = 49
SI5351_REGISTER_50_MULTISYNTH1_PARAMETERS_1           = 50
SI5351_REGISTER_51_MULTISYNTH1_PARAMETERS_2           = 51
SI5351_REGISTER_52_MULTISYNTH1_PARAMETERS_3           = 52
SI5351_REGISTER_53_MULTISYNTH1_PARAMETERS_4           = 53
SI5351_REGISTER_54_MULTISYNTH1_PARAMETERS_5           = 54
SI5351_REGISTER_55_MULTISYNTH1_PARAMETERS_6           = 55
SI5351_REGISTER_56_MULTISYNTH1_PARAMETERS_7           = 56
SI5351_REGISTER_57_MULTISYNTH1_PARAMETERS_8           = 57
SI5351_REGISTER_58_MULTISYNTH2_PARAMETERS_1           = 58
SI5351_REGISTER_59_MULTISYNTH2_PARAMETERS_2           = 59
SI5351_REGISTER_60_MULTISYNTH2_PARAMETERS_3           = 60
SI5351_REGISTER_61_MULTISYNTH2_PARAMETERS_4           = 61
SI5351_REGISTER_62_MULTISYNTH2_PARAMETERS_5           = 62
SI5351_REGISTER_63_MULTISYNTH2_PARAMETERS_6           = 63
SI5351_REGISTER_64_MULTISYNTH2_PARAMETERS_7           = 64
SI5351_REGISTER_65_MULTISYNTH2_PARAMETERS_8           = 65
SI5351_REGISTER_66_MULTISYNTH3_PARAMETERS_1           = 66
SI5351_REGISTER_67_MULTISYNTH3_PARAMETERS_2           = 67
SI5351_REGISTER_68_MULTISYNTH3_PARAMETERS_3           = 68
SI5351_REGISTER_69_MULTISYNTH3_PARAMETERS_4           = 69
SI5351_REGISTER_70_MULTISYNTH3_PARAMETERS_5           = 70
SI5351_REGISTER_71_MULTISYNTH3_PARAMETERS_6           = 71
SI5351_REGISTER_72_MULTISYNTH3_PARAMETERS_7           = 72
SI5351_REGISTER_73_MULTISYNTH3_PARAMETERS_8           = 73
SI5351_REGISTER_74_MULTISYNTH4_PARAMETERS_1           = 74
SI5351_REGISTER_75_MULTISYNTH4_PARAMETERS_2           = 75
SI5351_REGISTER_76_MULTISYNTH4_PARAMETERS_3           = 76
SI5351_REGISTER_77_MULTISYNTH4_PARAMETERS_4           = 77
SI5351_REGISTER_78_MULTISYNTH4_PARAMETERS_5           = 78
SI5351_REGISTER_79_MULTISYNTH4_PARAMETERS_6           = 79
SI5351_REGISTER_80_MULTISYNTH4_PARAMETERS_7           = 80
SI5351_REGISTER_81_MULTISYNTH4_PARAMETERS_8           = 81
SI5351_REGISTER_82_MULTISYNTH5_PARAMETERS_1           = 82
SI5351_REGISTER_83_MULTISYNTH5_PARAMETERS_2           = 83
SI5351_REGISTER_84_MULTISYNTH5_PARAMETERS_3           = 84
SI5351_REGISTER_85_MULTISYNTH5_PARAMETERS_4           = 85
SI5351_REGISTER_86_MULTISYNTH5_PARAMETERS_5           = 86
SI5351_REGISTER_87_MULTISYNTH5_PARAMETERS_6           = 87
SI5351_REGISTER_88_MULTISYNTH5_PARAMETERS_7           = 88
SI5351_REGISTER_89_MULTISYNTH5_PARAMETERS_8           = 89
SI5351_REGISTER_90_MULTISYNTH6_PARAMETERS             = 90
SI5351_REGISTER_91_MULTISYNTH7_PARAMETERS             = 91
SI5351_REGISTER_092_CLOCK_6_7_OUTPUT_DIVIDER          = 92
SI5351_REGISTER_165_CLK0_INITIAL_PHASE_OFFSET         = 165
SI5351_REGISTER_166_CLK1_INITIAL_PHASE_OFFSET         = 166
SI5351_REGISTER_167_CLK2_INITIAL_PHASE_OFFSET         = 167
SI5351_REGISTER_168_CLK3_INITIAL_PHASE_OFFSET         = 168
SI5351_REGISTER_169_CLK4_INITIAL_PHASE_OFFSET         = 169
SI5351_REGISTER_170_CLK5_INITIAL_PHASE_OFFSET         = 170
SI5351_REGISTER_177_PLL_RESET                         = 177
SI5351_REGISTER_183_CRYSTAL_INTERNAL_LOAD_CAPACITANCE   = 183

SI5351_CRYSTAL_FREQ_25MHZ = 25000000
SI5351_CRYSTAL_FREQ_27MHZ = 27000000
SI5351_CRYSTAL_LOAD_6PF  = 1<<6
SI5351_CRYSTAL_LOAD_8PF  = 2<<6
SI5351_CRYSTAL_LOAD_10PF = 3<<6

si5351_15to92 = bytearray(b'\x00OOo\x80\x80\x80\x80\x80\x00\x00\x00\x05\x00\x0cf\x00\x00\x02\x02q\x00\x0c\x1a\x00\x00\x86\x00\x01\x00\x01\x00\x00\x00\x00\x00\x01\x00\x1c\x00\x00\x00\x00\x00\x01\x00\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

SI5351_MULTISYNTH_DIV_4  = 4
SI5351_MULTISYNTH_DIV_6  = 6
SI5351_MULTISYNTH_DIV_8  = 8

class SI5351:
    def __init__( self, i2c, address=0x60, crystalFreq=25000000):
        self.i2c = i2c
        self.address = address
        
        self.initialized     = False
        self.crystalFreq     = crystalFreq
        self.crystalLoad     = SI5351_CRYSTAL_LOAD_10PF
        self.crystalPPM      = 30
        self.plla_configured = False
        self.plla_freq       = 0
        self.pllb_configured = False
        self.pllb_freq       = 0
        return

    def write8( self, register, value):
        buffera = bytearray(1)
        buffera[0] = value & 0xff
        self.i2c.writeto_mem(  self.address, register, buffera)
        return

    def read8( self, register, value):
        buffera = bytearray(1)
        self.i2c.readfrom_mem_into(  self.address, register, buffera)
        return


    def begin( self):
        self.write8( SI5351_REGISTER_3_OUTPUT_ENABLE_CONTROL, 0xFF)
        # Power down all output drivers */
        self.write8(SI5351_REGISTER_16_CLK0_CONTROL, 0x80)
        self.write8(SI5351_REGISTER_17_CLK1_CONTROL, 0x80)
        self.write8(SI5351_REGISTER_18_CLK2_CONTROL, 0x80)
        self.write8(SI5351_REGISTER_19_CLK3_CONTROL, 0x80)
        self.write8(SI5351_REGISTER_20_CLK4_CONTROL, 0x80)
        self.write8(SI5351_REGISTER_21_CLK5_CONTROL, 0x80)
        self.write8(SI5351_REGISTER_22_CLK6_CONTROL, 0x80)
        self.write8(SI5351_REGISTER_23_CLK7_CONTROL, 0x80)

        #  Set the load capacitance for the XTAL */
        self.write8(SI5351_REGISTER_183_CRYSTAL_INTERNAL_LOAD_CAPACITANCE,
                       self.crystalLoad)

        # Set interrupt masks as required (see Register 2 description in AN619).
        # By default, ClockBuilder Desktop sets this register to 0x18.
        # Note that the least significant nibble must remain 0x8, but the most
        # significant nibble may be modified to suit your needs. 

        # Reset the PLL config fields just in case we call init again
        self.plla_configured = False
        self.plla_freq = 0
        self.pllb_configured = False
        self.pllb_freq = 0

        # All done!
        self.initialized = True

        return

    def setClockBuilderData(self ):
        i = 0

        # Make sure we've called init first

        assert self.initialized == True, "you have not initialized the object"

        # Disable all outputs setting CLKx_DIS high
        self.write8( SI5351_REGISTER_3_OUTPUT_ENABLE_CONTROL, 0xFF)

        # Writes configuration data to device using the register map contents
        # generated by ClockBuilder Desktop (registers 15-92 + 149-170)
        for i, x in enumerate( range(15,93)): 
            #print( x,  si5351_15to92[i] )
            self.write8( x, si5351_15to92[i] )

        for i in range(149, 171):
            self.write8( i, 0x00) 

        # Apply soft reset
        self.write8(SI5351_REGISTER_177_PLL_RESET, 0xAC)

        # Enabled desired outputs (see Register 3)
        self.write8(SI5351_REGISTER_3_OUTPUT_ENABLE_CONTROL, 0x00)
        return None

    def setupPLL( self, mult, num, denom, pllsource = 'A'):
        assert self.initialized == True, "you have not initialized the object"
        assert ( (mult > 14) and (mult < 91) ), "invalid mult parameter"
        assert denom > 0, "denom must be > 0"
        assert num <= 0xfffff, "invalid parameter num"
        assert denom <= 0xfffff, "invalid parameter denom"
        if num ==0:
            P1 = 128*mult -512
            P2 = num
            P3 = denom
        else:
            P1 = 128*mult + math.floor( 128 * num/denom ) -512
            P2 = 128*num - denom * math.floor( 128 * num/denom)
            P3 = denom 

        if pllsource == 'A':
            baseaddr = 26
        else:
            baseaddr = 34

        self.write8( baseaddr,   (P3 & 0x0000FF00) >> 8)
        self.write8( baseaddr+1, (P3 & 0x000000FF))
        self.write8( baseaddr+2, (P1 & 0x00030000) >> 16)
        self.write8( baseaddr+3, (P1 & 0x0000FF00) >> 8)
        self.write8( baseaddr+4, (P1 & 0x000000FF))
        self.write8( baseaddr+5, ((P3 & 0x000F0000) >> 12) | ((P2 & 0x000F0000) >> 16) )
        self.write8( baseaddr+6, (P2 & 0x0000FF00) >> 8)
        self.write8( baseaddr+7, (P2 & 0x000000FF))

        self.write8(SI5351_REGISTER_177_PLL_RESET, (1<<7) | (1<<5) )
        if pllsource =='A':
            fvco = self.crystalFreq*( mult + num/denom)
            self.plla_configured = True
            self.plla_freq = int(math.floor( fvco))
        else:
            fvco = self.crystalFreq*(mult + num/denom)
            self.pllb_configured = True
            self.pllb_freq = int(math.floor(fvco))
        return None

    def setupRdiv( self, output, div):
        assert output in [0,1,2], "output value invalid"
        assert div in [1,2,4,8,16,32,64,128], "div invalid"
        divdict = {1: 0, 2: 1, 4: 2, 8: 3, 16: 4, 32: 5, 64: 6, 128: 7}
        registers = [ 44, 52, 60]
        Rreg = registers[output]
        buf = bytearray( 1)

        self.read8(Rreg, buf)

        regval = buf[0] & 0x0F
        divider = divdict[div]
        divider &= 0x07
        divider <<= 4
        regval |= divider
        self.write8(Rreg, regval)

        return None

    def setupMultisynth( self, output, div, num, denom, pllsource="A", phase_delay=0, inverted=0, powerdown=0):
        assert self.initialized  == True, "device not initialized"
        assert output in [0,1,2], "output out of range"
        assert div > 3, "div out of range"
        assert denom >0, "denom out of range"
        assert num <= 0xfffff, "num has a 20-bit limit"
        assert denom <= 0xfffff, "denom as a 20-bit limit"
        if pllsource=="A":
            assert self.plla_configured == True, "plla has not been configured"
        else:
            assert self.pllb_configured == True, 'pllb has not been configured'

         # Output Multisynth Divider Equations
         # where: a = div, b = num and c = denom
         #
         #  P1 register is an 18-bit value using following formula:
         #
         # P1[17:0] = 128 * a + floor(128*(b/c)) - 512
         #
         # P2 register is a 20-bit value using the following formula:
         #
         #  P2[19:0] = 128 * b - c * floor(128*(b/c))
         #
         # P3 register is a 20-bit value using the following formula:
         #
         # P3[19:0] = c

        if num==0 and phase_delay == 0.0:
            # integer mode
            P1 = 128 *div -512
            P2 = num
            P3 = denom
        else:
            # Fractional mode */
            P1 = int( 128 * div + math.floor(128 * (num/denom)) - 512 )
            P2 = int( 128 * num - denom * math.floor(128 * (num/denom)))
            P3 = denom


        baseaddrs = [ 42, 50, 58]
        baseaddr = baseaddrs[output]

        self.write8( baseaddr,  (P3 & 0x0000FF00) >> 8)
        self.write8( baseaddr+1, (P3 & 0x000000FF))
        self.write8( baseaddr+2, (P1 & 0x00030000) >> 16)	# ToDo: Add DIVBY4 (>150MHz) and R0 support (<500kHz) later */
        self.write8( baseaddr+3, (P1 & 0x0000FF00) >> 8)
        self.write8( baseaddr+4, (P1 & 0x000000FF))
        self.write8( baseaddr+5, ((P3 & 0x000F0000) >> 12) | ((P2 & 0x000F0000) >> 16) )
        self.write8( baseaddr+6, (P2 & 0x0000FF00) >> 8)
        self.write8( baseaddr+7, (P2 & 0x000000FF))
        
        if phase_delay != 0.0:
            assert phase_delay > 0 and phase_delay <= 1.0, "Invalid phase delay, must be in [0,1]"
            ph_delay_reg = SI5351_REGISTER_165_CLK0_INITIAL_PHASE_OFFSET + output
            delay = int(phase_delay * (div + num/denom))
            assert delay < 128, "Phase delay too large for selected PLL divisor"
            self.write8(ph_delay_reg, delay)
            

         # Configure the clk control and enable the output 
        clkControlReg = 0x0F                             # 8mA drive strength, MS0 as CLK0 source, Clock not inverted, powered up 
        if pllsource == 'B':
            clkControlReg |= (1 << 5) # /* Uses PLLB */
        if num == 0:
            clkControlReg |= (1 << 6) #  Integer mode */
        if inverted == 1:
            clkControlReg |= (1 << 4) #  Inverted clock */
        if powerdown == 1:
            clkControlReg |= (1 << 7) #  Powerdown driver */
            
        if output == 0: 
            self.write8(SI5351_REGISTER_16_CLK0_CONTROL, clkControlReg)
        if output == 1:
            self.write8(SI5351_REGISTER_17_CLK1_CONTROL, clkControlReg)
        if output == 2:
            self.write8(SI5351_REGISTER_18_CLK2_CONTROL, clkControlReg)


    def enableOutputs( self, enabled=True):
        assert self.initialized == True, "Error Device not initialized"
        if enabled:
            self.write8( SI5351_REGISTER_3_OUTPUT_ENABLE_CONTROL, 0x00)
        else:
            self.write8( SI5351_REGISTER_3_OUTPUT_ENABLE_CONTROL, 0xff)

        return 

    
    def PLLsoftreset(self):
        # soft-reset the PLLs (must be done after all configuration of clocks is complete
        self.write8(SI5351_REGISTER_177_PLL_RESET, (1 << 7) | (1 << 5))

    
    def configureOutputs( self, mask=0x00):
        assert self.initialized == True, "Error Device not initialized"
        self.write8( SI5351_REGISTER_3_OUTPUT_ENABLE_CONTROL, mask ^ 0xFF)
        
        return

    def set_frequency(self, output, freq_mhz):
        """Set frequency for a specific output (0, 1, or 2)
        Args:
            output: 0, 1, or 2
            freq_mhz: Frequency in MHz (float or int)
        Returns:
            bool: True if successful, False otherwise
        """
        # Define frequency limits
        MIN_FREQ_MHZ = 50.0
        MAX_FREQ_MHZ = 120.0
        
        # Check if frequency is within valid range (50 MHz <= freq <= 120 MHz)
        if freq_mhz < MIN_FREQ_MHZ:
            print(f" Error: Frequency {freq_mhz:.3f} MHz is too low")
            print(f"   Frequency must be ≥ {MIN_FREQ_MHZ:.1f} MHz")
            return False
        elif freq_mhz > MAX_FREQ_MHZ:
            print(f" Error: Frequency {freq_mhz:.3f} MHz is too high")
            print(f"   Frequency must be ≤ {MAX_FREQ_MHZ:.1f} MHz")
            return False
        
        # Convert MHz to Hz for calculations
        freq_hz = int(freq_mhz * 1000000)
        
        # PLL frequency range: 600-900 MHz
        # Use 800 MHz as a good mid-range value
        pll_freq = 800000000  # 800 MHz in Hz
        
        # Calculate the divider needed
        divider = pll_freq / freq_hz
        
        # Divider must be between 4 and 900
        if divider < 4 or divider > 900:
            print(f" Error: Frequency {freq_mhz:.3f} MHz cannot be generated")
            print(f"   Divider {divider:.2f} is outside valid range (4-900)")
            return False
        
        # Integer and fractional parts
        div = int(divider)
        frac = divider - div
        
        # Calculate numerator and denominator for fractional mode
        # Use denominator of 1048575 (max 20-bit value) for best precision
        denom = 1048575
        num = int(frac * denom)
        
        # Setup PLL if not already configured
        if not self.plla_configured:
            # Configure PLLA for 800 MHz
            pll_mult = 32  # 800 MHz / 25 MHz = 32
            self.setupPLL(pll_mult, 0, 1, 'A')
        
        # Setup multisynth divider
        self.setupMultisynth(output, div, num, denom, 'A')
        
        # Enable the output
        self.enableOutputs(True)
        
        print(f"✓ Output {output} set to {freq_mhz:.3f} MHz ({freq_hz:,} Hz)")
        print(f"  PLL: {pll_freq/1000000:.0f} MHz, Divider: {divider:.3f}")
        print(f"  Integer: {div}, Fraction: {frac:.3f}")
        return True

    def get_frequency_from_user(self):
        """Get frequency input from user in MHz"""
        print("\n" + "="*50)
        print("        SI5351 Frequency Generator")
        print("="*50)
        print("Valid frequency range: 50.0 MHz to 120.0 MHz")
        print("(50 MHz ≤ frequency ≤ 120 MHz)")
        print("Available outputs: 0, 1, 2")
        print("-"*50)
        
        # Get output number
        while True:
            try:
                output_str = input("Select output (0, 1, or 2): ")
                output = int(output_str)
                if output in [0, 1, 2]:
                    break
                else:
                    print("Please enter 0, 1, or 2")
            except ValueError:
                print("Please enter a valid number")
        
        # Get frequency in MHz
        print("\nEnter frequency in MHz (e.g., 100 for 100 MHz)")
        print("You can use decimals (e.g., 75.5 for 75.5 MHz)")
        
        while True:
            try:
                freq_str = input("Frequency (MHz): ")
                freq_mhz = float(freq_str)
                
                # Check if frequency is within valid range (50 <= freq <= 120)
                MIN_FREQ_MHZ = 50.0
                MAX_FREQ_MHZ = 120.0
                
                if freq_mhz < MIN_FREQ_MHZ:
                    print(f" Frequency {freq_mhz:.3f} MHz is too low")
                    print(f"   Frequency must be ≥ {MIN_FREQ_MHZ:.1f} MHz")
                    print(f"   Please enter a value between {MIN_FREQ_MHZ:.1f} and {MAX_FREQ_MHZ:.1f} MHz")
                    continue
                elif freq_mhz > MAX_FREQ_MHZ:
                    print(f" Frequency {freq_mhz:.3f} MHz is too high")
                    print(f"   Frequency must be ≤ {MAX_FREQ_MHZ:.1f} MHz")
                    print(f"   Please enter a value between {MIN_FREQ_MHZ:.1f} and {MAX_FREQ_MHZ:.1f} MHz")
                    continue
                else:
                    # Frequency is within valid range
                    break
            except ValueError:
                print(" Please enter a valid number (e.g., 100 or 75.5)")
        
        print("-"*50)
        print(f"Output: {output}, Frequency: {freq_mhz:.3f} MHz")
        print(f"Range check: {MIN_FREQ_MHZ:.1f} MHz ≤ {freq_mhz:.3f} MHz ≤ {MAX_FREQ_MHZ:.1f} MHz ✓")
        print("-"*50)
        
        # Set the frequency
        return self.set_frequency(output, freq_mhz)

# Example usage
if __name__ == "__main__":
    # Initialize I2C
    # Adjust pins as needed for your microcontroller
    # For Raspberry Pi Pico: scl=22, sda=21
    # For ESP32: scl=22, sda=21
    # For other boards, adjust accordingly
    i2c = I2C(0, scl=5, sda=4, freq=100000)
    
    # Create SI5351 object
    si = SI5351(i2c)
    
    # Initialize the chip
    si.begin()
    
    print("\n✓ SI5351 initialized successfully")
    print(f"  Crystal frequency: {si.crystalFreq/1000000:.1f} MHz")
    
    # Show example inputs
    print("\n Example inputs (50 MHz to 120 MHz):")
    print("   50   - for 50.0 MHz (minimum)")
    print("   75.5 - for 75.5 MHz")
    print("   100  - for 100.0 MHz")
    print("   120  - for 120.0 MHz (maximum)")
    
    # Get frequency from user
    while True:
        success = si.get_frequency_from_user()
        
        if success:
            print("\n Frequency set successfully!")
        else:
            print("\n Failed to set frequency")
        
        # Ask if user wants to set another frequency
        again = input("\nSet another frequency? (y/n): ").lower()
        if again != 'y':
            break
    
    print("\n" + "="*50)
    print("Program ended. Goodbye!")
    print("="*50)
