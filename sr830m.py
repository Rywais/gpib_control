import visa, pyvisa, gpib
import time

class Sr830m:
    
    #Notes:
    # - It seems no delay is necessary on consecutive write or query commands.

    QUERY_DELAY = 0.06

    SERIAL_BIT_NO_SCAN = 1 << 0
    SERIAL_BIT_NO_COMMAND = 1 << 1
    SERIAL_BIT_ERROR_BIT = 1 << 2
    SERIAL_BIT_LIA_BIT = 1 << 3
    SERIAL_BIT_MESSAGE_AVAILABLE = 1 << 4
    SERIAL_BIT_STANDARD_BIT = 1 << 5
    SERIAL_BIT_SERVICE_REQUEST = 1 << 6

    STANDARD_BIT_INPUT_OVERFLOW = 1 << 0
    STANDARD_BIT_OUTPUT_OVERFLOW = 1 << 2
    STANDARD_BIT_CANNOT_EXECUTE = 1 << 4
    STANDARD_BIT_ILLEGAL_COMMAND = 1 << 5
    STANDARD_BIT_KEY_PRESS = 1 << 6
    STANDARD_BIT_POWER_ON = 1 << 7

    LIA_BIT_INPUT_AMP_OVERLOAD = 1 << 0
    LIA_BIT_TIME_CONST_OVERLOAD = 1 << 1
    LIA_BIT_OUTPT_OVERLOAD = 1 << 2
    LIA_BIT_REFERNCE_INLOCK = 1 << 3
    LIA_BIT_RANGE_CHANGE = 1 << 4
    LIA_BIT__TIME_CONST_CHANGE = 1 << 5
    LIA_BIT_DATA_STORAGE_TRIGGER = 1 << 6

    ERROR_BIT_BATTERY_FAIL = 1 << 1
    ERROR_BIT_RAM_FAIL = 1 << 2
    ERROR_BIT_ROM_FAIL = 1 << 4
    ERROR_BIT_GPIB_FAST_FAIL = 1 << 5
    ERROR_BIT_DSP_FAIL = 1 << 6
    ERROR_BIT_MATH_FAIL = 1 << 7
    
    def __init__(self):
        self.address = ''
        self.rm = ''
        self.comm = gpib.Gpib_communicator()

    #Basic communications functions/initialization
    def set_address(self, address):
        self.comm.set_address(address)

    def get_address(self):
        return self.comm.get_address()

    def read_stb(self):
        return self.comm.read_stb()

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

    #Data Storage Commands
    def get_data_sample_rate(self):
        return self.comm.query('SRAT?\n', delay=self.QUERY_DELAY)

    def set_data_sample_rate(self, sample_rate_index):
        self.comm.write('SRAT'+str(sample_rate_index)+'\n')

    def get_end_of_buf_mode(self):
        return self.comm.query('SEND?\n',delay=self.QUERY_DELAY)

    def set_end_of_buf_mode(self, shot_loop):
        self.comm.write('SEND'+str(shot_loop)+'\n')

    def software_trigger(self):
        self.comm.write('TRIG\n')

    def get_trigger_start_mode(self):
        return self.comm.query('TSTR?\n', delay=self.QUERY_DELAY)

    def set_trigger_start_mode(self, off_on):
        self.comm.write('TSTR'+str(off_on)+'\n')

    def start_data_storage(self):
        self.comm.write('STRT\n')

    def pause_data_storage(self):
        self.comm.write('PAUS\n')

    def reset_data_buffer(self):
        self.comm.write('REST\n')

    #Data Transfer Commands
    def read_xyrtheta(self, x_y_r_theta):
        return self.comm.query('OUTP?'+str(x_y_r_theta)+'\n', delay=self.QUERY_DELAY)

    def read_display(self, ch1_ch2):
        return self.comm.query('OUTR?'+str(ch1_ch2)+'\n',delay=self.QUERY_DELAY)

    def snap(self, param_array):
        cmnd = 'SNAP?'+str(param_array[0])+','+str(param_array[1])
        for i in range(2,max(len(param_array),6)):
            cmnd = cmnd+','+str(param_array[i])
        cmnd = cmnd+'\n'
        return self.comm.query(cmnd, delay=self.QUERY_DELAY)

    def read_aux(self, aux_index):
        return self.comm.query('OAUX?'+str(aux_index)+'\n',delay=self.QUERY_DELAY)

    def get_data_points_count(self):
        return self.comm.query('SPTS?\n',delay=self.QUERY_DELAY)

    def get_buffer_values_ascii(self, channel_index, start_bin, bin_count):
        cmnd = 'TRCA?'+str(channel_index)
        cmnd = cmnd+','+str(start_bin)
        cmnd = cmnd+','+str(bin_count)+'\n'
        return self.comm.query(cmnd,delay=self.QUERY_DELAY)

    def get_buffer_values_ieee(self, channel_index, start_bin, bin_count):
        cmnd = 'TRCB?'+str(channel_index)
        cmnd = cmnd+','+str(start_bin)
        cmnd = cmnd+','+str(bin_count)+'\n'
        return self.comm.query(cmnd,delay=self.QUERY_DELAY)

    def get_buffer_values_float(self, channel_index, start_bin, bin_count):
        cmnd = 'TRCL?'+str(channel_index)
        cmnd = cmnd+','+str(start_bin)
        cmnd = cmnd+','+str(bin_count)+'\n'
        return self.comm.query(cmnd,delay=self.QUERY_DELAY)

    def get_data_transfer_mode(self):
        return self.comm.query('FAST?\n',delay=self.QUERY_DELAY)

    def set_data_transfer_mode(self, off_dos_windows):
        self.comm.write('FAST'+str(off_dos_windows)+'\n')

    def start_fast_scan(self):
        self.comm.write('STRD\n')

    #Interface Commands
    def reset_config(self):
        self.comm.write('*RST\n')

    def get_identity(self):
        return self.comm.write('*IDN?\n')

    def get_local_function(self):
        return self.comm.query('LOCL?\n')

    def set_local_function(self, local_remote):
        self.comm.write('LOCL'+str(local_remote)+'\n')

    def get_gpib_override(self):
        return self.comm.query('OVRM?\n',delay=self.QUERY_DELAY)

    def set_gpib_override(self, no_yes):
        self.comm.write('OVRM'+str(no_yes)+'\n')

    #Status Reporting Commands
    def clear_status_registers(self):
        self.comm.write('*CLS\n')

    def get_standard_event_enable_decimal(self):
        return self.comm.query('ESE?\n',delay=self.QUERY_DELAY)

    def get_standard_event_enable_binary(self, index):
        return self.comm.query('ESE?'+str(index)+'\n',delay=self.QUERY_DELAY)

    def set_standard_event_enable_decimal(self, val):
        self.comm.write('ESE'+str(val)+'\n')

    def set_standard_event_enable_binary(self, index, low_high):
        cmnd = 'ESE'+str(index)+','+str(low_high)+'\n'
        self.comm.write(cmnd)

    def get_standard_event_status_decimal(self):
        return self.comm.query('ESR?', delay=self.QUERY_DELAY)

    def get_standard_event_status_binary(self, index):
        cmnd = 'ESR'+str(index)+'\n'
        return self.comm.query(cmnd,delay=self.QUERY_DELAY)

    def set_standard_event_status_decimal(self, val):
        self.comm.write('ESR'+str(val)+'\n')

    def get_serial_poll_decimal(self):
        return self.comm.query('*STB?\n',delay=self.QUERY_DELAY)

    def get_serial_poll_binary(self, index):
        return self.comm.query('*STB?'+str(index)+'\n', delay=self.QUERY_DELAY)

    def get_power_on_status_clear(self):
        return self.comm.query('*PSC?\n',delay=self.comm.QUERY_DELAY)

    def set_power_on_status_clear(self, bit):
        self.comm.write('*PSC'+str(bit)+'\n')

    def get_error_status_enable_decimal(self):
        return self.comm.query('ERRE?\n',delay=self.QUERY_DELAY)

    def get_error_status_enable_binary(self, index):
        return self.comm.query('ERRE?'+str(index)+'\n',delay=self.QUERY_DELAY)

    def set_error_status_enable_decimal(self, val):
        self.comm.write('ERRE'+str(val)+'\n')

    def set_error_status_enable_binary(self,bit_index, low_high):
        self.comm.write('ERRE'+str(bit_index)+','+str(low_high)+'\n')

    def get_error_status_decimal(self):
        return self.comm.query('ERRS?\n',delay=self.QUERY_DELAY)

    def get_error_status_binary(self, bit_index):
        return self.comm.query('ERRS?'+str(bit_index)+'\n',delay=self.QUERY_DELAY)

    def get_lockin_status_enable_decimal(self):
        return self.comm.query('LIAE?\n',delay=self.QUERY_DELAY)

    def get_lockin_status_enable_binary(self, bit_index):
        return self.comm.query('LIAE?'+str(bit_index)+'\n',delay=self.QUERY_DELAY)

    def set_lockin_status_enable_decimal(self, val):
        self.comm.write('LIAE'+str(val)+'\n')

    def set_lockin_status_enable_binary(self, bit_index, low_high):
        self.comm.write('LIAE'+str(bit_index)+','+str(low_high)+'\n')

    def get_lockin_status_decimal(self):
        return self.comm.query('LIAS?\n',delay=self.QUERY_DELAY)

    def get_lockin_status_binary(self,bit_index):
        cmnd = 'LIAS?'+str(bit_index)+'\n'
        return self.comm.query(cmnd,delay=self.QUERY_DELAY)


