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

def AdvPollingStreamingAI(deviceDescription, startChannel, channelCount, sectionLength, sectionCount, clockRate, split_sec):

    USER_BUFFER_SIZE = channelCount * sectionLength
    profilePath = "DemoDevice.xml"
    ret = ErrorCode.Success
    
    csv_file = None  # 初始化 csv_file 變數
    start_time = datetime.now()  # 初始化 start_time
    row_count = 0  # 初始化 row_count
    
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
        wfAiCtrl.conversion.clockRate = clockRate 
        
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
            file_start_time = now  # 記錄檔案開始時間
            formatted_date = now.strftime('%Y%m%d%H%M%S') 
            csv_file = open(f"{formatted_date}.csv", "w", newline='')
            csv_writer = csv.writer(csv_file)

            # 生成特徵名並寫入CSV
            columns = ['timestamp'] + [f'channel{i}' for i in range(channelCount)]
            csv_writer.writerow(columns)


            # 步驟4：設備以輪詢方式採集數據
            print("Polling infinite acquisition is in progress, any key to quit!")
        
            while not kbhit():
                result = wfAiCtrl.getDataF64(USER_BUFFER_SIZE, -1)
                ret, returnedCount, data, = result[0], result[1], result[2]
                if BioFailed(ret):
                    break

                for i in range(0, returnedCount, channelCount):
                    current_time = datetime.now()
                    row_data = [current_time.strftime('%Y-%m-%d %H:%M:%S.%f')]
                    for j in range(channelCount):
                        index = i + j
                        if index < len(data):
                            row_data.append(data[index])

                    csv_writer.writerow(row_data)
                    row_count += channelCount

                    # 檢查是否達到split_sec，如果是，則關閉當前檔案並開啟新檔案
                    if (current_time - file_start_time).total_seconds() >= split_sec:
                        csv_file.close()
                        file_start_time = current_time
                        formatted_date = current_time.strftime('%Y%m%d%H%M%S')
                        csv_file = open(f"{formatted_date}.csv", "w", newline='')
                        csv_writer = csv.writer(csv_file)
                        csv_writer.writerow(columns)

        except KeyboardInterrupt:
            if csv_file:
                csv_file.close()  # 確保關閉文件
            
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
        
        finally:
            if csv_file:
                csv_file.close()  # 再次確保關閉文件




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

    print ('Please set clockRate parameters:')
    clockRate = int(input('clockRate(Ex: 200000):\n'))
    
    print ('Please set split_sec parameters:')
    split_sec = int(input('split_sec(Ex: 30):\n'))

    AdvPollingStreamingAI(deviceDescription, startChannel, channelCount, sectionLength, sectionCount, clockRate, split_sec)

