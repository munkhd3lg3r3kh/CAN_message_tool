from __future__ import print_function
from PCANBasic import *
import random
import time
import os.path
import datetime

unused_bits = {'0165': [3, '00'], '051A': [0, '00'], '02B0': [3, '07'], '00A0': [6, '00'],
 '05E4': [0, '00'], '0153': [4, '00'], '02A0': [1, '00'], '0120': [0, '00'], '043F': [2, '60'],
 '0316': [7, '7F'], '04B1': [4, '00'], '0050': [0, '00'], '0164': [0, '00'], '0018': [1, '00'],
 '0044': [0, '00'], '0110': [0, 'E0'], '05F0': [0, '00'], '0329': [7, '10'], '0440': [3, '00'],
 '00A1': [2, '80'], '04F2': [4, '00'], '018F': [6, '00'], '0382': [0, '40'], '04F0': [0, '00'],
 '05A2': [0, '25'], '0034': [0, '00'], '0260': [3, '30'], '01F1': [0, '00'], '02C0': [0, '3D'],
 '0517': [1, '00'], '05A0': [0, '00'], '0080': [1, '17'], '04F1': [2, '00'], '0043': [0, '00'],
 '0350': [5, '00'], '059B': [0, '00'], '0081': [3, '00'], '0042': [1, 'FF'], '0510': [0, '00'],
 '0690': [0, '03'], '0587': [0, '00'], '0370': [0, 'FF']}

cols = ["No", "Time_Offset", "Type", "ID", "Data_Length", 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight']
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
f.write(all_data)
def update_progress(progress):
    print("\r progress [{0}] {1}%".format('#'*(progress//10), progress), end='')
    

if __name__ == "__main__":
    CAN = PCANBasic()                            #CANi
    CAN_BUS = PCAN_USBBUS1
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
                    
            
                if id_hex in unused_bits:
                    check_val = int(unused_bits[id_hex][1], 16) + 1
                    check_ind = int(unused_bits[id_hex][0])
                
                    if mess[1].DATA[check_ind] == check_val:
                        all_data += str(99) + "\t" + id_hex + "\t" + str(hex(mess[1].LEN)[2:]) 
                    elif mess[1].DATA[check_ind] == ( check_val + 1 ):
                        all_data += str(98) + "\t" + id_hex + "\t" + str(hex(mess[1].LEN)[2:])
                    else:
                        all_data += str(mess[1].MSGTYPE) + "\t" + id_hex + "\t" + str(hex(mess[1].LEN)[2:]) 
                else: 
                    all_data += str(mess[1].MSGTYPE) + "\t" + id_hex + "\t" + str(hex(mess[1].LEN)[2:]) 

                for j in range(mess[1].LEN):
                    if id_hex in unused_bits and check_ind == j and mess[1].DATA[check_ind] == check_val:
                        print("yes")
                        print(all_data)
                        data_hex = hex(mess[1].DATA[j] - 1)[2:]
                    elif id_hex in unused_bits and check_ind == j and mess[1].DATA[check_ind] == ( check_val + 1 ):
                        print("DoS")
                        data_hex = hex(mess[1].DATA[j] - 2)[2:]
                    else:
                        data_hex = hex(mess[1].DATA[j])[2:]  
                    
                    for _ in range(2 - len(data_hex)):
                        data_hex = '0' + data_hex.upper()
     
                    all_data += "\t" + data_hex.upper()
                all_data += "\n"
                ind += 1
                print(all_data)
                f.write(all_data)

    # All initialized channels are released
    CAN.Uninitialize(PCAN_NONEBUS)
