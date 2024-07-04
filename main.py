import pyvisa

# Define the VISA resource string for the Agilent 34411A multimeter
# The resource string format may vary depending on your system and connection method (e.g., USB, LAN)
# Example resource string for USB connection:
resource_str = "USB0::0x0957::0x0618::MY51141218::0::INSTR"

# Initialize PyVISA's ResourceManager
rm = pyvisa.ResourceManager()

try:
    # Open a connection to the instrument
    with rm.open_resource(resource_str) as inst:
        # Query the instrument's identification information
        idn = inst.query("*IDN?")
        print(f"Connected to: {idn.strip()}")

        # Example: Set the measurement function to DC voltage
        inst.write("CONF:VOLT:DC")
        
        # Example: Initiate a single measurement and read the result
        inst.write("INIT")
        result = inst.query("FETCH?")
        print(f"Measurement result: {result.strip()}")

except pyvisa.Error as e:
    print(f"PyVISA error: {e}")

finally:
    # Close the connection
    rm.close()
