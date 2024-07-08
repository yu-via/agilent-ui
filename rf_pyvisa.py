import pyvisa
resource = 'USB0::2391::16648::DE47C00628::INSTR'
def set_dc(rf):
    rm = pyvisa.ResourceManager()
    inst = rm.open_resource(resource)
    inst.write("FUNC:SHAP SIN")
    inst.write("FM:STAT OFF")
    inst.write("OUTP:STAT ON")
    inst.write(f"FREQ {rf}")
    inst.close()
def set_ac(dev,fm):
    rm = pyvisa.ResourceManager()
    inst = rm.open_resource(resource)
    inst.write("FUNC:SHAP SIN")
    inst.write("FM:STAT ON")
    inst.write("OUTP:STAT ON")
    inst.write(f"FM:DEV {dev}")
    inst.write(f"FM:INT:FREQ {fm}")
    inst.close()
def set_off():
    rm = pyvisa.ResourceManager()
    inst = rm.open_resource(resource)
    inst.close()

