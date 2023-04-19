from serial import Serial
import os
import datetime
import csv

CH_1 = "COM6"
CH_2 = "COM11"

BAUD = 115200
TIMEOUT = 1

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

try:
    dev_ch1 = Serial(CH_1, BAUD, timeout=TIMEOUT)
except:
    raise ConnectionError("Failed to connect to serial device.")

try:
    dev_ch2 = Serial(CH_2, BAUD, timeout=TIMEOUT)
except:
    raise ConnectionError("Failed to connect to serial device.")

time = 0

filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.csv'
filepath = os.path.join(DATA_DIR, filename)

with open(filepath, mode='w', newline='') as file:
    writer = csv.writer(file)
    print('Time', 'Channel 1 Value', 'Channel 2 Value')
    writer.writerow(['Time', 'Channel 1 Value', 'Channel 2 Value'])

    time = 0
    while True:
        try:
            ch1_val = dev_ch1.readline().decode()
            ch2_val = dev_ch2.readline().decode()
        except:
            print("Serial device not responding.")
            break
        
        try:
            ch1_pval = float(ch1_val.split(':')[1])*-1.0
            ch2_pval = float(ch2_val.split(':')[1])*-1.0
        except:
            print(f"Serial device sending unexpected data: {CH_1}:{ch1_val}, {CH_2}:{ch2_val}")
            pass
        
        print(f"{time:.1f}, {ch1_pval}, {ch2_pval}")
        writer.writerow([round(time, 2), ch1_pval, ch2_pval])
        # print(f"{time}, {ch2_pval}")
        # writer.writerow([time, ch2_pval])

        time += 1

dev_ch1.close()
dev_ch2.close()

    
