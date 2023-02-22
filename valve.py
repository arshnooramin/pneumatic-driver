class Valve:
    """
    couples hardware valves to ui buttons
    """
    STATE0_OFFSET = 5                       # serial message offset to set state (0)

    def __init__(self, bin_val, state, serial_device):
        self.bin_val = bin_val              # binary value of the valve
        self.state = state                  # state of the valve (0 or 1)
        self.serial_device = serial_device  # serial object for controller device

        self.update()
    
    def update(self):
        """
        sends a serial message to update the physical valve state
        """
        if self.state.get() == 1:
            oval = bytes(str(self.bin_val + 1), 'utf-8')
        elif self.state.get() == 0:
            oval = bytes(str(self.bin_val + 1 + Valve.STATE0_OFFSET), 'utf-8')
        else:
            raise ValueError("Unexpected valve state.")
        try:
            self.serial_device.write(oval)
        except:
            raise ConnectionError("Failed to update valve value.")