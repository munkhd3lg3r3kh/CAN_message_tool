from __future__ import print_function
from PCANBasic import *
import random
import time
import datetime

cols = ["No", "Time_Offset", "Type", "ID", "Data_Length", 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight']
x = datetime.datetime.now()
x = "Dataset\\Replay Attack Injected Datas " + str(x).split()[0] + ".txt"
f = open(x, "a")

# all_data = "No\tID\tTYPE\tLEN\tONE\tTWO\tTHREE\tFOUR\tFIVE\tSIX\tSEVEN\tEIGHT\n"
all_data = ""
for col in cols:
    all_data += col + "\t"

print(all_data)
f.write(all_data)
def update_progress(progress):
    print("\r progress [{0}] {1}%".format('#'*(progress//10), progress), end='')
    

if __name__ == "__main__":
    CAN = PCANBasic()                            #CANi
    CAN_BUS = PCAN_USBBUS3
    result = CAN.Initialize(CAN_BUS, PCAN_BAUD_500K, 2047, 0, 0) #Channel, Btr, HwType, IOPort, INterrupt
    counter = 0
    start_time = time.time()
    ind = 0
    while True:

        if result != PCAN_ERROR_OK:
            # An error occurred, get a text describing the error and show it
            #
            print("oh No")
            CAN.GetErrorText(result)
            print(result)
            break
        else:
            # print("PCAN-USB Pro FD (Ch-1) was initialized")
            mess = CAN.Read(CAN_BUS)
            if hex(mess[1].ID) != "0x0":
                all_data = str(ind) + ')' + "\t"
                offset = (time.time() - start_time)*1000
                all_data += "{:.1f}".format(offset) + "\t"
                id_hex = hex(mess[1].ID)[2:]
                for _ in range(4 - len(id_hex)):
                    id_hex = '0' + id_hex.upper()
                all_data += str(mess[1].MSGTYPE) + "\t" + id_hex + "\t" + str(hex(mess[1].LEN)[2:]) 
                for j in range(mess[1].LEN):
                    data_hex = hex(mess[1].DATA[j])[2:]
                    for _ in range(2 - len(data_hex)):
                        data_hex = '0' + data_hex.upper()
                    all_data += "\t" + data_hex.upper()
                all_data += "\n"
                ind += 1
                f.write(all_data)
                print(all_data)

    # All initialized channels are released
    CAN.Uninitialize(PCAN_NONEBUS)