# Advantech iDAQ 數據擷取與監控

此項目主要提供兩大功能：數據擷取以及即時監控。

## 1. 環境設定

為了設定必要的執行環境，請使用以下的 `conda` 命令：

```bash
conda env create -f iDAQ_environment.yml
```
## 2. PollingStreamingAI

**功能描述**：`PollingStreamingAI.py` 專為擷取訊號並將其儲存為CSV格式而設計。

### 設定參數

在使用此程式時，您會被要求依序設定以下參數：

- **deviceDescription**：設備描述 (例如：`iDAQ-817,BID#65`)
  ![螢幕擷取畫面 2023-11-02 141240](https://github.com/EduCatCode/Advantech_iDAQ/assets/148319229/2d32888c-8894-475d-8ac2-e1b3072391b5)
- **startChannel**：起始通道 (例如：`0`)
- **channelCount**：通道數量 (例如：`5`)
- **sectionLength**：段落長度 (例如：`1024`)
- **sectionCount**：段落計數 (例如：`0`)
- **split_sec**：分割秒數 (例如：`30`)

**終止程序**：使用 `Ctrl+C` 中斷程式。當程序中斷後，已儲存的CSV文件將依據您設定的時間區間進行分割。

## 3. RealTime_Monitor

**功能描述**：`RealTime_Monitor.py` 主要用於從CSV讀取數據並進行即時視覺化，從而達到即時監控的功能。

### 使用方法：

1. 使用UI選擇CSV文件後，它將顯示視覺化的訊號圖表。
2. 提供三種視覺化界面：長條圖、散點圖和時間圖。
3. 您還可以使用提供的控制按鈕來暫停或終止視覺化過程。
   
## 4. 實際使用畫面
- ** 因目前無設置取樣頻率功能，故終止程式時會顯示此次收集資料的頻率(資料筆數/秒數)
![image](https://github.com/EduCatCode/Advantech_iDAQ/assets/148319229/d770c189-9e17-4b93-a2d1-6e47694d23da)

