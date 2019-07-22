import sys
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


def takeClosest(myList, myNumber):
    orderFreq = min(myList, key=lambda x: abs(x - myNumber))
    return orderFreq, myList.index(orderFreq)

def outputOrders2File(freqList, fileName, fp):
    pos = ''

    freqCombine = ''
    for freq in freqList:
        freqCombine += ',' + str(freq)

    # fp.write('%s,%s,%s,%s,%s,%s\n' % (model.lower(), pos, axis, fixState, vibCombine[1:], fileName[:-4]))
    fp.write('%s\n' % (freqCombine[1:]))


dbg = False  # debug flag
subDBG = False  # sub debug flag

np.set_printoptions(threshold=np.inf)  # enable for print every elements in numpy array

dirPath = r'vibration_data'

# drawing a vibration of time waveform format
fontPath = r'C:\ProgramData\Anaconda3\pkgs\matplotlib-3.0.3-py36hc8f65d3_0\Lib\site-packages\matplotlib\mpl-data\fonts\ttf\NotoSansCJKtc-Medium.otf'
cht_font = fm.FontProperties(fname=fontPath, size=10)
# plt.subplots_adjust(left=None, bottom=0.070, right=None, top=0.950, wspace=None, hspace=0.320)
#
# fig = plt.figure(1)
# plt.subplot(311)
# x_labels = [float(row.split()[0]) for row in data if "#" not in row and len(row) != 0]
# y_labels = [float(row.split()[1]) for row in data if "#" not in row and len(row) != 0]
# plt.plot(x_labels, y_labels, color='blue')
# plt.title('原始資料 (acceleration)', fontproperties=cht_font)
# plt.xlabel('Time (s)')
# plt.ylabel('Amplitude (g-value)')

fileCreateTime = time.time()
fp = open('ML_Data_' + str(int(fileCreateTime)) + '.csv', 'a', encoding='utf-8')
# fp.write('model,position,axis,fix_state,order_1,order_2,order_3,order_4,order_5,order_6,order_7,order_8,order_9,order_10,order_11,order_12,order_13,order_14,order_15,order_16,order_17,order_18,order_19,order_20,order_21,order_22,order_23,order_24,order_25,order_26,order_27,order_28,order_29,order_30,order_31,order_32,order_33,order_34,order_35,order_36,order_37,order_38,order_39,order_40\n')

for root, dirs, files in walk(dirPath):  # root:string, dirs&files:list
    modelLabel, fixedLabel = '', ''
    # print(root)

    if len(files) != 0:
        modelLabel = root[root.find('/') + 1:root.rfind('/')]
        fixLabel = root[root.rfind('/') + 1:]
        if 'Before' in fixedLabel:
            fixedLabel = '0'
        elif 'After' in fixedLabel:
            fixedLabel = '1'

        for idx in range(len(files)):
            # To check avoiding appear .DS_Store files by MacOS
            # print(root + '/' + files[idx])

            if '(2)' in files[idx]:
                with open(root + '/' + files[idx]) as f:
                    data = f.read()
                    data = data.split('\n')

                xf_x_float4 = []
                # 1:X_Axis, 2:X&Y_Axis
                for axes in range(2):
                    x_axis_g_List = [float(row.split()[axes + 1]) for row in data if '#' not in row and len(row) != 0]  # the type of t is 'list'

                    N = 100000
                    T = 1.0 / 5000.0

                    # include real and image number, need to do abs processing next.
                    yf_x = fft(x_axis_g_List)

                    # Just first half of the spectrum, as the second is the negative copy
                    xf_x = np.linspace(0.0, 1.0 / (2.0 * T), N / 2)  # X軸 start = 0, end = 2500, axis = 5000(samples)

                    yf_x_abs = abs(fft(x_axis_g_List)) / ((len(x_axis_g_List) / 2))
                    yf_x_half = yf_x_abs[range(int(len(x_axis_g_List) / 2))]  # 由於對稱性，只取一半區間

                    # for index in range(len(xf_x)):
                    #     xf_x_float4.append(round(xf_x[index], 4))

                    for index in range(len(yf_x_half)):
                        xf_x_float4.append(round(yf_x_half[index], 4))

                    # plt.subplot(312)
                    # plt.plot(xf_x_float4, yf_x_float4, label=files[idx] + ("_X axis" if axes + 1 == 1 else "_Y axis"), color='green')
                    # plt.title('頻譜 (FFT Spectrum)', fontproperties=cht_font)
                    # plt.xlabel("Frenquency (Hz)")
                    # plt.ylabel("Amplitude (g-value)")
                    # plt.ylim(-0.1, 0.5)

                    # find base order freqency
                    # store filtered orders frequency within 40x Frequency and Amplitude
                    orderFreqDic = {}
                    baseFreq = -1

                    # output the FFT result
                    # outputOrders2File(modelLabel, fixLabel, axes, ordersFreqList, ordersAmpList, files[idx], fp)
                outputOrders2File(xf_x_float4, files[idx], fp)
fp.close()


"""
plt.subplot(313)
plt.plot(xf_x_float4, yf_x_float4, color='green')
plt.errorbar(ordersFreqList, ordersAmpList, fmt='o', color='red', ecolor='LightSteelBlue', elinewidth=0.5)
plt.title('倍頻', fontproperties=cht_font)

for i in range(len(ordersFreqList)):
    plt.text(ordersFreqList[i], ordersAmpList[i], str(i + 1) + 'x')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude (g-value)')
plt.ylim(-0.1, 0.5)

ticks = time.time()
mFreqDic = {}
# for i in range(len(multiFreqList_x)):
mFreqDic["apiKey"] = "tkk821has78dh17"
mFreqDic["model"] = "6P11"
mFreqDic["uploadTime"] = ticks
mFreqDic["freq"] = ordersFreqList
mFreqDic["amp"] = ordersAmpList
# print(mFreqDic)

jsonData = json.dumps(mFreqDic, indent=4, separators=(',', ': '))
# print(jsonData)

plt.show()

"""