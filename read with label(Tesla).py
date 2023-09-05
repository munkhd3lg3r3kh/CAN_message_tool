from __future__ import print_function
from PCANBasic import *
import random
import time
import os.path
import datetime
import sys

unused_bits = {'03FE': [2, '00'], '0238': [2, '9A'], '03DC': [0, '40'], '0502': [0, '00'], '027D': [0, '01'],
 '0284': [0, '10'], '0321': [4, '02'], '030E': [1, '00'], '02A8': [1, '00'], '032E': [0, '00'], '03F8': [0, '03'],
 '0231': [2, '00'], '02BC': [7, '01'], '0257': [6, '00'], '0479': [0, '00'], '0401': [0, '81'], '03D5': [1, '00'],
 '0420': [0, '28'], '02E8': [1, '00'], '0353': [1, '0F'], '037E': [2, '00'], '0103': [2, '00'], '0129': [6, 'FF'],
 '0717': [2, '00'], '03F4': [5, '01'], '0031': [2, '02'], '036F': [0, '08'], '0391': [2, '00'], '03AF': [7, 'FF'],
 '0145': [2, '00'], '030F': [3, '01'], '0410': [1, '00'], '034F': [7, 'FF'], '03C2': [1, '55'], '032B': [0, '00'],
 '0448': [0, '00'], '035D': [1, '00'], '0128': [0, '00'], '0428': [0, '00'], '0350': [0, '00'], '0371': [1, '00'], 
 '03B8': [0, '00'], '03F7': [0, '00'], '03CB': [1, '00'], '03EF': [0, '00'], '031E': [3, '14'], '0303': [0, '03'], 
 '03CA': [0, '00'], '0249': [3, '00'], '0227': [2, '00'], '03D1': [5, '00'], '021E': [4, '00'], '0186': [7, '00'],
 '0102': [2, '00'], '02F8': [5, 'DE'], '03FD': [1, '00'], '02D1': [0, 'FF'], '03FA': [7, 'FF'], '024A': [0, '00'],
 '03FC': [1, '00'], '0419': [0, '00'], '0558': [0, '84'], '036C': [0, '00'], '0239': [5, '7D'], '026E': [1, '00'],
 '039D': [4, '00'], '0221': [2, '55'], '0399': [4, 'B0'], '0108': [7, '00'], '0329': [0, '00'], '004F': [6, '79'],
 '0229': [2, '00'], '025F': [0, 'C4'], '0326': [1, '00'], '0439': [0, '00'], '0334': [0, '1F'], '0293': [0, '00'],
 '0267': [3, '00'], '03C3': [0, '55'], '0051': [2, '0A'], '0425': [0, '00'], '0720': [0, '00'], '03F0': [0, '00'],
 '0259': [0, 'D3'], '0429': [0, '00'], '03C9': [0, '03'], '0395': [1, '00'], '0449': [0, '00'], '033E': [0, '00'],
 '0459': [0, '00'], '0369': [1, '00'], '0740': [1, '00'], '0211': [2, '41'], '0234': [3, '09'],  '03DF': [0, '00'], 
 '0235': [1, '01']}



cols = ["No", "Time_Offset", "Type", "ID", "Data_Length", 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Label']

    

if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("Please dataset type: (e.g, Attack-Dos, Normal etc)")
        dataset_type = input("Please dataset type: ")
    else:
        dataset_type = sys.argv[1]
    
    x = datetime.datetime.now()
    x = "Dataset\\Tesla " + dataset_type + " Dataset " + str(x).split()[0] + "-"
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
    

    CAN = PCANBasic()                            #CANi
    CAN_BUS = PCAN_USBBUS1
    result = CAN.Initialize(CAN_BUS, PCAN_BAUD_500K, 2047, 0, 0) #Channel, Btr, HwType, IOPort, INterrupt

    if result != PCAN_ERROR_OK:
        # An error occurred, get a text describing the error and show it
        #
        print("oh No")
        CAN.GetErrorText(result)
        print(result)
    print("Succesfully Connected")
    counter = 0
    start_time = time.time()
    ind = 1
    while True:
        # print("PCAN-USB Pro FD (Ch-1) was initialized")
        mess = CAN.Read(CAN_BUS)
        if hex(mess[1].ID) != "0x0":
            label_data = "Legitimate"
            all_data = str(ind) + ')' + "\t"
            offset = (time.time() - start_time)*1000
            all_data += "{:.1f}".format(offset) + "\t"
            id_hex = hex(mess[1].ID)[2:]
            for _ in range(4 - len(id_hex)):
                id_hex = '0' + id_hex.upper()
            
            all_data += str(mess[1].MSGTYPE) + "\t" + id_hex + "\t" + str(hex(mess[1].LEN)[2:]) 
                
            for j in range(mess[1].LEN):
                if id_hex in unused_bits:
                    check_val = int(unused_bits[id_hex][1], 16)
                    check_ind = int(unused_bits[id_hex][0])

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
