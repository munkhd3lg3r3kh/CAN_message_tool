from __future__ import print_function
from PCANBasic import *
import random
import time
import os.path
import datetime
import pandas as pd

# this program can detect Replay, DoS, Fuzzy
# Replay + 1 ==> -1
# DoS + 2 ==> -2
# Replay + 3 ==> Random
#

unused_byte = pd.read_csv("Unused Bytes/KIA_SOUL_2014.csv", sep=";")


cols = ["No", "Time_Offset", "Type", "ID", "Data_Length", 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Label']
x = datetime.datetime.now()
x = "Dataset\\Replay Attack Injected Datas " + str(x).split()[0] + "-"
ind = 0

while os.path.isfile( x + str(ind) + ".txt"):
    ind += 1
    print("Yes")

print("No")
x = x + str(ind) + ".txt"
f = open(x, "a")

# all_data = "No\tID\tTYPE\tLEN\tONE\tTWO\tTHREE\tFOUR\tFIVE\tSIX\tSEVEN\tEIGHT\n"
all_data = ""
for col in cols:
    all_data += col + "\t"

print(all_data)
f.write(all_data + "\n")
def update_progress(progress):
    print("\r progress [{0}] {1}%".format('#'*(progress//10), progress), end='')
    

if __name__ == "__main__":
    CAN = PCANBasic()                            #CANi
    CAN_BUS = PCAN_USBBUS1
    result = CAN.Initialize(CAN_BUS, PCAN_BAUD_500K, 2047, 0, 0) #Channel, Btr, HwType, IOPort, INterrupt

    if result != PCAN_ERROR_OK:
        # An error occurred, get a text describing the error and show it
        #
        print("oh No")
        CAN.GetErrorText(result)
        print(result)
    counter = 0
    start_time = time.time()
    ind = 1
    while True: 
        # print("PCAN-USB Pro FD (Ch-1) was initialized")
        mess = CAN.Read(CAN_BUS)
        # if hex(mess[1].ID) != "0x0":
        label_data = "Legitimate"
        all_data = str(ind) + ')' + "\t"
        offset = (time.time() - start_time)*1000
        all_data += "{:.1f}".format(offset) + "\t"
        id_hex = hex(mess[1].ID)[2:]
        for _ in range(4 - len(id_hex)):
            id_hex = '0' + id_hex.upper()
        
        all_data += str(mess[1].MSGTYPE) + "\t" + id_hex + "\t" + str(hex(mess[1].LEN)[2:]) 

        for j in range(mess[1].LEN):
            if id_hex in list(unused_byte["ID"]):
                check_val = int(unused_byte[unused_byte["ID"] == id_hex].iloc[0][2], 16)
                check_ind = int(unused_byte[unused_byte["ID"] == id_hex].iloc[0][1])

                if check_ind == j and mess[1].DATA[check_ind] == (check_val + 1):
                    print("Replay")
                    label_data = "Replay"
                    data_hex = hex(mess[1].DATA[j] - 1)[2:]
                elif check_ind == j and mess[1].DATA[check_ind] == ( check_val + 2):
                    print("DoS")
                    label_data = "DoS"
                    data_hex = hex(mess[1].DATA[j] - 2)[2:]
                elif check_ind == j and mess[1].DATA[check_ind] == ( check_val + 3):
                    print("Fuzzy")
                    label_data = "Fuzzy"
                    data_hex = hex(random.randrange(0, 255))[2:]
                else:
                    data_hex = hex(mess[1].DATA[j])[2:]  
            else:
                data_hex = hex(mess[1].DATA[j])[2:]  

            for _ in range(2 - len(data_hex)):
                data_hex = '0' + data_hex.upper()

            all_data += "\t" + data_hex.upper()
        for _ in range(mess[1].LEN, 8):
            all_data += "\t" + "-1"
            
        all_data += "\t" + label_data 
        all_data += "\n"
        ind += 1
        print(all_data)
        f.write(all_data)

    # All initialized channels are released
    CAN.Uninitialize(PCAN_NONEBUS)
