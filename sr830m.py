import visa, pyvisa, gpib
import time

class Sr830m:
    
    #Notes:
    # - It seems no delay is necessary on consecutive write or query commands.

    QUERY_DELAY = 0.06
    
    def __init__(self):
        self.address = ''
        self.rm = ''
        self.comm = gpib.Gpib_communicator()

    #Basic communications functions/initialization
    def set_address(self, address):
        self.comm.set_address(address)

    def get_address(self):
        return self.comm.get_address()

    #Reference/Phase Commands:
    def get_phase_shift(self):
        return self.comm.query('PHAS?\n', delay = self.QUERY_DELAY)

    def set_phase_shift(self, ps):
        self.comm.write('PHAS' + str(ps) + '\n' )

    def get_ref_src(self):
        return self.comm.query('FMOD?\n', delay=self.QUERY_DELAY)

    #ext_or_int is 0 for external source or 1 for internal
    def set_ref_src(self, ext_or_int):
        self.comm.write('FMOD' + str(ext_or_int) + '\n' )

    def get_ref_freq(self):
        return self.comm.query('FREQ\n', delay=self.QUERY_DELAY)

    def set_ref_freq(self, freq):
        self.comm.write('FREQ'+str(freq)+'\n')

    def get_ref_trig(self):
        self.comm.query('RSLP?\n', delay=self.QUERY_DELAY)

    def set_ref_trig(self, sinezero_rise_fall):
        self.comm.write('RSLP'+str(sinezero_rise_fall)+'\n')

    def get_harmonic(self):
        return self.comm.query('HARM?\n', delay=self.QUERY_DELAY)

    def set_harmonic(self, harmonic_n):
        self.comm.write('HARM'+str(harmonic_n)+'\n')

    def get_sine_output(self):
        return self.comm.query('SLVL?\n', delay=self.QUERY_DELAY)

    #Input and Filter Commands
    def get_input_config(self):
        return self.comm.query('ISRC?\n',delay=self.QUERY_DELAY)

    def set_input_config(self, config):
        self.comm.write('ISRC'+str(config)+'\n')

    def get_input_shield(self):
        return self.comm.query('IGND?\n',delay=self.QUERY_DELAY)

    def set_input_shield(self, float_gnd):
        self.comm.write('IGND'+str(float_gnd)+'\n')

    def get_input_coupling(self):
        return self.comm.query('ICPL?\n', delay=self.QUERY_DELAY)

    def set_input_coupling(self, ac_dc):
        self.comm.write('ICPL'+str(ac_dc)+'\n')

    def get_input_notch(self):
        return self.comm.query('ILIN?\n', delay=self.QUERY_DELAY)

    def set_input_notch(self, notch):
        self.comm.write('ILIN'+str(notch)+'\n')

    #Gain and Time Constant Commands
    def get_sensitivity(self):
        return self.comm.query('SENS?\n', delay=self.QUERY_DELAY)

    def set_sensitivity(self, sensitivity):
        self.comm.write('SENS'+str(sensitivity)+'\n')

    def get_reserve_mode(self):
        return self.comm.query('RMOD?\n', delay=self.QUERY_DELAY)

    def set_reserve_mode(self, reserve_mode):
        self.comm.write('RMOD'+str(reserve_mode)+'\n')

    def get_time_const(self):
        return self.comm.query('OFLT?\n', delay=self.QUERY_DELAY)

    def set_time_const(self, time_const):
        self.comm.write('OFLT'+str(time_const)+'\n')

    def get_lpf_slope(self):
        return self.comm.query('OFSL?\n', delay=self.QUERY_DELAY)

    def set_lpf_slope(self, lpf_slope):
        self.comm.write('OFSL'+str(lpf_slope)+'\n')

    def get_sync_filter_status(self):
        return self.comm.query('SYNC?\n', delay=self.QUERY_DELAY)

    def set_sync_filter_status(self, sync_filter_status):
        self.comm.write('SYNC'+str(sync_filter_status)+'\n')

    #Aux input and Output Commands
    def get_aux_input(self, aux_index):
        i = aux_index
        return self.comm.query('OAUX?'+str(i)+'\n', delay=self.QUERY_DELAY)

    def get_aux_output(self, aux_index):
        i = aux_index
        return self.comm.query('AUXV?'+str(i)+'\n',delay=self.QUERY_DELAY)

    def set_aux_output(self, aux_index, voltage):
        self.comm.write('AUXV'+str(aux_index)+','+str(voltage)+'\n')

    #Remote Programming Commands
    def set_gpib(self):
        self.comm.write('OUTX1\n')

    def get_is_gpib(self):
        cond = self.comm.query('OUTX?\n',delay=QUERY_DELAY)
        return int(cond) == 1

    def disable_lockout(self):
        self.comm.write('OVRM1\n')

    def enable_lockout(self):
        self.comm.write('OVRM0\n')

    def get_key_click(self):
        return self.comm.query('KCLK?\n',delay=self.QUERY_DELAY)

    def set_key_click(self, on_off):
        self.comm.write('KCLK'+str(on_off)+'\n')

    def get_alarm(self):
        return self.comm.query('ALRM?\n',delay=self.QUERY_ALARM)

    def set_alarm(self, on_off):
        self.comm.write('ALRM'+str(on_off)+'\n')

    def save_setup(self, save_index):
        self.comm.write('SSET'+str(save_index)+'\n')
    
    def load_setup(self, save_index):
        self.comm.write('RSET'+str(save_index)+'\n')

    #Auto Functions
    def auto_gain(self):
        self.comm.write('AGAN\n')

    def auto_reserve(self):
        self.comm.write('ARSV\n')

    def auto_phase(self):
        self.comm.write('APHS\n')
    
    #Note 1=X, 2=Y, 3=R
    def auto_offset(self, x_y_r):
        self.comm.write('AOFF'+str(x_y_r)+'\n')

    #Auto Storage Commands
