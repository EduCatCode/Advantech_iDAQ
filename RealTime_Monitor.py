
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import Tk, Button, filedialog, Frame, IntVar, Checkbutton
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_graph():
    global file_path
    global is_paused
    is_paused = False
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    update_graph()

def toggle_pause():
    global is_paused
    is_paused = not is_paused

def stop_graph():
    window.quit()

def update_graph():
    global file_path
    if is_paused:
        window.after(500, update_graph)
        return

    if not file_path:
        return

    df = pd.read_csv(file_path)

    if df.shape[0] < 1:
        print("CSV file must have at least one row.")
        return

    df = df.tail(50).reset_index(drop=True)
    ax.clear()
    sns.set_theme(style="whitegrid")

    # Rename columns to 'channelX'
    df.columns = ['channel{}'.format(i) for i in range(df.shape[1])]

    # Plotting all columns
    for col in df.columns:
        if plot_type.get() == 1:
            sns.lineplot(x=df.index, y=df[col], ax=ax, label=col)
        elif plot_type.get() == 2:
            sns.scatterplot(x=df.index, y=df[col], ax=ax, label=col)
        elif plot_type.get() == 3:
            sns.barplot(x=df.index, y=df[col], ax=ax, label=col)

    ax.set_xlabel('Time Step')
    ax.set_ylabel('Value')
    ax.legend(loc='center right', bbox_to_anchor=(1.25, 0.5))
    fig.tight_layout()
    canvas.draw()
    window.after(1000, update_graph)


window = Tk()
window.title("CSV Realtime Plotter")

file_path = ""
is_paused = False


fig, ax = plt.subplots(figsize=(10, 5))  
canvas = FigureCanvasTkAgg(fig, master=window)

canvas.get_tk_widget().pack(side="top", fill="both", expand=True, padx=20, pady=20)

button_frame = Frame(window)
button_frame.pack(padx=20, pady=20)

plot_button = Button(button_frame, text="Select CSV and Plot", command=plot_graph)
plot_button.grid(row=0, column=0, padx=5, pady=5)

pause_button = Button(button_frame, text="Pause/Resume", command=toggle_pause)
pause_button.grid(row=0, column=1, padx=5, pady=5)

stop_button = Button(button_frame, text="Stop and Close", command=stop_graph)
stop_button.grid(row=0, column=2, padx=5, pady=5)

plot_type = IntVar()

line_check = Checkbutton(button_frame, text="Line Plot", variable=plot_type, onvalue=1)
line_check.grid(row=0, column=3, padx=5, pady=5)

scatter_check = Checkbutton(button_frame, text="Scatter Plot", variable=plot_type, onvalue=2)
scatter_check.grid(row=0, column=4, padx=5, pady=5)

hist_check = Checkbutton(button_frame, text="Histogram", variable=plot_type, onvalue=3)
hist_check.grid(row=0, column=5, padx=5, pady=5)

window.mainloop()

