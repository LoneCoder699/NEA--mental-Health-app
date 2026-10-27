import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, date, timedelta
import json
from pathlib import Path
from collections import deque
from tkcalendar import DateEntry

DATA_FILE = Path.home() / "goal_tracking_data.json"

BG = "#f5f5f5"
PANEL = "#dedede"
SIDEBAR = "#1E1E1E"
DARK = "#111111"
BLACK = "#000000"
WHITE = "#ffffff"
GRAY = "#777777"
GRID = "#8c8c8c"
LIGHT_GRAY = "#eeeeee"

DATA_FILE = Path.home()/"mood_tracking_data.json"
EXPORT_FILE = Path.home()/"Mood_Histroy.csv"
MOODS = {
    1: {"emoji": "😭", "name": "Awful", "color": "#111111"},
    2: {"emoji": "😢", "name": "Sad",   "color": "#3d3d3d"},
    3: {"emoji": "😑", "name": "Meh",  "color": "#6b6b6b"},
    4: {"emoji": "😁", "name": "Good",  "color": "#999999"},
    5: {"emoji": "🤩", "name": "Amazing", "color": "#bdbdbd"},
}

class Mood(ctk.CTk):
    def __init__(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        super().__init__()
        self.title("Mood Tracking")
        self.geometry("1280x760")
        self.minsize(1050, 650)
        self.configure(fg_color=BG)
        self.entries = {}
        self.selected_mood = None
        self.mood_buttons = {}
        self.chart_data = []
        self.history_popup = None
        self.settings_popup = None
        self.load_data()
        self.build_ui()
        self.restore_today()
        self.refresh_all()
        self.bind('<Return>', lambda e: self.save_data())

    def load_data(self):
        if not DATA_FILE.exists():
            return
        try:
            raw = json.loads(DATA_FILE.read_text(encoding = 'utf-8'))
            for key, e in raw.get("entries",{}).items():
                datetime.strptime(key,'%Y-%m-%d')
                mood = int(e.get('mood',0))
                if mood in MOODS:
                    self.entries[key]={'mood':mood,'note':str(e.get("note",'')),'time':str(e.get('time',''))}
        except Exception:
            self.entries = {}

    def save_data(self):
        try:
            DATA_FILE.write_text(json.dumps({'entries':self.entries},indent = True),encoding='utf-8')
        except Exception as e:
            messagebox.showerror("Save Error",str(e),parent = self)

    def create_streak(self):
        d = date.today()

