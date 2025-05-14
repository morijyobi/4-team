import sys
import os
import unittest
import tkinter as tk

# calendar_component.py のある Diary_App をパスに追加
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../Diary_App"))

from calendar_component import calendar_component

class TestCalendarComponent(unittest.TestCase):

    def setUp(self):
        # テスト用のルートウィンドウ作成
        self.root = tk.Tk()
        self.root.withdraw()  # GUI表示を抑制
        self.calendar = calendar_component(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_default_selected_date_is_today(self):
        import datetime
        today = datetime.date.today()
        self.assertEqual(self.calendar.get_date(), today)

    def test_change_month_increments_correctly(self):
        current_month = self.calendar.month
        current_year = self.calendar.year
        self.calendar.change_month(1)

        if current_month == 12:
            self.assertEqual(self.calendar.month, 1)
            self.assertEqual(self.calendar.year, current_year + 1)
        else:
            self.assertEqual(self.calendar.month, current_month + 1)
            self.assertEqual(self.calendar.year, current_year)

    def test_change_month_decrements_correctly(self):
        current_month = self.calendar.month
        current_year = self.calendar.year
        self.calendar.change_month(-1)

        if current_month == 1:
            self.assertEqual(self.calendar.month, 12)
            self.assertEqual(self.calendar.year, current_year - 1)
        else:
            self.assertEqual(self.calendar.month, current_month - 1)
            self.assertEqual(self.calendar.year, current_year)

if __name__ == "__main__":
    unittest.main()
