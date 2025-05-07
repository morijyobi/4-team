import tkinter as tk
import datetime as dt
import calendar as cl

class CalendarComponent(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#EEEEE8", width=550, height=360)

        self.selected_date = dt.date.today()
        

        self.label1 = tk.Label(self, font=("Meiryo UI", 20), anchor=tk.CENTER, width=2, bg="#EEEEE8")
        self.label1.place(x=20, y=3)

        self.label2 = tk.Label(self, font=("Meiryo UI", 9), anchor=tk.W, width=10, bg="#EEEEE8")
        self.label2.place(x=70, y=18)

        self.label3 = tk.Label(self, font=("Meiryo UI", 10), anchor=tk.W, width=10, bg="#EEEEE8")
        self.label3.place(x=100, y=18)

        labels = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        for i in range(7):
            tk.Label(self, text=labels[i], font=("Meiryo UI", 8), anchor=tk.CENTER, width=8, bg="#EEEEE8")\
                .place(x=25 + 75 * i, y=40)

        self.btns = [""] * 42

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
                self.btns[idx] = tk.Button(self, font=("Meiryo UI", 10), anchor=tk.NW, bg=bg, fg=fg,
                                           relief='flat', command=lambda idx=idx: self.select_day(idx))
                self.btns[idx].place(x=15 + 75 * j, y=65 + 60 * i, width=70, height=50)

        self.cal_data = [""] * 42

        self.now = dt.datetime.now()
        self.year, self.month, self.day = self.now.year, self.now.month, self.now.day

        self.generate_calendar(self.year, self.month)
        self.set_calendar()
        self.label1["text"] = str(self.month)
        self.label2["text"] = cl.month_name[self.month]
        self.label3["text"] = str(self.year)

        tk.Button(self, text="prev", font=("Meiryo UI", 9), bg="#D0D0D0",
                  relief='flat', command=lambda: self.change_month(-1)).place(x=420, y=5, width=50, height=25)
        tk.Button(self, text="next", font=("Meiryo UI", 9), bg="#D0D0D0",
                  relief='flat', command=lambda: self.change_month(1)).place(x=480, y=5, width=50, height=25)

    def generate_calendar(self, y, m):
        self.cal_data = [""] * 42
        date_start = dt.date(y, m, 1)
        start_weekday = date_start.weekday()
        if start_weekday > 5:
            start_weekday -= 7
        max_day = cl.monthrange(y, m)[1]
        for i in range(max_day):
            self.cal_data[i + start_weekday + 1] = str(i + 1)

    def set_calendar(self):
        for i in range(42):
            self.btns[i]["text"] = self.cal_data[i]

    def change_month(self, offset):
        self.month += offset
        if self.month > 12:
            self.month = 1
            self.year += 1
        elif self.month < 1:
            self.month = 12
            self.year -= 1
        self.label1["text"] = str(self.month)
        self.label2["text"] = cl.month_name[self.month]
        self.label3["text"] = str(self.year)
        self.generate_calendar(self.year, self.month)
        self.set_calendar()

    def select_day(self, idx):
        day = self.cal_data[idx]
        if day:
            self.selected_date = dt.date(self.year, self.month, int(day))
            self.event_generate("<<CalendarSelected>>")

    def get_date(self):
        return self.selected_date

# これを外部から呼び出すとき
def calendar_component(master):
    return CalendarComponent(master)
