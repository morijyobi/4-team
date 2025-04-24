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

root = tk.Tk()
root.title("Journée")
root.geometry("1440x1024")
root.configure(bg="#f8f8f8")

font_main = ("Helvetica", 10)
label_font = ("Helvetica", 10, "bold")

# ロゴ
tk.Label(root, text="M.", font=("Helvetica", 20, "bold"), bg="#f8f8f8").place(x=30, y=20)

# カレンダー
cal = calendar_component(root)
cal.place(x=30, y=50)


# 天気
tk.Label(root, text="天気", font=label_font, bg="#f8f8f8").place(x=30, y=260)
weather_cb = ttk.Combobox(root, values=["晴れ", "曇り", "雨", "雪", "雷"], width=15)
weather_cb.place(x=80, y=260)

# 行動
tk.Label(root, text="行動", font=label_font, bg="#f8f8f8").place(x=30, y=300)
action_cb = ttk.Combobox(root, values=["勉強", "仕事", "運動", "遊び", "休憩"], width=15)
action_cb.place(x=80, y=300)

# 充実度
tk.Label(root, text="充実度", font=label_font, bg="#f8f8f8").place(x=30, y=340)
satisfaction_entry = tk.Entry(root, width=18)
satisfaction_entry.place(x=100, y=340)

# メッセージ欄
tk.Label(root, text="メッセージを入力してください", font=("Helvetica", 9), bg="#f8f8f8", fg="gray").place(x=30, y=380)
message_frame = tk.Frame(root, bg="white", bd=1, relief="solid", width=250, height=80)
message_frame.place(x=30, y=400)
message_text = tk.Text(message_frame, width=30, height=5, bd=0, font=font_main)
message_text.pack(padx=5, pady=5)

# 保存ボタン
save_btn = tk.Button(root, text="💾 保存", command=save_entry,
                     font=("Helvetica", 10, "bold"), bg="black", fg="white",
                     width=10, relief="flat", padx=10, pady=5)
save_btn.place(x=100, y=490)

# 日記表示枠
diary_display = tk.Text(root, width=40, height=26, bd=1, relief="solid", font=font_main)
diary_display.place(x=720, y=30)

root.mainloop()
