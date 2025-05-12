import unittest
import datetime as dt
import tkinter as tk
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from calendar_component import CalendarComponent

class TestCalendarComponent(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # ウィンドウを表示しない
        self.cal = CalendarComponent(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_initial_date(self):
        today = dt.date.today()
        self.assertEqual(self.cal.get_date(), today)

    def test_change_month_next(self):
        current_month = self.cal.month
        current_year = self.cal.year
        self.cal.change_month(1)
        if current_month == 12:
            self.assertEqual(self.cal.month, 1)
            self.assertEqual(self.cal.year, current_year + 1)
        else:
            self.assertEqual(self.cal.month, current_month + 1)
            self.assertEqual(self.cal.year, current_year)

    def test_change_month_prev(self):
        current_month = self.cal.month
        current_year = self.cal.year
        self.cal.change_month(-1)
        if current_month == 1:
            self.assertEqual(self.cal.month, 12)
            self.assertEqual(self.cal.year, current_year - 1)
        else:
            self.assertEqual(self.cal.month, current_month - 1)
            self.assertEqual(self.cal.year, current_year)

    def test_select_day(self):
        self.cal.generate_calendar(2025, 5)
        self.cal.set_calendar()
        idx = self.cal.cal_data.index('1')
        self.cal.select_day(idx)
        self.assertEqual(self.cal.get_date(), dt.date(2025, 5, 1))

if __name__ == '__main__':
    unittest.main()
