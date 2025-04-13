import tkinter as tk
from tkinter import ttk

def save_data (text_input):
    print(text_input)

def open_new_log():
    print("new log")

def load_log(log):
    print("actually load the log")

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

text_box = tk.Text(text_frame, width=50, height=30)
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

save_button = tk.Button(text_frame, command =  lambda: save_data(text_box.get("1.0", "end")), width=30, height=3, text="Save", font=("Times New Roman", 20))
save_button.grid(row = 5, column = 0, padx=(25,25))

log_canvas = tk.Canvas(log_frame, width=500, height=300)
log_canvas.config(bg="green")
log_canvas.grid(row = 0, column = 0, padx=(25,25), pady=(25,25))

new_log_button = tk.Button(button_frame, command = lambda: open_new_log(), width = 5, height = 2, text="+", font=("Times New Roman", 20, "bold"))
new_log_button.grid(row = 0, column = 1)

root.mainloop()