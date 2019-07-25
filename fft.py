import sys
from io import StringIO
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.signal import stft
import time
import json
from os import listdir, walk
from os.path import isfile, isdir, join
import \
    matplotlib.font_manager as fm  # for using external font resource on Plot, below is loading NotoSansCJKtc-Medium.otf font
import pandas as pd
import math
from sklearn import preprocessing


# design not yet
# class fftData:
#     def __init__(self, group, participants):

def takeClosest(myList, myNumber):
    orderFreq = min(myList, key=lambda x: abs(x - myNumber))
    return orderFreq, myList.index(orderFreq)

def outputOrders2File(freqList, fileName, fp):
    freqCombine = ''
    for freq in freqList:
        freqCombine += ',' + str(freq)
    fp.write('%s%s\n' % (fileName, freqCombine))
    # fp.write('%s\n' % (fileName))

dbg = False  # debug flag
subDBG = False  # sub debug flag

np.set_printoptions(threshold=np.inf)  # enable for print every elements in numpy array

dirPath = r'vibration_data/A'

# drawing a vibration of time waveform format
fontPath = r'C:\ProgramData\Anaconda3\pkgs\matplotlib-3.0.3-py36hc8f65d3_0\Lib\site-packages\matplotlib\mpl-data\fonts\ttf\NotoSansCJKtc-Medium.otf'
cht_font = fm.FontProperties(fname=fontPath, size=10)

fileCreateTime = time.time()
fp = open('ML_Data_' + str(int(fileCreateTime)) + '.csv', 'a', encoding='utf-8')
# fp.write('2P-1_B_F_3,2P-1_B_F_2,2P-1_A_F_3,2P-1_A_E_2,2P-1_B_E_3,2P-1_B_E_2,2P-1_A_E_3\n')

headerString = ''
for i in range(1, 41):
    headerString += ',' + str(i)

fp.write('fileName,' + headerString[1:] + '\n')

for root, dirs, files in walk(dirPath):  # root:string, dirs&files:list
    modelLabel, fixedLabel = '', ''
    # print(root)
    # print(dirs)
    print(files)

    if len(files) != 0:
        files.sort(reverse=True)

        modelLabel = root[root.find('/') + 1:root.rfind('/')]
        # fixLabel = root[root.rfind('/') + 1:]

        print(modelLabel)

        for idx in range(len(files)):
            # To check avoiding appear .DS_Store files by MacOS
            # print(files[idx])

            # if '_2' in files[idx] or '_3' in files[idx]:
            with open(root + '/' + files[idx]) as f:
                data = f.read()
                data = data.split('\n')

            xf_x_float4 = []
            # 1:X_Axis, 2:X&Y_Axis
            for axes in range(2):
                x_axis_g_List = [float(row.split()[axes + 1]) for row in data if '#' not in row and len(row) != 0]

                N = 100000
                T = 1.0 / 5000.0

                # include real and image number, need to do abs processing next.
                yf_x = fft(x_axis_g_List)

                # Just first half of the spectrum, as the second is the negative copy
                xf_x = np.linspace(0.0, 1.0 / (2.0 * T), N / 2)  # X軸 start = 0, end = 2500, axis = 5000(samples)

                yf_x_abs = abs(fft(x_axis_g_List)) / (len(x_axis_g_List) / 2)
                yf_x_half = yf_x_abs[range(int(len(x_axis_g_List) / 2))]  # 由於對稱性，只取一半區間

                # for index in range(len(xf_x)):
                #     xf_x_float4.append(round(xf_x[index], 4))

                yf_x_float4 = []
                for index in range(len(yf_x_half)):
                    yf_x_float4.append(round(yf_x_half[index], 4))

                xf_x_float4 = []
                for index in range(len(xf_x)):
                    xf_x_float4.append(round(xf_x[index], 4))

                orderFreqDic = {}
                baseFreq = -1
                # Figure out the order frequencies that can be divisible by base frequency
                for i in range(len(xf_x_float4)):
                    if xf_x_float4[i] > 55 and xf_x_float4[i] <= 60:
                        orderFreqDic[xf_x_float4[i]] = yf_x_float4[i]
                baseFreq = max(orderFreqDic, key=orderFreqDic.get)  # find the base frequency

                ordersFreqList = []
                ordersAmpList = []
                for i in range(1, 41):
                    myNumber = baseFreq * i
                    orderFreq, index = takeClosest(xf_x_float4, myNumber)
                    ordersFreqList.append(orderFreq)
                    ordersAmpList.append(yf_x_float4[index])

                test = np.asarray(ordersAmpList)
                # x = test.reshape(-1, 1)
                # normalizer = preprocessing.Normalizer().fit(x)
                x_scaled = preprocessing.scale(test)
                # print(x_scaled)


            # print("filename: %s, count of less than 0.001: %d\n"%(files[idx], sum(i < 0.001 for i in xf_x_float4)))
            outputOrders2File(x_scaled, files[idx], fp)

fp.close()