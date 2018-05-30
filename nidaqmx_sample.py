AI_VOLTAGE_CHANNEL = 'Dev1/ai15'

import nidaqmx

task = nidaqmx.Task()
task.ai_channels.add_ai_voltage_chan(AI_VOLTAGE_CHANNEL)

try:
    while True:
        print(task.read())

except KeyboardInterrupt:
    print('Done reading!')

exit()
