import tkinter as tk
from tkinter import ttk
import os

active_log = ""

def save_data (active_log, text_input):
    print(active_log, text_input)

def create_new_log(root, option, date, entry):
    date_file_path = os.path.join("data", "combat_logs", date, option, entry + ".txt")
    try:
        with open(date_file_path, 'x') as f:
            pass
    except FileExistsError:
        return "File already exists"
    global active_log
    active_log = date_file_path
    load_log(active_log)
    root.destroy()

def open_new_log():
    log_popout = tk.Toplevel(root)
    log_popout.overrideredirect(True)
    log_popout.geometry("300x300-50+50")

    popout_frame = tk.Frame(log_popout, width=300, height=300)
    popout_frame.config(bg="#343c45")
    popout_frame.grid(row = 0, column = 0, sticky = "NEWS")
    popout_frame.grid_rowconfigure(0, weight = 1)
    popout_frame.grid_columnconfigure(0, weight = 1)
    
    campaign_file_path = os.path.join("data", "campaigns", "campaigns.txt")
    CAMPAIGNS = create_list_from_txt(campaign_file_path)

    campaign_var = tk.StringVar(popout_frame)
    campaign_var.set("Select a Campaign")
    campaign_option = tk.OptionMenu(popout_frame, campaign_var, *CAMPAIGNS)
    campaign_option.config(width=20, height=3, justify="center")
    campaign_option.grid(row = 0, column = 0, padx=(70,70), pady=(10,0))

    date_file_path = os.path.join("data", "combat_logs")
    DATE_OPTIONS = os.listdir(date_file_path)
    
    date_var = tk.StringVar(popout_frame)
    date_var.set("Select a Month")
    date_option = tk.OptionMenu(popout_frame, date_var, *DATE_OPTIONS)
    date_option.config(width=20, height=3, justify="center")
    date_option.grid(row = 1, column = 0, padx=(70,70), pady=(10,0))

    date_label = tk.Label(popout_frame, justify="center", text="Enter the Date:")
    date_label.grid(row = 2, column = 0, padx=(70,70), pady=(10,0))

    date_entry = tk.Entry(popout_frame, justify="center", width=20)
    date_entry.grid(row = 3, column = 0, padx=(70,70), pady=(10,0))

    submit_button = tk.Button(popout_frame, command = lambda: create_new_log(log_popout, campaign_var.get(), date_var.get(), date_entry.get()), width=10, height=2, text="Submit", font=("Times New Roman", 20))
    submit_button.grid(row = 4, column = 0, padx=(70,70), pady=(10,10))

def create_list_from_txt(file_path):
    output_list = []
    try:
        with open(file_path, 'r') as f:
            output_list = [line.rstrip('\n') for line in f.readlines()]
        return output_list
    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return f"An error occured: {e}"

def load_log(log):
    print("actually load the log")

def display_in_columns(canvas, data, num_columns=3):
    if not data:
        return

    text_x = canvas.config("width") // 2
    max_len = max(len(item) for item in data)
    terminal_width = 80
    col_width = max(max_len + 2, terminal_width // num_columns)

    for i in range(0, len(data), num_columns):
        row = data[i:i + num_columns]
        formatted_row = "".join(item.ljust(col_width) for item in row)
        print(formatted_row)

root = tk.Tk()
root.title("Runaria")
root.state("zoomed")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

root_frame = tk.Frame(root, width=200, height=200)
root_frame.config(bg="red")
root_frame.grid(row = 0, column = 0, sticky = "NEWS")
root_frame.grid_rowconfigure(0, weight=0)
root_frame.grid_columnconfigure(0, weight=0)
root_frame.grid_rowconfigure(1, weight=1)
root_frame.grid_columnconfigure(1, weight=1)

button_frame = tk.Frame(root_frame, width=1000, height=200)
button_frame.config(bg="yellow")
button_frame.grid(row = 0, column = 0, columnspan = 2, sticky = "NEW")
button_frame.grid_rowconfigure(0, weight=1)
button_frame.grid_columnconfigure(0, weight=1)

text_frame = tk.Frame(root_frame, width=550, height=200)
text_frame.config(bg="blue")
text_frame.grid(row = 1, column = 0, sticky="NEWS")
text_frame.grid_rowconfigure(0, weight=0)
text_frame.grid_columnconfigure(0, weight=0)
text_frame.grid_rowconfigure(5, weight=1)

log_frame = tk.Frame(root_frame, width=800, height=200)
log_frame.config(bg="green")
log_frame.grid(row = 1, column = 1, sticky="NEWS")
log_frame.grid_rowconfigure(0, weight=1)
log_frame.grid_columnconfigure(0, weight=1)

text_box = tk.Text(text_frame, width=40, height=20, font=("Times New Roman", 15))
text_box.config(bg="orange")
text_box.grid(row = 4, column = 0, padx=(25,25), pady=(10,10))

player_label = tk.Label(text_frame, text="Wrap {  } for player", font = ("Times New Roman", 20))
player_label.grid(row = 0, column = 0, padx=(25,25), pady=(25,0))
item_label = tk.Label(text_frame, text="Wrap [  ] for item", font = ("Times New Roman", 20))
item_label.grid(row = 1, column = 0, padx=(25,25))
damage_label = tk.Label(text_frame, text="Wrap (  ) for damage", font = ("Times New Roman", 20))
damage_label.grid(row = 2, column = 0, padx=(25,25))
target_label = tk.Label(text_frame, text="Wrap {(  )} for target", font = ("Times New Roman", 20))
target_label.grid(row = 3, column = 0, padx=(25,25))

save_button = tk.Button(text_frame, command =  lambda: save_data(active_log, text_box.get("1.0", "end")), width=30, height=3, text="Save", font=("Times New Roman", 20))
save_button.grid(row = 5, column = 0, padx=(25,25))

log_canvas = tk.Canvas(log_frame, width=500, height=300)
log_canvas.grid(row = 0, column = 0, padx=(25,25), pady=(25,25), sticky = "NEWS")

new_log_button = tk.Button(button_frame, command = lambda: open_new_log(), width = 5, height = 2, text="+", font=("Times New Roman", 20, "bold"))
new_log_button.grid(row = 0, column = 1)

root.mainloop()