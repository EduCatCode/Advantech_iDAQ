import sqlite3
import sys
from datetime import datetime
from CommonUtils import kbhit
from Automation.BDaq import *
from Automation.BDaq.WaveformAiCtrl import WaveformAiCtrl
from Automation.BDaq.BDaqApi import AdxEnumToString, BioFailed

# 創建數據庫和表
def create_database(channelCount):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
  
    # 創建一個包含所有通道的字段列表
    channels = [f"channel{i} REAL" for i in range(1, channelCount + 1)]
    channels_sql = ', '.join(channels)

    # 創建表的 SQL 命令
    sql_command = f"CREATE TABLE IF NOT EXISTS data (timestamp TEXT, {channels_sql})"
    c.execute(sql_command)
  
    conn.commit()
    conn.close()



# 將數據寫入數據庫
def save_data_to_db(data, channelCount):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    # 根據通道數量創建適當數量的佔位符
    placeholders = ', '.join(['?'] * (channelCount + 1))  # +1 是因為還有一個 timestamp 字段
    sql_command = f'INSERT INTO data VALUES ({placeholders})'

    c.executemany(sql_command, data)
    conn.commit()
    conn.close()


def AdvPollingStreamingAI(deviceDescription, startChannel, channelCount, sectionLength, sectionCount, clockRate, split_sec):
    USER_BUFFER_SIZE = channelCount * sectionLength
    profilePath = "DemoDevice.xml"
    ret = ErrorCode.Success
    
    wfAiCtrl = WaveformAiCtrl(deviceDescription)
    create_database()  # 創建數據庫和表

    for _ in range(1):
        wfAiCtrl.loadProfile = profilePath 
        wfAiCtrl.conversion.channelStart = startChannel
        wfAiCtrl.conversion.channelCount = channelCount
        wfAiCtrl.record.sectionCount = sectionCount
        wfAiCtrl.record.sectionLength = sectionLength
        wfAiCtrl.conversion.clockRate = clockRate 
        
        ret = wfAiCtrl.prepare()
        if BioFailed(ret):
            break

        ret = wfAiCtrl.start()
        if BioFailed(ret):
            break

        all_data = []

        try:
            start_time = datetime.now()
            row_count = 0
            print("Polling infinite acquisition is in progress, any key to quit!")
        
            while not kbhit():
                result = wfAiCtrl.getDataF64(USER_BUFFER_SIZE, -1)
                ret, returnedCount, data, = result[0], result[1], result[2]
                if BioFailed(ret):
                    break

                for i in range(0, returnedCount, channelCount):
                    row_data = [datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')]
                    for j in range(channelCount):
                        index = i + j
                        if index < len(data):
                            row_data.append(data[index])
                        else:
                            row_data.append(None)  # 如果數據不可用，添加 None

                    all_data.append(tuple(row_data))
                    row_count += 1

                # 每次擷取一定量的數據後，將其寫入數據庫
                if len(all_data) >= 1000:  # 假設每1000條數據寫入一次
                    save_data_to_db(all_data)
                    all_data = []

        except KeyboardInterrupt:
            save_data_to_db(all_data)  # 確保所有剩餘數據被寫入
            ret = wfAiCtrl.stop()
            end_time = datetime.now()
            elapsed_time = (end_time - start_time).total_seconds()
            sampling_rate = row_count / elapsed_time
            print(f"Elapsed Time: {elapsed_time} seconds")
            print(f"Sampling Rate: {sampling_rate} rows per second")

    wfAiCtrl.dispose()

    if BioFailed(ret):
        enumStr = AdxEnumToString("ErrorCode", ret.value, 256)
        print("Some error occurred. And the last error code is %#x. [%s]" % (ret.value, enumStr))
    return 0

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
