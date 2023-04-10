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

unused_byte = {'0165': 3, '02B0': 3, '04B0': None, '0164': 0, '0370': 0, '043F': 2, '0440': 0, 
 '0018': 0, '0316': 7, '018F': 0, '0080': 1, '0081': 3, '0260': 3, '02A0': 1, 
 '0153': 0, '0220': None, '0329': 7, '0382': 0, '0545': 0, '04F0': 0, '04B1': 4,
 '0350': 1, '01F1': 0, '02C0': 0, '04F2': 0, '0120': 0, '0517': 1, '0587': 0, '00A0': 6,
 '00A1': 2, '0510': 0, '05E4': 0, '059B': 0, '0110': 0, '0050': 0, '04F1': 0, '0690': 0,
 '05F0': 0, '051A': 0, '0034': 0, '05A0': 0, '05A2': 0, '0042': 0, '0043': 0, '0044': 0}

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
    time_offset = 0.001
    Fuzzing_attack = TPCANMsg()
    Fuzzing_attack.ID = int(data_iloc[3],16)
    Fuzzing_attack.LEN = int(data_iloc[4])
    Fuzzing_attack.MSGTYPE = PCAN_MESSAGE_STANDARD
    all_datas += str(hex(Fuzzing_attack.ID)) + "\t" + str(Fuzzing_attack.MSGTYPE) + "\t" + str(hex(Fuzzing_attack.LEN)) 

    if data_iloc[3] in unused_byte:
        unused_index = unused_byte[data_iloc[3]]
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
    time.sleep(time_offset)


if __name__ == "__main__":
    dataset_path = "W:\\temp\\attack_data_tools\\Attack_tools\\Fuzzing Attack\\Dataset\\"
    dataset_name = "2022.08.12 구쏘울 C-CAN (정상).trc"
    df_dataset = Convert_to_Dataframe(dataset_path+dataset_name)[17:]
    nID = list(dict.fromkeys(df_dataset["ID"]))
    ilo_df = df_dataset.iloc
    for i in range(10):
        print(bcolors.OKBLUE)
        print(bcolors.OKBLUE + str(ilo_df[i][3]), end="\t")
        print(ilo_df[i][2], end="\t")
        print(ilo_df[i][4], end="\t")
        for j in range(int(ilo_df[i][4])):
            print(ilo_df[i][5+j], end = '\t')
        print(bcolors.ENDC)
        Replay_attack(ilo_df[i])
    
    
    

