import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.signal import stft
import time
import json
from os import listdir, walk
from os.path import isfile, isdir, join
import matplotlib.font_manager as fm  # for using external font resource on Plot, below is loading NotoSansCJKtc-Medium.otf font

def takeClosest(myList, myNumber):
    orderFreq = min(myList, key=lambda x: abs(x - myNumber))
    return orderFreq, myList.index(orderFreq)

def outputOrders2File(xAxis, yAxis, fileName):
    # with open("X_axis_FFT" if times + 1 == 1 else "Y_axis_FFT", 'w') as f:
    with open(fileName, 'w') as f:
        for idx in range(len(xAxis)):
            f.write("%s\t%s\n" % (xAxis[idx], yAxis[idx]))

# def outputPureOrders2File(yAxis, fileName):
#     # with open("X_axis_FFT" if times + 1 == 1 else "Y_axis_FFT", 'w') as f:
#     with open(fileName, 'w') as f:
#         for idx in range(len(xAxis)):
#             f.write("%s,%s," % (yAxis[idx]))

dbg = False  # debug flag
subDBG = False  # sub debug flag

np.set_printoptions(threshold=np.inf)  # enable for print every elements in numpy array

dirPath = r"vibration_data"
# files = [f for f in os.listdir(dirPath) if os.path.isfile(os.path.join(dirPath, f))]

### Drawing a vibration of time waveform format ###
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
fp = open("ML_Data_" + str(int(fileCreateTime)), "a")
print(str(int(fileCreateTime)))

# """
for root, dirs, files in walk(dirPath): # root:string, dirs&files:list
    modelLabel, fixedLabel = "", ""
    if len(files) != 0:
        modelLabel = root[root.find('\\')+1:root.rfind('\\')]
        fixedLabel = root[root.rfind('\\')+1:]

        for idx in range(len(files)):
            with open(root + "\\" + files[idx]) as f:
                data = f.read()
                data = data.split('\n')
            print(data)

            for axes in range(2):  # 1:x_axis, 2:x&y_axis
                x_axis_g_List = [float(row.split()[axes + 1]) for row in data if "#" not in row and len(row) != 0]  # the type of t is 'list'

                N = 100000
                T = 1.0 / 5000.0

                yf_x = fft(x_axis_g_List)  # include real and image number, need to do abs processing next.

                # Just first half of the spectrum, as the second is the negative copy
                xf_x = np.linspace(0.0, 1.0 / (2.0 * T), N / 2)  # X軸 start = 0, end = 2500, axis = 5000(samples)

                yf_x_abs = abs(fft(x_axis_g_List)) / ((len(x_axis_g_List) / 2))
                yf_x_half = yf_x_abs[range(int(len(x_axis_g_List) / 2))]  # 由於對稱性，只取一半區間

                yf_x_float4 = []
                for index in range(len(yf_x_half)):
                    yf_x_float4.append(round(yf_x_half[index], 4))

                xf_x_float4 = []
                for index in range(len(xf_x)):
                    xf_x_float4.append(round(xf_x[index], 4))

                plt.subplot(312)
                plt.plot(xf_x_float4, yf_x_float4, label=files[idx] + ("_X axis" if axes + 1 == 1 else "_Y axis"), color='green')
                plt.title('頻譜 (FFT Spectrum)', fontproperties=cht_font)
                plt.xlabel("Frenquency (Hz)")
                plt.ylabel("Amplitude (g-value)")
                plt.ylim(-0.1, 0.5)

                # output the FFT result
                ##################################準備寫檔##############################
                outputOrders2File(xf_x_float4, yf_x_float4, 'ftt_raw')

                with open("X_axis_FFT" if axes + 1 == 1 else "Y_axis_FFT", 'w') as f:
                    for idx in range(len(xf_x_float4)):
                        f.write("%s\t%s\n" % (xf_x_float4[idx], yf_x_float4[idx]))

# find base order freqency
orderFreqDic = {}  # store orders frequency within 40x Frequency and Amplitude
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

if dbg == True:
    print(ordersFreqList, ordersAmpList, sep='\n')  # The frequencies of Orders and corresponding amplitudes

outputOrders2File(ordersFreqList, ordersAmpList, 'fft_orders')

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

# """