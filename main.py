import sys
sys.path.append("C:\\Users\\scy4\\AppData\\Local\\Packages")
import pyvisa

resource_str = "USB0::2391::2567::MY48005948::INSTR"


rm = pyvisa.ResourceManager()

def dc_volt(times):
    results = []
    for i in range(times):
        try:
            with rm.open_resource(resource_str) as inst:
                idn = inst.query("*IDN?")
                inst.write("CONF:VOLT:DC")
                
                inst.write("INIT")
                result = inst.query("FETCH?")
                results.append(float(result.strip()))

        except pyvisa.Error as e:
            print(f"PyVISA error: {e}")
    return results
def ac_volt(times):
    results = []
    for i in range(times):
        try:
            with rm.open_resource(resource_str) as inst:
                idn = inst.query("*IDN?")

                inst.write("CONF:VOLT:AC")
                
                inst.write("INIT")
                result = inst.query("FETCH?")
                results.append(float(result.strip()))

        except pyvisa.Error as e:
            print(f"PyVISA error: {e}")
    return results
