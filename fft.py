import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import time
import json

def get_two_float(f_str, n):
    f_str = str(f_str)      # f_str = '{}'.format(f_str) 也可以转换为字符串
    a, b, c = f_str.partition('.')
    c = (c+"0"*n)[:n]       # 如论传入的函数有几位小数，在字符串后面都添加n为小数0
    return ".".join([a, c])

np.set_printoptions(threshold=np.inf)  # for print every elements in numpy array

dirPath = r"vibration_data"
files = [f for f in os.listdir(dirPath) if os.path.isfile(os.path.join(dirPath, f))]

with open(dirPath + "\\" + files[0]) as f:
    data = f.read()
data = data.split('\n')

import matplotlib.font_manager as fm
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
            for idx in range(2500):
                f.write("%s,%s\n" % (xf_x_float6[idx], yf_x_float6[idx]))

# multiFreqList_x = []
# multiFreqList_y = []

maxMultiFreq = []
maxAmp = 0
for i in range(1000, 1200):
    if yf_x_float6[i] > maxAmp:
        maxFreq = xf_x_float6[i]
        maxAmp = yf_x_float6[i]

print(maxFreq, maxAmp)

plt.show()


"""
for i in range(1, len(xf_x_float6)-1):
    if int(xf_x_float6[i]) % int(xf_x_float6[58]) == 0:
        multiFreqList_x.append(xf_x_float6[i])
        multiFreqList_y.append(yf_x_float6[i])

plt.subplot(313)
plt.plot(xf_x_float6, yf_x_float6, color='green')
plt.errorbar(multiFreqList_x, multiFreqList_y, fmt='o', color='red', ecolor='LightSteelBlue', elinewidth=0.5)
plt.title('倍頻', fontproperties=cht_font)
for i in range(len(multiFreqList_x)):
    plt.text(multiFreqList_x[i], multiFreqList_y[i], str(i+1)+'x')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude (g-value)')
plt.ylim(-0.1, 0.5)

ticks = time.time()
mFreqDic = {}
# for i in range(len(multiFreqList_x)):
mFreqDic["apiKey"] = "tkk821has78dh17"
mFreqDic["model"] = "6P11"
mFreqDic["uploadTime"] = ticks
mFreqDic["freq"] = multiFreqList_x
mFreqDic["amp"] = multiFreqList_y

# print(mFreqDic)

jsonData = json.dumps(mFreqDic, indent=4, separators=(',', ': '))

# test = json.loads(jsonData)

print(jsonData)

# plt.legend()

# plt.show()

# For_FFT
"""
"""
for times in range(2):
    # for i in range(len(files)):
    for i in range(1):
        # print(result[i])
        with open(dirPath + "\\" + files[i]) as f:
            data = f.read()
        data = data.split('\n')

        x_axis_g_List = [float(row.split()[times + 1]) for row in data if "#" not in row and len(row) != 0]  # the type of t is 'list'

        N = 5000
        T = 1.0 / 5000.0

        # print(x_axis_g_List)
        yf_x = fft(x_axis_g_List)
        # Just first half of the spectrum, as the second is the negative copy
        xf_x = np.linspace(0.0, 1.0 / (2.0 * T), N / 2)  # start = 0, end = 2500, axis = 5000

        yf_x_new = 2.0 / N * np.abs(yf_x[:N // 2])
        yf_x_float6 = []
        for index in range(len(yf_x_new)):
            yf_x_float6.append(round(yf_x_new[index], 6))

        xf_x_float6 = []
        for index in range(len(xf_x)):
            xf_x_float6.append(round(xf_x[index], 6))

        print(type(yf_x_float6), yf_x_float6)
        # print(type(xf_x_float6), xf_x_float6)

        plt.plot(xf_x_float6, yf_x_float6, label=files[i] + ("_X axis" if times + 1 == 1 else "_Y axis"))
        # plt.plot(xf_x, 2.0 / N * np.abs(yf_x[:N // 2]), label=result[i] + ("_X axis" if times + 1 == 1 else "_Y axis"))?
        # plt.plot(xf_y, 2.0/N * np.abs(yf_y[:N//2]), label=result[i] + "_Y")
        plt.xlabel("Frenquency (Hz)")
        plt.ylabel("Amplitude (g)")

        # print(xf_x[:10])
        # print(2.0 / N * np.abs(yf_x[:N // 2]))
        # np.savetxt('vibration_data\\001', test)
        with open("X_axis_FFT" if times + 1 == 1 else "Y_axis_FFT", 'w') as f:
            for idx in range(2500):
                f.write("%s,%s\n" % (xf_x_float6[idx], yf_x_float6[idx]))

    plt.legend()
    plt.show()
"""