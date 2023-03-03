from __future__ import print_function
import time

def update_progress(progress):
    print("\r progress [{0}] {1}%".format('#'*(progress//10), progress), end='')
j = 0
start_time = time.time()
while True:
    j += 1
    update_progress(j)
    time.sleep(0.001)
    if (time.time() - start_time) > 2.0:
        print((time.time() - start_time))
        break