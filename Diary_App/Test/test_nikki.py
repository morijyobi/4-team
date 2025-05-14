import unittest
import os
import shutil
import csv
import datetime as dt
from unittest.mock import patch, MagicMock
import tkinter as tk
import sys

# calendar_componentのダミーを用意（UIテストを避けるため）
class DummyCalendar:
    def __init__(self, date=None):
        self._date = date or dt.date.today()
    def get_date(self):
        return self._date
    def bind(self, *args, **kwargs):
        pass
    def place(self, *args, **kwargs):
        pass

# niki.pyの関数をimportするための準備
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import niki

class TestNiki(unittest.TestCase):
    def setUp(self):
        # テスト用の一時ディレクトリを作成
        self.test_dir = os.path.join(os.path.dirname(__file__), 'test_diary_entries')
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)
        niki.FOLDER_NAME = self.test_dir
        # テスト用のカレンダーと各ウィジェットをダミーで置き換え
        niki.cal = DummyCalendar(dt.date(2025, 5, 7))
        niki.weather_cb = MagicMock()
        niki.weather_cb.get.return_value = '晴れ'
        niki.action_cb = MagicMock()
        niki.action_cb.get.return_value = '出社'
        niki.satisfaction_entry = MagicMock()
        niki.satisfaction_entry.get.return_value = '80'
        niki.satisfaction_entry.delete = MagicMock()
        niki.message_text = MagicMock()
        niki.message_text.get.return_value = 'テストメッセージ'
        niki.message_text.delete = MagicMock()
        niki.diary_display = MagicMock()
        niki.diary_display.insert = MagicMock()
        niki.diary_display.delete = MagicMock()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch('niki.messagebox.showerror')
    @patch('niki.messagebox.showwarning')
    def test_save_entry_success(self, mock_warning, mock_error):
        niki.omikuji_result = '大吉'
        niki.save_entry()
        # ファイルが作成されているか
        csv_path = os.path.join(self.test_dir, '2025_05_07.csv')
        txt_path = os.path.join(self.test_dir, '2025_05_07.txt')
        self.assertTrue(os.path.exists(csv_path))
        self.assertTrue(os.path.exists(txt_path))
        # CSV内容確認
        with open(csv_path, encoding='utf-8') as f:
            row = next(csv.reader(f))
            self.assertEqual(row[0], '2025_05_07')
            self.assertEqual(row[1], '晴れ')
            self.assertEqual(row[2], '80')
            self.assertEqual(row[3], '出社')
            self.assertEqual(row[4], '大吉')
        # テキスト内容確認
        with open(txt_path, encoding='utf-8') as f:
            self.assertEqual(f.read(), 'テストメッセージ')
        mock_error.assert_not_called()
        mock_warning.assert_not_called()

    @patch('niki.messagebox.showerror')
    def test_save_entry_invalid_satisfaction(self, mock_error):
        niki.satisfaction_entry.get.return_value = '200'
        niki.save_entry()
        mock_error.assert_called_once()
        self.assertIn('充実度は0から100の範囲で入力してください', mock_error.call_args[0][1])

    @patch('niki.messagebox.showerror')
    def test_save_entry_nonint_satisfaction(self, mock_error):
        niki.satisfaction_entry.get.return_value = 'abc'
        niki.save_entry()
        mock_error.assert_called_once()
        self.assertIn('充実度には整数を入力してください', mock_error.call_args[0][1])

    @patch('niki.messagebox.showwarning')
    def test_save_entry_empty_message(self, mock_warning):
        niki.message_text.get.return_value = ''
        niki.save_entry()
        mock_warning.assert_called_once()
        self.assertIn('メッセージを入力してください', mock_warning.call_args[0][1])

    def test_load_entries(self):
        # 事前にファイルを作成
        csv_path = os.path.join(self.test_dir, '2025_05_07.csv')
        txt_path = os.path.join(self.test_dir, '2025_05_07.txt')
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['2025_05_07', '晴れ', '80', '出社', '大吉'])
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write('テストメッセージ')
        niki.load_entries(dt.date(2025, 5, 7))
        niki.diary_display.insert.assert_called()

if __name__ == '__main__':
    unittest.main()