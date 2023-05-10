import pandas as pd
import time
from PCANBasic import *

cols = ["No", "Time_Offset", "Type", "ID", "Data_Length", 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight']
CAN = PCANBasic()                            #CAN 생성자 

#importing dataset
def Convert_to_Dataframe(path):
    test = pd.read_csv(path, encoding='cp949', index_col=0)
    b = []
    for i in test.index:
        temp = i.split(" ")
        b.append(list(filter(('').__ne__, temp)))
    #final = pd.DataFrame(b, columns = ["No", "Time_Offset", "Type", "ID", "Data_Length", 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight'])
    final = pd.DataFrame(b, columns = cols)
    return final


def Injector(id, leng, data):
    all_datas = ""
    time_offset = 0.001
    Fuzzing_attack = TPCANMsg()
    Fuzzing_attack.ID = int(id,16)
    Fuzzing_attack.LEN = leng
    Fuzzing_attack.MSGTYPE = PCAN_MESSAGE_STANDARD
    all_datas += str(hex(Fuzzing_attack.ID)) + "\t" + str(Fuzzing_attack.MSGTYPE) + "\t" + str(hex(Fuzzing_attack.LEN)) 

    for i in range(leng):
        Fuzzing_attack.DATA[i] = int(data[i],16)
        all_datas += "\t" + str(hex(Fuzzing_attack.DATA[i]))

    all_datas += "\n"
    res = CAN.Write(CAN_BUS, Fuzzing_attack)
    if res != PCAN_ERROR_OK:
        print("Oh nooo")
        result = CAN.GetErrorText(res)
        print(result)
        CAN.Uninitialize()
        exit()
        
    print(all_datas)
    time.sleep(time_offset)



def find_IDs(data_frame):
    temp1 = data_frame["ID"]
    return list(dict.fromkeys(temp1))


if __name__ == "__main__":
    
    CAN_BUS = PCAN_USBBUS1
    res = CAN.Initialize(CAN_BUS, PCAN_BAUD_500K, 2047, 0, 0) #Channel, Btr, HwType, IOPort, INterrupt
    
    if res != PCAN_ERROR_OK:
        print("Oh nooo")
        result = CAN.GetErrorText(res)
        print(result)
        CAN.Uninitialize()
        exit()
    
    dataset_path = "W:\\New_ERA\\CAN_message_tool\\Dataset\\Tesla - 2022.05.04\\"
    vcan = Convert_to_Dataframe(dataset_path + "2022.05.04 VCAN.trc")[17:]

    nID = find_IDs(vcan)
    nID.sort()
    print(nID[0])
    spec_df = vcan[vcan["ID"] == nID[0]]
    spec_list = spec_df.iloc

    time_offset = 0.1

    for i in range(50):
        datas = []
        leng = int(spec_list[i][4], 16)

        for j in range(leng):
            datas.append(spec_list[i][j+5])

        Injector(spec_list[i][3], leng, datas)

    CAN.Uninitialize()