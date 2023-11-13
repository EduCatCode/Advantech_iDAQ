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

[研華科技驅動安裝與測試手冊](https://hackmd.io/pB_POm47Ska-MMRIPyNrFg?edit)

```bash
python PollingStreamingAI.py
```

在使用此程式時，您會被要求依序設定以下參數：

- **deviceDescription**：設備描述 (例如：`iDAQ-817,BID#65`)，可在Advantech IDE Navigator上查詢(如圖)。
  ![螢幕擷取畫面 2023-11-02 141240](https://github.com/EduCatCode/Advantech_iDAQ/assets/148319229/2d32888c-8894-475d-8ac2-e1b3072391b5)
- **startChannel**：起始通道 (例如：`0`)
- **channelCount**：通道數量 (例如：`5`)
- **sectionLength**：段落長度 (例如：`1024`)
- **sectionCount**：段落計數 (例如：`0`)
- **clockRate**: 取樣頻率(例如：`200000`)
- **split_sec**：分割秒數 (例如：`30`)

**終止程序**：使用 `Ctrl+C` 中斷程式。當程序中斷後，已儲存的CSV文件將依據您設定的時間區間進行分割。

## 3. RealTime_Monitor

**功能描述**：`RealTime_Monitor.py` 主要用於從CSV讀取數據並進行即時視覺化，從而達到即時監控的功能。

### 使用方法：

```bash
python RealTime_Monitor.py
```

1. 使用UI選擇CSV文件後，它將顯示視覺化的訊號圖表。
2. 提供三種視覺化界面：長條圖、散點圖和時間圖。
3. 您還可以使用提供的控制按鈕來暫停或終止視覺化過程。
   
## 4. 使用範例教學
本節將逐步指導使用者如何使用我們的系統來進行即時監測和資料視覺化。

### 步驟一: 啟動系統
監測需要同時運行數據擷取和視覺化兩個組件。請打開兩個終端機窗口以執行以下操作：

- **擷取訊號終端機：**
```bash
python PollingStreamingAI.py
```
- **視覺化介面終端機：**
```bash
python RealTime_Monitor.py
```
![image](https://github.com/EduCatCode/Advantech_iDAQ/assets/148319229/74558325-12f9-452d-a5db-3a41eca6b579)

### 步驟二：設定系統參數
按照終端機中的文字提示設定必要的運行參數。

![image](https://github.com/EduCatCode/Advantech_iDAQ/assets/148319229/fb03831d-1024-44d4-8763-1cc85468b133)

### 步驟三：選擇資料文件
在使用者介面中，選擇系統啟動時自動產生的CSV檔案進行分析。

![image](https://github.com/EduCatCode/Advantech_iDAQ/assets/148319229/6a29aa05-5ef2-401d-b7e1-327a9961d285)

### 步驟四：繪製數據圖表
選擇希望視覺化展示的數據特徵。

![image](https://github.com/EduCatCode/Advantech_iDAQ/assets/148319229/40877b8f-032f-4bcf-8cd7-2463f6146ba2)


請依照上述步驟進行操作，如果遇到任何疑問，歡迎隨時聯繫我。
### 步驟五：資料記錄與分段
系統將自動記錄時間戳記以便後續分析。使用者也可以根據需求，輸入特定時間區間以便將Excel檔案分割。

![image](https://github.com/EduCatCode/Advantech_iDAQ/assets/148319229/b142d788-a0b6-479a-88c7-9f959e3df521)


請依照上述步驟進行操作，如果遇到任何疑問，歡迎隨時聯繫我。
