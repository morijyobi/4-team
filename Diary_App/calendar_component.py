import tkinter as tk
import datetime as dt
import calendar as cl

def calendar_component(master):
    frame = tk.Frame(master, bg="#EEEEE8", width=550, height=360)

    label1 = tk.Label(frame, font=("Meiryo UI", 20), anchor=tk.CENTER, width=2, bg="#EEEEE8")
    label1.place(x=20, y=3)

    label2 = tk.Label(frame, font=("Meiryo UI", 9), anchor=tk.W, width=10, bg="#EEEEE8")
    label2.place(x=70, y=8)

    label3 = tk.Label(frame, font=("Meiryo UI", 10), anchor=tk.W, width=10, bg="#EEEEE8")
    label3.place(x=70, y=25)

    labels = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    for i in range(7):
        tk.Label(frame, text=labels[i], font=("Meiryo UI", 8), anchor=tk.CENTER, width=8, bg="#EEEEE8")\
            .place(x=25 + 75 * i, y=40)

    btns = [""] * 42

    def btn_click():
        return

    for i in range(6):
        for j in range(7):
            fg = "#000000"
            if j == 0:
                bg = "#FFF0F0"
                fg = "#FF0000"
            elif j == 6:
                bg = "#F6F0FF"
                fg = "#0000A0"
            else:
                bg = "#FFFFFF"
            idx = j + 7 * i
            btns[idx] = tk.Button(frame, font=("Meiryo UI", 10), anchor=tk.NW, bg=bg, fg=fg,
                                  relief='flat', command=btn_click)
            btns[idx].place(x=15 + 75 * j, y=65 + 60 * i, width=70, height=50)

    cal_data = [""] * 42

    def generate_calendar(y, m):
        cal_data[:] = ["" for _ in range(42)]
        date_start = dt.date(y, m, 1)
        start_weekday = date_start.weekday()
        if start_weekday > 5:
            start_weekday -= 7
        max_day = cl.monthrange(y, m)[1]
        for i in range(max_day):
            cal_data[i + start_weekday + 1] = str(i + 1)

    def set_calendar():
        for i in range(42):
            btns[i]["text"] = cal_data[i]

    def change_month(offset):
        nonlocal year, month
        month += offset
        if month > 12:
            month = 1
            year += 1
        elif month < 1:
            month = 12
            year -= 1
        label1["text"] = str(month)
        label2["text"] = cl.month_name[month]
        label3["text"] = str(year)
        generate_calendar(year, month)
        set_calendar()

    now = dt.datetime.now()
    year, month, day = now.year, now.month, now.day
    generate_calendar(year, month)
    set_calendar()
    label1["text"] = str(month)
    label2["text"] = cl.month_name[month]
    label3["text"] = str(year)

    tk.Button(frame, text="prev", font=("Meiryo UI", 9), bg="#D0D0D0",
              relief='flat', command=lambda: change_month(-1)).place(x=420, y=5, width=50, height=25)
    tk.Button(frame, text="next", font=("Meiryo UI", 9), bg="#D0D0D0",
              relief='flat', command=lambda: change_month(1)).place(x=480, y=5, width=50, height=25)

    return frame
