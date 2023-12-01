import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from tkinter import Tk, Button, filedialog, Frame, IntVar, Checkbutton, Label
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def clear_checks():
    global check_vars, channel_checks, value_labels
    for check in channel_checks:
        check.destroy()  # 移除舊的Checkbuttons
    for label in value_labels.values():
        label.destroy()  # 移除舊的數值標籤
    check_vars = []  # 清空變數列表
    channel_checks = []  # 清空Checkbutton列表
    value_labels = {}  # 清空數值標籤字典

def plot_graph():
    global dir_path, is_paused, check_vars, channel_checks, value_labels
    is_paused = False
    dir_path = filedialog.askdirectory()  # 讓使用者選擇 CSV 文件的資料夾
    if not dir_path:
        return

    update_graph()

    if 'df' not in globals() or df is None or df.empty:
        print("Failed to load data.")
        return

    clear_checks()

    if 'timestamp' in df.columns:
        df.drop(columns='timestamp', inplace=True)

    max_columns = 3
    for i, column_name in enumerate(df.columns):
        var = IntVar(value=1)
        check = Checkbutton(button_frame, text=column_name, variable=var)
        label = Label(button_frame, text=f'{column_name}: N/A')
        row = i // max_columns + 1
        column = i % max_columns
        check.grid(row=row, column=column*2, padx=5, pady=5)
        label.grid(row=row, column=column*2+1, padx=5, pady=5)
        check_vars.append(var)
        channel_checks.append(check)
        value_labels[column_name] = label

    update_graph()

def update_graph():
    global dir_path, check_vars, value_labels, df
    if is_paused or not dir_path:
        window.after(500, update_graph)
        return

    all_files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith('.csv')]
    if not all_files:
        print("No CSV files found in the directory.")
        window.after(500, update_graph)
        return

    all_files.sort(key=os.path.getmtime)
    latest_file = all_files[-1]  # 取最新的文件
    print(f"Attempting to load data from {latest_file}")  # 讀取的文件名

    try:
        df = pd.read_csv(latest_file)
        print(f"Successfully loaded data from {latest_file}")
    except Exception as e:
        print(f"Error loading data from {latest_file}: {e}")
        df = None
        window.after(500, update_graph)
        return

    if df.empty:
        print(f"No data in file: {latest_file}")
        df = None
        window.after(500, update_graph)
        return


    if df.shape[0] < 1:
        print("CSV file must have at least one row.")
        return

    df = df.tail(10000).reset_index(drop=True)  
    ax.clear()
    sns.set_theme(style="whitegrid")
      
    if 'timestamp' in df.columns:
        df = df.drop(columns='timestamp')

    for i, (column_name, data) in enumerate(df.items()):
        if i < len(check_vars) and check_vars[i].get() == 1:
            if pd.api.types.is_numeric_dtype(data):
                sns.lineplot(x=df.index, y=data, ax=ax, label=column_name)
                value_labels[column_name].config(text=f'{column_name}: {data.iloc[-1]:.4f}')
            else:
                print(f"Warning: The column '{column_name}' contains non-numeric data and cannot be plotted.")
    
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Value')
    ax.legend(loc='center right', bbox_to_anchor=(1.25, 0.5))
    fig.tight_layout()
    canvas.draw()
    window.after(1000, update_graph)

def toggle_pause():
    global is_paused
    is_paused = not is_paused

def stop_graph():
    window.quit()

# Tkinter視窗和配置
window = Tk()
window.title("Real-Time Machine Monitoring System")
window.geometry('')  # 空字符串將允許窗口根據內容自動調整大小
window.iconbitmap('EduCatCode.ico')

# 初始化全局變數
file_path = ""
is_paused = False
check_vars = []  # 儲存Checkbutton的變量
channel_checks = []  # 儲存Checkbutton的對象
value_labels = {}  # 儲存數值標籤的字典

# 創建Matplotlib圖表和布局
fig, ax = plt.subplots(figsize=(10, 5))
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack(side="top", fill="both", expand=True, padx=20, pady=20)

button_frame = Frame(window)
button_frame.pack(padx=20, pady=20)

# 創建按鈕
plot_button = Button(button_frame, text="Select CSV and Plot", command=plot_graph)
plot_button.grid(row=0, column=1, padx=5, pady=5)

pause_button = Button(button_frame, text="Pause/Resume", command=toggle_pause)
pause_button.grid(row=0, column=3, padx=5, pady=5)

stop_button = Button(button_frame, text="Stop and Close", command=stop_graph)
stop_button.grid(row=0, column=5, padx=5, pady=5)

window.mainloop()
