import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import time
import json

dbg = False #debug flag
subDBG = False #sub debug flag

np.set_printoptions(threshold=np.inf)  #enable for print every elements in numpy array

dirPath = r"vibration_data"
files = [f for f in os.listdir(dirPath) if os.path.isfile(os.path.join(dirPath, f))]

with open(dirPath + "\\" + files[0]) as f:
    data = f.read()
data = data.split('\n')

import matplotlib.font_manager as fm #for using external font resource on Plot, below is loading NotoSansCJKtc-Medium.otf font
fontPath = r'C:\ProgramData\Anaconda3\pkgs\matplotlib-3.0.3-py36hc8f65d3_0\Lib\site-packages\matplotlib\mpl-data\fonts\ttf\NotoSansCJKtc-Medium.otf'
cht_font = fm.FontProperties(fname=fontPath, size=10)
plt.subplots_adjust(left=None, bottom=0.070, right=None, top=0.950, wspace=None, hspace=0.320)

fig = plt.figure(1)
plt.subplot(311)
x_labels = [float(row.split()[0]) for row in data if "#" not in row and len(row) != 0]
y_labels = [float(row.split()[1]) for row in data if "#" not in row and len(row) != 0]
plt.plot(x_labels, y_labels, color='blue')
plt.title('原始資料 (acceleration)', fontproperties=cht_font)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude (g-value)')

for times in range(1): #1:x_axis, 2:x&y_axis
    # for i in range(len(files)):
    for i in range(1): #file_amount
        # print(result[i])
        with open(dirPath + "\\" + files[i]) as f:
            data = f.read()
        data = data.split('\n')

        x_axis_g_List = [float(row.split()[times + 1]) for row in data if "#" not in row and len(row) != 0]  # the type of t is 'list'

        N = 100000
        T = 1.0 / 5000.0

        yf_x = fft(x_axis_g_List) #include real and image number, need to do abs processing next.
        # Just first half of the spectrum, as the second is the negative copy
        xf_x = np.linspace(0.0, 1.0 / (2.0 * T), N/2)  #X軸 start = 0, end = 2500, axis = 5000(samples)

        yf_x_abs = abs(fft(x_axis_g_List)) / ((len(x_axis_g_List) / 2))
        yf_x_half = yf_x_abs[range(int(len(x_axis_g_List) / 2))]  # 由於對稱性，只取一半區間

        # print(len(yf2)) #for check output  after doing FFT
        # print(yf2[:500]) #for check previous 500 output after doing FFT

        yf_x_float6 = []
        for index in range(len(yf_x_half)):
            yf_x_float6.append(round(yf_x_half[index], 6))

        xf_x_float6 = []
        for index in range(len(xf_x)):
            xf_x_float6.append(round(xf_x[index], 6))

        plt.subplot(312)
        plt.plot(xf_x_float6, yf_x_float6, label=files[i] + ("_X axis" if times + 1 == 1 else "_Y axis"), color='green')
        plt.title('頻譜 (FFT Spectrum)', fontproperties=cht_font)
        plt.xlabel("Frenquency (Hz)")
        plt.ylabel("Amplitude (g-value)")
        plt.ylim(-0.1, 0.5)

        #output the FFT result
        with open("X_axis_FFT" if times + 1 == 1 else "Y_axis_FFT", 'w') as f:
            for idx in range(len(xf_x_float6)):
                f.write("%s\t%s\n" % (xf_x_float6[idx], yf_x_float6[idx]))

#find base order freqency
currencyFreqDic = {} #store currency frequency possible postion
orderFreqDic = {} #store orders frequency within 40x Frequency and Amplitude

ordersFreqList = []
ordersAmpList = []

baseFreq = -1
for i in range(len(xf_x_float6)):
    if int(xf_x_float6[i]) % int(baseFreq) == 0 and xf_x_float6[i] % int(baseFreq) <= 1 and i != 0 and baseFreq != -1: #找基頻以外的倍頻
        orderFreqDic[xf_x_float6[i]] = yf_x_float6[i]
    elif xf_x_float6[i] > 55 and xf_x_float6[i] <= 60:
        orderFreqDic[xf_x_float6[i]] = yf_x_float6[i]
        baseFreq = max(orderFreqDic, key=orderFreqDic.get)
    elif xf_x_float6[i] > 120 and xf_x_float6[i] <= 121:
        currencyFreqDic[xf_x_float6[i]] = yf_x_float6[i]
    else:
        if xf_x_float6[i] > 60 and len(orderFreqDic) != 0:
            # ordersFreq = max(orderFreqDic, key=orderFreqDic.get)
            ordersFreqList.append(max(orderFreqDic, key=orderFreqDic.get))
            ordersAmpList.append(orderFreqDic[max(orderFreqDic, key=orderFreqDic.get)])
            orderFreqDic = {}
        elif len(currencyFreqDic) != 0:
            currencyFreq = max(currencyFreqDic, key=currencyFreqDic.get)
            # print(currencyFreq)

ordersFreqList = ordersFreqList[:40]
ordersAmpList = ordersAmpList[0:40]

if dbg == True:
    print(ordersFreqList, ordersAmpList, sep='\n') #The frequencies of Orders and corresponding amplitudes

plt.subplot(313)
plt.plot(xf_x_float6, yf_x_float6, color='green')
plt.errorbar(ordersFreqList, ordersAmpList, fmt='o', color='red', ecolor='LightSteelBlue', elinewidth=0.5)
plt.title('倍頻', fontproperties=cht_font)

for i in range(len(ordersFreqList)):
    plt.text(ordersFreqList[i], ordersAmpList[i], str(i+1)+'x')
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

print(mFreqDic)

jsonData = json.dumps(mFreqDic, indent=4, separators=(',', ': '))

# test = json.loads(jsonData)

print(jsonData)

# plt.show()