import sys
import csv
sys.path.append('..')
import datetime
from datetime import datetime
from CommonUtils import kbhit
from Automation.BDaq import *
from Automation.BDaq.WaveformAiCtrl import WaveformAiCtrl
from Automation.BDaq.BDaqApi import AdxEnumToString, BioFailed

def save_data_to_csv(data, filename):
    with open(filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(data)

def AdvPollingStreamingAI(deviceDescription, startChannel, channelCount, sectionLength, sectionCount, split_sec):
    USER_BUFFER_SIZE = channelCount * sectionLength
    profilePath = "DemoDevice.xml"
    ret = ErrorCode.Success
    
    # 步驟1：創建一個'WaveformAiCtrl'用於暫存功能
    wfAiCtrl = WaveformAiCtrl(deviceDescription)

    for _ in range(1):

        # 載入配置文件以初始化設備
        wfAiCtrl.loadProfile = profilePath 

        # 步驟2：設置必要的參數
        wfAiCtrl.conversion.channelStart = startChannel
        wfAiCtrl.conversion.channelCount = channelCount
        wfAiCtrl.record.sectionCount = sectionCount
        wfAiCtrl.record.sectionLength = sectionLength
        
        # 步驟3：開始操作
        ret = wfAiCtrl.prepare()
        if BioFailed(ret):
            break

        ret = wfAiCtrl.start()
        if BioFailed(ret):
            break

        all_data = []

        try:
            # 獲取當前的日期和時間
            now = datetime.now()
            formatted_date = now.strftime('%Y%m%d%H%M%S') 
            csv_file = open(f"{formatted_date}.csv", "w", newline='')
            csv_writer = csv.writer(csv_file)

            # 生成列名並寫入CSV
            columns = ['timestamp'] + [f'channel{i}' for i in range(channelCount)]
            csv_writer.writerow(columns)

            start_time = datetime.now()
            row_count = 0

            # 步驟4：設備以輪詢方式採集數據
            print("Polling infinite acquisition is in progress, any key to quit!")
        
            while not kbhit():
                result = wfAiCtrl.getDataF64(USER_BUFFER_SIZE, -1)
                ret, returnedCount, data, = result[0], result[1], result[2]
                if BioFailed(ret):
                    break

                print("Polling Stream AI get data count is %d" % returnedCount)
                if returnedCount > 0:
                    print("the first sample for each channel are:")
                for i in range(channelCount):
                    if i < len(data):
                        print("channel %d: %10.6f" % (i + startChannel, data[i]))
                    else:
                        print(f"channel {i + startChannel}: Data not available")

                for i in range(0, returnedCount, channelCount):
                    row_data = [datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')]  # 加入當前時間戳記
                    for j in range(channelCount):
                        index = i + j
                        if index < len(data):
                            row_data.append(data[index])
                        else:
                            pass
                            
                    all_data.append(row_data)
                    csv_writer.writerow(row_data)
                    row_count += 1

        except KeyboardInterrupt:
            # 步驟6：如果正在運作則停止操作
            ret = wfAiCtrl.stop()
            end_time = datetime.now()
            elapsed_time = (end_time - start_time).total_seconds()
            sampling_rate = row_count / elapsed_time
            print(f"Elapsed Time: {elapsed_time} seconds")
            print(f"Sampling Rate: {sampling_rate} rows per second")
            rows_per_file = int(split_sec * sampling_rate)  # 計算每個文件的行數
            formatted_date = start_time.strftime('%Y%m%d%H%M%S')
            for i in range(0, len(all_data), rows_per_file):
                chunk = all_data[i:i+rows_per_file]
                save_data_to_csv(chunk, f'{formatted_date}({i // rows_per_file + 1}).csv')

    # 步驟 7: 關閉設備，釋放所有分配的資源
    wfAiCtrl.dispose()

        # 如果執行中出現問題，將錯誤代碼列印在螢幕上以便跟踪
    if BioFailed(ret):
        enumStr = AdxEnumToString("ErrorCode", ret.value, 256)
        print("Some error occurred. And the last error code is %#x. [%s]" % (ret.value, enumStr))
    return 0

# 在主函數或程式的適當位置
if __name__ == '__main__':
    print ('Please set the necessary parameters in order')
    print ('Please set deviceDescription parameters')
    deviceDescription = str(input('deviceDescription(Ex: iDAQ-817,BID#65):\n'))

    print ('Please set deviceDescription parameters')
    startChannel = int(input('startChannel(Ex: 0):\n'))

    print ('Please set channelCount parameters:')
    channelCount = int(input('channelCount(Ex: 5):\n'))

    print ('Please set sectionLength parameters:')
    sectionLength = int(input('sectionLength(Ex: 1024):\n'))

    print ('Please set sectionCount parameters:')
    sectionCount = int(input('sectionCount(Ex: 0):\n'))

    print ('Please set split_sec parameters:')
    split_sec = int(input('split_sec(Ex: 30):\n'))

    AdvPollingStreamingAI(deviceDescription, startChannel, channelCount, sectionLength, sectionCount, split_sec)

