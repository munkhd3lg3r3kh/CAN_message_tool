from PCANBasic import *
import random
import time
import datetime
from os import walk
import pandas as pd 

cols = ["No", "Time_Offset", "Type", "ID", "Data_Length", 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight']

unused_bytes = {}
used_bytes = []

if __name__ == "__main__":
    CAN = PCANBasic()                           #CAN 생성자 
    CAN_BUS = PCAN_USBBUS1
    # time_offset = random.uniform(0.001, 0.5)
    first_time = True
    prev_time_gap = 0.0
    start_time = time.time()

    waiter = 0
    result = CAN.Initialize(CAN_BUS, PCAN_BAUD_500K, 2047, 0, 0) #Channel, Btr, HwType, IOPort, INterrupt
    if result != PCAN_ERROR_OK:           
        print("oh No")
        CAN.GetErrorText(result)
        print(result)
        exit()
    mess = CAN.Read(CAN_BUS)
    while True:
        if hex(mess[1].ID) != "0x0":
            id_hex = hex(mess[1].ID)[2:]
            for _ in range(4 - len(id_hex)):
                id_hex = '0' + id_hex.upper()
                         
            offset = time.time() - start_time
            some = {cols[1]: offset, 
                    cols[2]: mess[1].MSGTYPE,
                    cols[3]: id_hex,
                    cols[4]: str(hex(mess[1].LEN)[2:])}
            for i in range(mess[1].LEN):
                data_hex = hex(mess[1].DATA[j] - 1)[2:]
                for _ in range(2 - len(data_hex)):
                    some[cols[5+i]] = '0' + data_hex.upper()
            if first_time == True: 


            