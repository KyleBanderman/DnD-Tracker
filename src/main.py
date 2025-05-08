import tkinter as tk
from tkinter import ttk
import os
import datetime
from tkcalendar import DateEntry

active_log = ""

def focus_out_window(event):
    if event.widget is root:
        root.destroy()

def remove_chars(text, chars_to_remove):
    return ''.join(char for char in text if char not in chars_to_remove)

def get_name_of_month(month_number):
    if month_number < 1 or month_number > 12:
        return "Invalid Number"
    
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    return months[month_number - 1]

def save_log (active_log, text_input):
    lines = text_input.splitlines()
    try:
        with open(active_log, "a") as f:
            f.writelines(line + "\n" for line in lines)
        print(f"Data Saved at {active_log}")
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print(f"An error has occured: {e}")

def load_log(log):
    print(f"actually load the {log}")

def create_new_log(root, option, entry):
    date = datetime.date.today()
    month = get_name_of_month(date.month)
    formatted_date = f"{date.month}-{date.day}"
    date_file_path = os.path.join("data", "combat_logs", option, str(date.year), month, formatted_date, entry + ".txt")
    try:
        os.mkdir(os.path.dirname(date_file_path))
    except FileExistsError:
        pass
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
    log_popout.geometry("300x300-70+50")
    log_popout.bind("<FocusOut>", focus_out_window)
    log_popout.focus_set()

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

    date_label = tk.Label(popout_frame, justify="center", text="Enter the Name:")
    date_label.grid(row = 2, column = 0, padx=(70,70), pady=(10,0))

    date_entry = tk.Entry(popout_frame, justify="center", width=20)
    date_entry.grid(row = 3, column = 0, padx=(70,70), pady=(10,0))

    submit_button = tk.Button(popout_frame, command = lambda: create_new_log(log_popout, campaign_var.get(), date_entry.get()), width=10, height=2, text="Submit", font=("Times New Roman", 20))
    submit_button.grid(row = 4, column = 0, padx=(70,70), pady=(10,10))

def select_log():
    select_popout = tk.Toplevel(root)
    select_popout.overrideredirect(True)
    select_popout.geometry("300x300-70+50")
    select_popout.bind("<FocusOut>", focus_out_window)
    select_popout.focus_set()

    popout_frame = tk.Frame(select_popout, width=300, height=300)
    popout_frame.config(bg="#343c45")
    popout_frame.grid(row = 0, column = 0, sticky = "NEWS")
    popout_frame.grid_rowconfigure(0, weight = 1)
    popout_frame.grid_columnconfigure(0, weight = 1)

    calendar = DateEntry(popout_frame, date_pattern = "m-d-y", width=12, bg='darkblue', fg='white', borderwidth=2, font=("Times New Roman", 12))
    calendar.grid(row = 0, column = 0, sticky="N")

    campaign_file_path = os.path.join("data", "campaigns", "campaigns.txt")
    CAMPAIGNS = create_list_from_txt(campaign_file_path)

    campaign_var = tk.StringVar(popout_frame)
    campaign_var.set("Select a Campaign")
    campaign_option = tk.OptionMenu(popout_frame, campaign_var, *CAMPAIGNS)
    campaign_option.config(width=20, height=3, justify="center")
    campaign_option.grid(row = 1, column = 0, padx=(70,70), pady=(10,0))

    data_collect_button = tk.Button(popout_frame, command = lambda: process_selects(popout_frame, calendar.get_date(), campaign_var.get()), width = 10, height = 3, text="Submit")
    data_collect_button.grid(row = 2, column = 0)

def process_selects(root, date, entry):
    formatted_date = remove_chars(date.strftime("%m-%d"), "0")
    year = date.strftime("%Y")
    month_number = remove_chars(date.strftime("%m"), "0")
    month = get_name_of_month(int(month_number))
    file_path = os.path.join("data", "combat_logs", entry, year, month, formatted_date)
    
    option_var = tk.StringVar(root)
    OPTIONS = os.listdir(file_path)
    process_option = tk.OptionMenu(root, option_var, *OPTIONS)
    process_option.config(width=20, height=3, justify="center")
    process_option.grid(row = 3, column = 0, padx=(70,70), pady=(10,10))

    process_button = tk.Button(root, command = lambda: process_option_select(file_path, option_var.get()))
    process_button.grid(row = 4, column = 0, padx=(70,70), pady=(10,10))

def process_option_select(file_path, option):
    new_final_path = os.path.join(file_path, option)
    global active_log
    active_log = new_final_path

    read_log(log_canvas, active_log)

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

def read_log(canvas, log):
    content = ""
    try:
        with open(log, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        return "File not found"
    
    canvas.create_text(100, 50, text=content, font=("Times New Roman", 12))

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

save_button = tk.Button(text_frame, command =  lambda: save_log(active_log, text_box.get("1.0", "end-1c")), width=30, height=3, text="Save", font=("Times New Roman", 20))
save_button.grid(row = 5, column = 0, padx=(25,25))

log_canvas = tk.Canvas(log_frame, width=500, height=300)
log_canvas.grid(row = 0, column = 0, padx=(25,25), pady=(25,25), sticky = "NEWS")


new_log_button = tk.Button(button_frame, command = lambda: open_new_log(), width = 5, height = 2, text="+", font=("Times New Roman", 20, "bold"))
new_log_button.grid(row = 0, column = 1)

select_log_button = tk.Button(button_frame, command = lambda: select_log(), width = 5, height = 2, text="★", font=("Times New Roman", 20, "bold"))
select_log_button.grid(row = 0, column = 2)

"∘"

root.mainloop()