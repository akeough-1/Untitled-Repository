import tkinter as tk
from tkinter import ttk

def toggle_frame():
    state = 'normal' if checkbox_var.get() else 'disabled'
    for child in frame.winfo_children():
        child.configure(state=state)

root = tk.Tk()
root.title("Enable Frame with Checkbox")

checkbox_var = tk.BooleanVar()

# Checkbox to enable/disable the frame
checkbox = ttk.Checkbutton(root, text="Enable Options", variable=checkbox_var, command=toggle_frame)
checkbox.pack(pady=10)

# Frame with some widgets
frame = ttk.Frame(root, padding=10, relief="sunken")
frame.pack(padx=10, pady=10)

ttk.Label(frame, text="Option 1:").pack(anchor='w')
ttk.Entry(frame,state='disabled').pack(fill='x')
ttk.Label(frame, text="Option 2:").pack(anchor='w')
ttk.Entry(frame).pack(fill='x')
tk.Listbox(frame,bg="#f0f0f0",fg="#a3a3a3").pack(fill='x')

# Initially disable the frame's widgets
toggle_frame()

root.mainloop()
