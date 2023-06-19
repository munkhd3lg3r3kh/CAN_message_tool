import matplotlib.pyplot as plt
import pandas as pd
import math
import time
from os import walk
import numpy as np

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

output_path = "D:\Test"
dirs = ["2022.03.28", "2022.08.12"]


for direc in dirs:
    df_path = "D:\\" + direc + "\\"
    filenames = next(walk(df_path), (None, None, []))[2]  # [] if no file
    for file in filenames:
        if "CAN" in file:
            if "DoS" in file and "C-CAN" in file:
                print(file)
                normal_df = Convert_to_Dataframe(df_path+file)[17:]
                normal_df["Label"] = np.nan
                normal_df.loc[normal_df["ID"] == "0000", "Label"] = "DoS"
                normal_df.loc[normal_df["ID"] != "99", "Label"] = "Legitimate"
                for i in range(8):
                    normal_df[cols[i+5]] = normal_df[cols[i+5]].fillna(-1)
        else:
            if "DoS" in file:
                print(file)
                normal_df = Convert_to_Dataframe(df_path+file)[17:]
                normal_df["Label"] = np.nan
                normal_df.loc[normal_df["ID"] == "0000", "Label"] = "DoS"
                normal_df.loc[normal_df["ID"] != "99", "Label"] = "Legitimate"
                for i in range(8):
                    normal_df[cols[i+5]] = normal_df[cols[i+5]].fillna(-1)
        