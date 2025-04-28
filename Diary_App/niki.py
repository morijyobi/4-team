import tkinter as tk
from tkinter import ttk
from calendar_component import calendar_component

def save_entry():
    date = cal.get_date()
    weather = weather_cb.get()
    action = action_cb.get()
    satisfaction = satisfaction_entry.get()
    message = message_text.get("1.0", "end").strip()

    diary_display.insert("end", f"【{date}】\n{message}\n\n")
    message_text.delete("1.0", "end")

def exit_fullscreen(event=None):
    root.attributes("-fullscreen", False)

root = tk.Tk()
root.title("Monologue")
root.attributes("-fullscreen", True)  # 全画面表示
root.configure(bg="#f8f8f8")
root.bind("<Escape>", exit_fullscreen)

font_main = ("Helvetica", 10)
label_font = ("Helvetica", 10, "bold")

# ロゴ（左上）
tk.Label(root, text="Monologue", font=("Helvetica", 20, "bold"), bg="#f8f8f8").place(x=30, y=20)

# カレンダー
cal = calendar_component(root)
cal.place(x=30, y=70)

# 天気
tk.Label(root, text="天気", font=label_font, bg="#f8f8f8").place(x=50, y=500)
weather_cb = ttk.Combobox(root, values=["晴れ", "曇り", "雨", "雪", "雷"], width=15)
weather_cb.place(x=120, y=500)

# 行動
tk.Label(root, text="行動", font=label_font, bg="#f8f8f8").place(x=50, y=540)
action_cb = ttk.Combobox(root, values=["勉強", "仕事", "運動", "遊び", "休憩"], width=15)
action_cb.place(x=120, y=540)

# 充実度
tk.Label(root, text="充実度", font=label_font, bg="#f8f8f8").place(x=50, y=580)
satisfaction_entry = tk.Entry(root, width=18)
satisfaction_entry.place(x=120, y=580)

# メッセージ欄
tk.Label(root, text="今日の思い出を記録しよう！", font=("Helvetica", 9), bg="#f8f8f8", fg="gray").place(x=370, y=480)
message_frame = tk.Frame(root, bg="white", bd=1, relief="solid", width=300, height=120)
message_frame.place(x=330, y=500)
message_text = tk.Text(message_frame, width=34, height=6, bd=0, font=font_main)
message_text.pack(padx=5, pady=5)

# 保存ボタン
save_btn = tk.Button(root, text="📕記録する", command=save_entry,
                     font=("Helvetica", 10, "bold"), bg="black", fg="white",
                     width=10, relief="flat", padx=10, pady=5)
save_btn.place(x=400, y=620)


# 日記の日付表示ラベル
selected_date_label = tk.Label(root, text="日付を選んでください", font=("Helvetica", 12, "bold"), bg="#f8f8f8")
selected_date_label.place(x=700, y=20)


# 日記表示欄（右側）
diary_display = tk.Text(root, width=70, height=40, bd=1, relief="solid", font=font_main)
diary_display.place(x=700, y=50)

root.mainloop()
