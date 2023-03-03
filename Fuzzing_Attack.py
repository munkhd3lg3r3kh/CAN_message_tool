from PCANBasic import *
import time
import datetime
from os import walk
import keyboard
from rich.console import Console

def Fuzzing_Attack(id, leng, data):
    all_datas = ""
    time_offset = 0.001
    Fuzzing_attack = TPCANMsg()
    Fuzzing_attack.ID = int(id,16)
    Fuzzing_attack.LEN = leng
    Fuzzing_attack.MSGTYPE = PCAN_MESSAGE_STANDARD
    all_datas += str(hex(Fuzzing_attack.ID)) + "\t" + str(Fuzzing_attack.MSGTYPE) + "\t" + str(hex(Fuzzing_attack.LEN)) 

    for i in range(8):
        Fuzzing_attack.DATA[i] = int(data[i*2:i*2+2],16)
        all_datas += "\t" + str(hex(Fuzzing_attack.DATA[i]))

    all_datas += "\n"
    # print(all_datas)
    time.sleep(time_offset)


if __name__ == "__main__":
    x = datetime.datetime.now()
    x = "W:\\temp\\attack_data_tools\\Dastaset\\sometext-" + str(x).split()[0] + ".txt"

    f = open(x, "a")
    all_data = "ID\tTYPE\tLEN\tONE\tTWO\tTHREE\tFOUR\tFIVE\tSIX\tSEVEN\tEIGHT\n"
    f.write(all_data)
  
    fuzzing_path = "C:\\Users\\munkh\\Documents\\DBC\\Old Soul Datas\\Genisis"

    f = []
    j = 0
    
    for (dirpath, dirnames, filenames) in walk(fuzzing_path):
        f.extend(filenames)
        break

    console = Console()

    with console.status("[bold green]Working on tasks...") as status:        
        for id in f:

            start_time = time.time()
            fi = open(dirpath + "\\" + id, "r")
            id = id[1:-4]
            if '-' in id:
                continue
                #print(str[:-2])
            
            console.log(f"injection of ID({id}) has started")

            all_msg = fi.readlines()
            fi.close()
            
            for msg in all_msg:
                msg = msg[:-1]
                
                if len(msg)%2 != 0:
                    print("Invalid data has imported")
                    break
                l = int(len(msg)/2)
                t_off = time.time() - start_time            
                Fuzzing_Attack(id, l, msg)
                
                
            console.log(f"injection of ID: {id} has complete")

            while(t_off < 2):
                print("Waiting has started")
                if keyboard.is_pressed('q'):  
                    print('You Pressed A Key!')
                    break        

            
