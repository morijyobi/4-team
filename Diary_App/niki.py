import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  
import csv
import os
from calendar_component import calendar_component
from PIL import Image, ImageTk 
import random
FOLDER_NAME = "diary_entries"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_FOLDER = os.path.join(BASE_DIR, "img")

if not os.path.exists(FOLDER_NAME):
    os.makedirs(FOLDER_NAME)

def save_entry():
    date_obj = cal.get_date()
    date_str = date_obj.strftime("%Y_%m_%d")

    weather = weather_cb.get()
    action = action_cb.get()
    satisfaction = satisfaction_entry.get()
    message = message_text.get("1.0", "end").strip()

    if not message:
        messagebox.showwarning("警告", "メッセージを入力してください！")
        return

    # CSV保存
    csv_path = os.path.join(FOLDER_NAME, f"{date_str}.csv")
    with open(csv_path, "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([date_str, weather, satisfaction, action])

    # テキスト保存
    txt_path = os.path.join(FOLDER_NAME, f"{date_str}.txt")
    with open(txt_path, "w", encoding='utf-8') as file:
        file.write(message)

    # 表示欄に追加
    diary_display.insert("end", f"【{date_str}】 天気: {weather} 行動: {action} 充実度: {satisfaction}\n{message}\n\n")

    # 入力欄クリア
    message_text.delete("1.0", "end")
    satisfaction_entry.delete(0, 'end')

    load_entries(date_obj)  # ← 保存直後にその日だけ再表示（重複防止）

    

def load_entries(selected_date=None):
    diary_display.delete(1.0, "end")

    if selected_date:
        date_str = selected_date.strftime("%Y_%m_%d")
        csv_path = os.path.join(FOLDER_NAME, f"{date_str}.csv")
        txt_path = os.path.join(FOLDER_NAME, f"{date_str}.txt")

        if os.path.exists(csv_path):
            with open(csv_path, "r", encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) == 4:
                        date, weather, satisfaction, action = row
                        message = ""
                        if os.path.exists(txt_path):
                            with open(txt_path, "r", encoding="utf-8") as t:
                                message = t.read()
                        diary_display.insert("end", f"【{date}】 天気: {weather} 行動: {action} 充実度: {satisfaction}\n{message}\n\n")
    else:
        # すべての日記を表示
        for file in sorted(os.listdir(FOLDER_NAME)):
            if file.endswith(".csv"):
                date_str = file[:-4]
                csv_path = os.path.join(FOLDER_NAME, f"{date_str}.csv")
                txt_path = os.path.join(FOLDER_NAME, f"{date_str}.txt")

                with open(csv_path, "r", encoding='utf-8') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if len(row) == 4:
                            date, weather, satisfaction, action = row
                            message = ""
                            if os.path.exists(txt_path):
                                with open(txt_path, "r", encoding="utf-8") as t:
                                    message = t.read()
                            diary_display.insert("end", f"【{date}】 天気: {weather} 行動: {action} 充実度: {satisfaction}\n{message}\n\n")


def on_date_click(event):
    selected_date = cal.get_date()
    selected_date_label.config(text=f"選択中の日付: {selected_date}") 
    load_entries(selected_date)

    


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
cal.bind("<<CalendarSelected>>", on_date_click)

# 天気
tk.Label(root, text="天気", font=label_font, bg="#f8f8f8").place(x=50, y=500)
weather_cb = ttk.Combobox(root, values=["晴れ", "曇り", "雨", "雪", "雷"], width=15)
weather_cb.place(x=120, y=500)

# 行動
tk.Label(root, text="行動", font=label_font, bg="#f8f8f8").place(x=50, y=540)
action_cb = ttk.Combobox(root, values=["出社", "テレワーク", "外回り", "出張", "休日"], width=15)
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
save_btn.place(x=350, y=620)
# 閉じるボタン
exit_btn = tk.Button(root, text="✖閉じる", command=root.quit,
                     font=("Helvetica", 10, "bold"), bg="gray", fg="white",
                     width=10, relief="flat", padx=10, pady=5)
exit_btn.place(x=470, y=620)

# 日記の日付表示ラベル
selected_date_label = tk.Label(root, text="日付を選んでください", font=("Helvetica", 12, "bold"), bg="#f8f8f8")
selected_date_label.place(x=700, y=20)


# 日記表示欄（右側）
diary_display = tk.Text(root, width=70, height=23, bd=1, relief="solid", font=font_main)
diary_display.place(x=700, y=50)



def draw_omikuji():
    from datetime import datetime

    today = datetime.now().date()
    log_file = "last_omikuji.txt"

    # すでに今日引いたか確認
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            last_date_str = f.read().strip()
            if last_date_str:
                try:
                    last_date = datetime.strptime(last_date_str, "%Y-%m-%d").date()
                    if last_date == today:
                        messagebox.showinfo("おみくじ", "今日はすでにおみくじを引きました！")
                        return
                except:
                    pass  # ファイルが壊れていた場合は無視して続行

    results = {
    "大吉": os.path.join(IMG_FOLDER, "daikichi.png"),
    "中吉": os.path.join(IMG_FOLDER, "chukichi.png"),
    "小吉": os.path.join(IMG_FOLDER, "shokichi.png"),
    "吉": os.path.join(IMG_FOLDER, "kichi.png"),
    "末吉": os.path.join(IMG_FOLDER, "suekichi.png"),
    "凶": os.path.join(IMG_FOLDER, "kyo.png"),
    "大凶": os.path.join(IMG_FOLDER, "daikyo.png")
}

    result = random.choice(list(results.keys()))
    image_path = results[result]

    # 画像読み込み
    img = Image.open(image_path)
    img = img.resize((150, 150))
    img_tk = ImageTk.PhotoImage(img)

    # 表示
    omikuji_image_label.config(image=img_tk)
    omikuji_image_label.image = img_tk

    # 今日の日付をファイルに記録
    with open(log_file, "w") as f:
        f.write(str(today))



def on_enter(e):
    omikuji_btn["background"] = "#e6d5b8"
    omikuji_btn["relief"] = "sunken"

def on_leave(e):
    omikuji_btn["background"] = "#f5e1c8"
    omikuji_btn["relief"] = "raised"

# おみくじボタン
omikuji_btn = tk.Button(
    root,
    text="おみくじを引く",
    command=draw_omikuji,
    font=("Meiryo", 14, "bold"),
    bg="#f5e1c8",
    fg="#3c2f2f",
    activebackground="#e6d5b8",
    relief="raised",
    bd=2,
    width=20,
    height=2
)

omikuji_btn.bind("<Enter>", on_enter)
omikuji_btn.bind("<Leave>", on_leave)
omikuji_btn.place(x=900, y=550)

# 結果画像表示用ラベル
omikuji_image_label = tk.Label(root, bg="#f8f8f8")
omikuji_image_label.place(x=700, y=500)  





# 起動時に既存データ読み込み
load_entries()

selected_date_label.config(text=f"選択中の日付: {cal.get_date()}")



root.mainloop()