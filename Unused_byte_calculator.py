import pandas as pd
from os import walk

def Convert_to_df(path):
    if path[-3:] == "trc":
        data_df = Convert_from_trc(path)[17:]
    elif path[-3:] == "txt": 
        data_df = Convert_from_txt(path)[1:]
    else:
        print("Error, not suitable file")
        exit()
    return data_df

def Convert_from_txt(path):
    test = pd.read_csv(path, encoding='cp949', index_col=0)
    b = []
    for i in test.index:
        temp = i.split("\t")
        b.append(list(filter(('').__ne__, temp)))
    final = pd.DataFrame(b, columns = cols)
    return final

def Convert_from_trc(path):
    test = pd.read_csv(path, encoding='cp949', index_col=0)
    b = []
    for i in test.index:
        temp = i.split(" ")
        b.append(list(filter(('').__ne__, temp)))
    final = pd.DataFrame(b, columns = cols)
    return final

def find_IDs(data_frame):
    temp1 = data_frame["ID"]
    return list(dict.fromkeys(temp1))
    

def find_unused_bytes(dataframe):
    unused_bytes = {}
    IDs = find_IDs(dataframe)
    for ID in IDs:
        spec_df = dataframe[dataframe["ID"] == ID]
        l = int(spec_df["Data_Length"].iloc[0])
        t_order = []
        t_value = []
        for i in range(l): 
            temp = list(dict.fromkeys(spec_df[cols[5+i]]))
            if len(temp) == 1:
                t_order.append(i)-
                t_value.append(temp[0])
        if t_order:
            unused_bytes[ID] = [t_order, t_value]
    return unused_bytes

cols = ["No", "Time_Offset", "Type", "ID", "Data_Length", 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight']

dataset_path = "C:\\Users\\munkh\\Documents\\DBC\\KIA SOUL\\"

unused_bits = {'0165': [3, '00'], '02B0': [3, '07'], '0164': [0, '00'], '0370': [0, 'FF'], '043F': [2, '60'], '0440': [0, 'FF'],
 '0018': [0, '00'], '0316': [7, '7F'], '018F': [0, 'FE'], '0080': [1, '17'], '0081': [3, '00'], '0260': [3, '30'], '02A0': [1, '00'],
 '0153': [0, '00'], '0329': [7, '10'], '0382': [0, '40'], '0545': [0, 'C8'], '04F0': [0, '00'], '04B1': [4, '00'], '0350': [1, '2B'],
 '01F1': [0, '00'], '02C0': [0, '3D'], '04F2': [0, 'A0'], '0120': [0, '00'], '0517': [1, '00'], '0587': [0, '00'], '00A0': [6, '00'],
 '00A1': [2, '80'], '0510': [0, '00'], '05E4': [0, '00'], '059B': [0, '00'], '0110': [0, 'E0'], '0050': [0, '00'], '04F1': [0, 'C0'],
 '0690': [0, '03'], '05F0': [0, '00'], '051A': [0, '00'], '0034': [0, '00'], '05A0': [0, '00'], '05A2': [0, '25'], '0042': [0, '0B'],
 '0043': [0, '00'], '0044': [0, '00']}

f = []
filenames = next(walk(dataset_path), (None, None, []))[2]  # [] if no file

# for file in filenames:
#     print(print(filenames))

for i in range(1, len(filenames)):
    
    df_path = dataset_path + filenames[i-1]
    a1 = find_unused_bytes(Convert_to_df(str(dataset_path + filenames[i-1])))
    a2 = find_unused_bytes(Convert_to_df(str(dataset_path + filenames[i])))
    
    print("Enumerate Counter: {0}".format(i+1))
    # Find keys present in dict2 but not in dict1
    keys_only_in_dict1 = set(a1.keys()) - set(a2.keys())

    # Find keys present in dict2 but not in dict1
    keys_only_in_dict2 = set(a2.keys()) - set(a1.keys())

    print("Keys only in dict1:", keys_only_in_dict1)
    print("Keys only in dict2:", keys_only_in_dict2)

