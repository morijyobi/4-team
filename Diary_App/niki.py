import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv
import os
from calendar_component import calendar_component
from PIL import Image, ImageTk
import random
from datetime import datetime

FOLDER_NAME = "diary_entries"
if not os.path.exists(FOLDER_NAME):
    os.makedirs(FOLDER_NAME)

omikuji_result = None  # おみくじ結果を保持

def save_entry():
    global omikuji_result

    date_obj = cal.get_date()
    date_str = date_obj.strftime("%Y_%m_%d")

    weather = weather_cb.get()
    action = action_cb.get()
    satisfaction = satisfaction_entry.get()
    message = message_text.get("1.0", "end").strip()
    
    satisfaction = satisfaction_entry.get()
    
    try:
        satisfaction_val = int(satisfaction)
        if not (0 <= satisfaction_val <= 100):
            messagebox.showerror("エラー", "充実度は0から100の範囲で入力してください。")
            return
    except ValueError:
        messagebox.showerror("エラー", "充実度には整数を入力してください。")
        return

    if not message:
        messagebox.showwarning("警告", "メッセージを入力してください！")
        return

    # CSV保存
    csv_path = os.path.join(FOLDER_NAME, f"{date_str}.csv")
    with open(csv_path, "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([date_str, weather, satisfaction, action, omikuji_result or "未実施"])

    # テキスト保存
    txt_path = os.path.join(FOLDER_NAME, f"{date_str}.txt")
    with open(txt_path, "w", encoding='utf-8') as file:
        file.write(message)

    # 表示欄に追加
    diary_display.insert("end", f"【{date_str}】 天気: {weather} 行動: {action} 充実度: {satisfaction} おみくじ: {omikuji_result or '未実施'}\n{message}\n\n")

    # 入力欄クリア
    message_text.delete("1.0", "end")
    satisfaction_entry.delete(0, 'end')

    load_entries(date_obj)  # 保存直後にその日だけ再表示（重複防止）

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
                    if len(row) == 5:
                        date, weather, satisfaction, action, omikuji = row
                        message = ""
                        if os.path.exists(txt_path):
                            with open(txt_path, "r", encoding="utf-8") as t:
                                message = t.read()
                        diary_display.insert("end", f"【{date}】 天気: {weather} 行動: {action} 充実度: {satisfaction} おみくじ: {omikuji}\n{message}\n\n")
    else:
        for file in sorted(os.listdir(FOLDER_NAME)):
            if file.endswith(".csv"):
                date_str = file[:-4]
                csv_path = os.path.join(FOLDER_NAME, f"{date_str}.csv")
                txt_path = os.path.join(FOLDER_NAME, f"{date_str}.txt")

                with open(csv_path, "r", encoding='utf-8') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if len(row) == 5:
                            date, weather, satisfaction, action, omikuji = row
                            message = ""
                            if os.path.exists(txt_path):
                                with open(txt_path, "r", encoding="utf-8") as t:
                                    message = t.read()
                            diary_display.insert("end", f"【{date}】 天気: {weather} 行動: {action} 充実度: {satisfaction} おみくじ: {omikuji}\n{message}\n\n")

def on_date_click(event):
    selected_date = cal.get_date()
    selected_date_label.config(text=f"選択中の日付: {selected_date}")
    load_entries(selected_date)

def exit_fullscreen(event=None):
    root.attributes("-fullscreen", False)

root = tk.Tk()
root.title("Monologue")
root.attributes("-fullscreen", True)
root.configure(bg="#f8f8f8")
root.bind("<Escape>", exit_fullscreen)

font_main = ("Helvetica", 10)
label_font = ("Helvetica", 10, "bold")

tk.Label(root, text="Monologue", font=("Helvetica", 20, "bold"), bg="#f8f8f8").place(x=30, y=20)

cal = calendar_component(root)
cal.place(x=30, y=70)
cal.bind("<<CalendarSelected>>", on_date_click)

tk.Label(root, text="天気", font=label_font, bg="#f8f8f8").place(x=50, y=500)
weather_cb = ttk.Combobox(root, values=["晴れ", "曇り", "雨", "雪", "雷"], width=15)
weather_cb.place(x=120, y=500)

tk.Label(root, text="行動", font=label_font, bg="#f8f8f8").place(x=50, y=540)
action_cb = ttk.Combobox(root, values=["出社", "テレワーク", "外回り", "出張", "休日"], width=15)
action_cb.place(x=120, y=540)

tk.Label(root, text="充実度", font=label_font, bg="#f8f8f8").place(x=50, y=580)
satisfaction_entry = tk.Entry(root, width=18)
satisfaction_entry.place(x=120, y=580)

tk.Label(root, text="今日の思い出を記録しよう！", font=("Helvetica", 9), bg="#f8f8f8", fg="gray").place(x=370, y=480)
message_frame = tk.Frame(root, bg="white", bd=1, relief="solid", width=300, height=120)
message_frame.place(x=330, y=500)
message_text = tk.Text(message_frame, width=34, height=6, bd=0, font=font_main)
message_text.pack(padx=5, pady=5)

save_btn = tk.Button(root, text="📕記録する", command=save_entry,
                     font=("Helvetica", 10, "bold"), bg="black", fg="white",
                     width=10, relief="flat", padx=10, pady=5)
save_btn.place(x=350, y=620)

exit_btn = tk.Button(root, text="✖閉じる", command=root.quit,
                     font=("Helvetica", 10, "bold"), bg="gray", fg="white",
                     width=10, relief="flat", padx=10, pady=5)
exit_btn.place(x=470, y=620)

selected_date_label = tk.Label(root, text="日付を選んでください", font=("Helvetica", 12, "bold"), bg="#f8f8f8")
selected_date_label.place(x=700, y=20)

diary_display = tk.Text(root, width=70, height=23, bd=1, relief="solid", font=font_main)
diary_display.place(x=700, y=50)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_FOLDER = os.path.join(BASE_DIR, "img")

def draw_omikuji():
    global omikuji_result

    today = datetime.now().date()
    log_file = "last_omikuji.txt"

    # すでに今日引いていれば再表示のみ
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            log = f.read().strip()
            if log:
                try:
                    last_date_str, last_result = log.split(",")
                    last_date = datetime.strptime(last_date_str, "%Y-%m-%d").date()
                    if last_date == today:
                        omikuji_result = last_result
                        image_path = os.path.join(IMG_FOLDER, f"{omikuji_result}.png")
                        if os.path.exists(image_path):
                            img = Image.open(image_path)
                            img = img.resize((150, 150))
                            img_tk = ImageTk.PhotoImage(img)
                            omikuji_image_label.config(image=img_tk)
                            omikuji_image_label.image = img_tk
                        messagebox.showinfo("おみくじ", f"今日はすでにおみくじを引きました！\n今日の運勢は「{omikuji_result}」です。")
                        return
                except:
                    pass

    # 新規に抽選
    results = {
        "大吉": os.path.join(IMG_FOLDER, "daikichi.png"),
        "中吉": os.path.join(IMG_FOLDER, "chukichi.png"),
        "小吉": os.path.join(IMG_FOLDER, "shokichi.png"),
        "吉": os.path.join(IMG_FOLDER, "kichi.png"),
        "末吉": os.path.join(IMG_FOLDER, "suekichi.png"),
        "凶": os.path.join(IMG_FOLDER, "kyo.png"),
        "大凶": os.path.join(IMG_FOLDER, "daikyo.png")
    }

    omikuji_result = random.choice(list(results.keys()))
    image_path = results[omikuji_result]

    img = Image.open(image_path)
    img = img.resize((150, 150))
    img_tk = ImageTk.PhotoImage(img)
    omikuji_image_label.config(image=img_tk)
    omikuji_image_label.image = img_tk

    # 日付 + 結果を保存
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"{today},{omikuji_result}")

    messagebox.showinfo("おみくじ", f"今日の運勢は「{omikuji_result}」です！")

def on_enter(e):
    omikuji_btn["background"] = "#e6d5b8"
    omikuji_btn["relief"] = "sunken"

def on_leave(e):
    omikuji_btn["background"] = "#f5e1c8"
    omikuji_btn["relief"] = "raised"

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

omikuji_image_label = tk.Label(root, bg="#f8f8f8")
omikuji_image_label.place(x=700, y=500)

load_entries()
selected_date_label.config(text=f"選択中の日付: {cal.get_date()}")

root.mainloop()
