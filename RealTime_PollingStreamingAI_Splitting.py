import os
import csv
from tqdm import tqdm
from Automation.BDaq import *
from datetime import datetime
from CommonUtils import kbhit
from typing import Any, List, Tuple
from Automation.BDaq.WaveformAiCtrl import WaveformAiCtrl
from Automation.BDaq.BDaqApi import AdxEnumToString, BioFailed
from Automation.BDaq.DeviceCtrl import DeviceCtrl
from Automation.BDaq import DeviceInformation, IepeType, CouplingType, AiSignalType

def list_all_supported_devices() -> List[str]:
    """
    List all supported devices and return their descriptions.

    Returns:
        List[str]: List of device descriptions.
    """
    device_ctrl = DeviceCtrl(None)
    descriptions = [device.Description for device in device_ctrl.installedDevices]

    print(f'Available Device count = {len(device_ctrl.installedDevices)}')
    for index, description in enumerate(descriptions):
        print(f'[{index}] {description}')

    return descriptions

def get_device_description_by_index(index: int, descriptions: List[str]) -> str:
    """
    Get device description by index.

    Args:
        index (int): The index of the device in the list.
        descriptions (List[str]): List of device descriptions.

    Returns:
        str: Device description corresponding to the index.
    """
    if 0 <= index < len(descriptions):
        return descriptions[index]
    else:
        raise ValueError("Invalid device index.")



def save_data_to_csv(data: List[List[Any]], filename: str) -> None:
    """
    Save given data to a CSV file.

    Args:
        data (List[List[Any]]): A list of rows, where each row is a list of data items.
        filename (str): The name of the file to save the data to.

    Returns:
        None
    """
    with open(filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(data)


def open_new_csv_file(formatted_date: str, channel_count: int) -> Tuple:
    """
    Opens a new CSV file for writing data.

    Args:
        formatted_date (str): The formatted date string to be used in the filename.
        channel_count (int): The number of channels to be recorded in the CSV file.

    Returns:
        Tuple: A tuple containing the opened file object and the CSV writer object.
    """
    
    file = open(formatted_date, "w", newline='')
    writer = csv.writer(file)
    columns = ['timestamp'] + [f'channel{i}' for i in range(channel_count)]
    writer.writerow(columns)

    return file, writer

def handle_csv_file_splitting(csv_file, current_time: datetime, channel_count: int, date_dir: str) -> Tuple:
    """
    Handles the splitting of the CSV file.

    Args:
        csv_file: The currently open CSV file.
        current_time (datetime): The current time.
        channel_count (int): The number of channels in the data.
        date_dir (str): The directory where the new CSV file should be saved.

    Returns:
        Tuple: A tuple containing the newly opened file object and the CSV writer object.
    """
    csv_file.close()
    formatted_date = current_time.strftime('%Y%m%d%H%M%S')
    csv_filename = os.path.join(date_dir, f"{formatted_date}.csv")
    return open_new_csv_file(csv_filename, channel_count)

def close_file(file) -> None:
    """
    Closes the given file.

    Args:
        file: The file to be closed.
    """
    if file is not None:
        file.close()

def stop_acquisition(wf_ai_ctrl, csv_file, start_time, row_count, all_data) -> None:
    """
    Stops the data acquisition.

    Args:
        wf_ai_ctrl: The waveform AI controller used for data acquisition.
    """
    close_file(csv_file)
    wf_ai_ctrl.stop()
    end_time = datetime.now()
    elapsed_time = (end_time - start_time).total_seconds()
    sampling_rate = row_count / elapsed_time
    print(f"Elapsed Time: {elapsed_time} seconds")
    print(f"Sampling Rate: {sampling_rate} rows per second")
    rows_per_file = int(split_sec * sampling_rate)  
    formatted_date = start_time.strftime('%Y%m%d%H%M%S')
    for i in range(0, len(all_data), rows_per_file):
        chunk = all_data[i:i+rows_per_file]
        filename = os.path.join(os.getcwd(), f'{formatted_date}({i // rows_per_file + 1}).csv')
        save_data_to_csv(chunk, filename)

def get_user_input(prompt: str, type_func = str) -> any:
    """
    Prompts the user for input and converts it to the specified type.

    Args:
    prompt (str): The prompt to display to the user.
    type_func (function): The function to convert the input to the desired type.

    Returns:
    any: The user input converted to the specified type.
    """
    while True:
        try:
            return type_func(input(prompt))
        except ValueError:
            print("Invalid input. Please try again.")


def device_data_acquisition(config):
    # Unpack device configuration
    device_description, start_channel, channel_count, section_length, section_count, clock_rate, split_sec, iepe = config

    # Call the adv_polling_streaming_ai function and pass it the unpacked arguments
    adv_polling_streaming_ai(device_description, start_channel, channel_count, section_length, section_count, clock_rate, split_sec, iepe)




def adv_polling_streaming_ai(device_description: str, start_channel: int, channel_count: int, 
                             section_length: int, section_count: int, clock_rate: int, 
                             split_sec: int, iepe: bool) -> None:
    """
    Advanced polling streaming AI.

    Args:
    device_description (str): Description of the device.
    start_channel (int): Starting channel number.
    channel_count (int): Number of channels.
    section_length (int): Length of each section.
    section_count (int): Number of sections.
    clock_rate (int): Clock rate.
    split_sec (int): Time in seconds to split the data.
    iepe (bool): IEPE status.
    """

    user_buffer_size = channel_count * section_length
    ret = ErrorCode.Success

    base_dir = os.path.join(os.getcwd(), device_description)
    os.makedirs(base_dir, exist_ok=True)

    # 創建以當前日期為名的子目錄
    date_str = datetime.now().strftime('%Y%m%d')
    date_dir = os.path.join(base_dir, f"{date_str}_1")
    counter = 2
    while os.path.exists(date_dir):
        # 如果當天目錄已存在，則創建帶編號的新目錄
        date_dir = os.path.join(base_dir, f"{date_str}_{counter}")
        counter += 1

    os.makedirs(date_dir, exist_ok=True)

    # Initialize variables
    csv_file = None
    start_time = datetime.now()
    row_count = 0
    
    # Step 1: Create a 'WaveformAiCtrl' for caching
    wf_ai_ctrl = WaveformAiCtrl(device_description)


    for _ in range(1):
        # 步驟2：傳入必要的參數(裝置名稱、開始頻道、頻道數量、緩存大小、緩存數量、取樣率)
        wf_ai_ctrl.conversion.channelStart = start_channel
        wf_ai_ctrl.conversion.channelCount = channel_count
        wf_ai_ctrl.record.sectionCount = section_count
        wf_ai_ctrl.record.sectionLength = section_length
        wf_ai_ctrl.conversion.clockRate = clock_rate

        # 設定IEPE (IEPE打開 需要設定連接類型:偽差分 耦合:交流耦合 壓電集成電路:2mA )
        iepe_type = IepeType(3 if iepe else 0)
        coupling_type = CouplingType(1 if iepe else 0)
        signal_type = AiSignalType(2 if iepe else 1)

        wf_ai_ctrl.selectedDevice = DeviceInformation(device_description)
        channel_names = [str(channel.logicalNumber) for channel in wf_ai_ctrl.channels]

        for channel_name in channel_names:
            channel = wf_ai_ctrl.channels[int(channel_name)]
            channel.iepeType = iepe_type
            channel.couplingType = coupling_type
            channel.signalType = signal_type

        # 步驟3：開始操作
        ret = wf_ai_ctrl.prepare()
        if BioFailed(ret):
            break

        ret = wf_ai_ctrl.start()
        if BioFailed(ret):
            break

        all_data = []

        try:
            now = datetime.now()
            file_start_time = now
            formatted_date = now.strftime('%Y%m%d%H%M%S') 
            csv_filename = os.path.join(date_dir, f"{formatted_date}.csv")
            csv_file, csv_writer = open_new_csv_file(csv_filename, channel_count)
            print("Polling infinite acquisition is in progress, any key to quit!")
    
            # Initialize progress bar
            pbar = tqdm(total=split_sec, desc="Retrieval progress", leave=True)

            while not kbhit():
                result = wf_ai_ctrl.getDataF64(user_buffer_size, -1)
                ret, returned_count, data = result[0], result[1], result[2]
                if BioFailed(ret):
                    break

                # 更新進度條
                elapsed_time = (datetime.now() - file_start_time).total_seconds()
                pbar.update(elapsed_time - pbar.n)

                for i in range(0, returned_count, channel_count):
                    current_time = datetime.now()
                    row_data = [current_time.strftime('%Y-%m-%d %H:%M:%S.%f')] + data[i:i+channel_count]
                    csv_writer.writerow(row_data)
                    row_count += channel_count

                    if (current_time - file_start_time).total_seconds() >= split_sec:
                        csv_file, csv_writer = handle_csv_file_splitting(csv_file, current_time, channel_count, date_dir)

                        # 重置進度條
                        pbar.reset()
    
                        file_start_time = current_time
                        formatted_date = current_time.strftime('%Y%m%d%H%M%S')
                        csv_filename = os.path.join(date_dir, f"{formatted_date}.csv")
                        csv_file, csv_writer = open_new_csv_file(csv_filename, channel_count)

        except KeyboardInterrupt:
            stop_acquisition(wf_ai_ctrl, start_time, row_count, all_data)

        finally:
            pbar.close()
            close_file(csv_file)

    # Step 7: Shut down the device and release all allocated resources
    wf_ai_ctrl.dispose()

    # If a problem occurs during execution, print the error code on the screen for tracking
    if BioFailed(ret):
        enumStr = AdxEnumToString("ErrorCode", ret.value, 256)
        print("Some error occurred. And the last error code is %#x. [%s]" % (ret.value, enumStr))
    return 0

# Single device use

if __name__ == '__main__':
    
    # User input parameters
    descriptions = list_all_supported_devices()
    device_index = get_user_input('Please select device by index (e.g., 0 for the first device):\n', int)
    device_description = get_device_description_by_index(device_index, descriptions)
    start_channel = get_user_input('Please set startChannel (Ex: 0):\n', int)
    channel_count = get_user_input('Please set channelCount (Ex: 5):\n', int)
    section_length = get_user_input('Please set sectionLength (Ex: 1024):\n', int)
    section_count = get_user_input('Please set sectionCount (Ex: 0):\n', int)
    clock_rate = get_user_input('Please set clockRate (Ex: 200000):\n', int)
    split_sec = get_user_input('Please set split_sec (Ex: 30):\n', int)
    iepe_input = get_user_input('Please set iepe (True or False):\n')
    iepe = iepe_input.lower() in ['true', '1', 'yes', 'y', 't', 'T', 'True', 'TRUE', 'YES', 'Yes']

    # Call function
    adv_polling_streaming_ai(device_description, start_channel, channel_count, section_length, section_count, clock_rate, split_sec, iepe)
