import csv
import json
import sys
from datetime import date, datetime, timedelta
from math import hypot
from pathlib import Path
from tkinter import messagebox
import tkinter as tk

import customtkinter as ctk

DATA_FILE = Path.home() / "mood_tracking_data.json"
EXPORT_FILE = Path.home() / "mood_history.csv"

BG = "#f5f5f5"
PANEL = "#dedede"
SIDEBAR = "#1E1E1E"
DARK = "#111111"
BLACK = "#000000"
WHITE = "#ffffff"
GRAY = "#777777"
GRID = "#8c8c8c"
BTN_IDLE = "#bcbcbc"

MOODS = {
    1: {"emoji": "😭", "name": "Awful", "color": "#111111"},
    2: {"emoji": "😢", "name": "Sad",   "color": "#3d3d3d"},
    3: {"emoji": "😑", "name": "Meh",  "color": "#6b6b6b"},
    4: {"emoji": "😁", "name": "Good",  "color": "#999999"},
    5: {"emoji": "🤩", "name": "Amazing", "color": "#bdbdbd"},
}

if sys.platform.startswith("win"):
    EMOJI_FONT = "Segoe UI Emoji"
elif sys.platform == "darwin":
    EMOJI_FONT = "Apple Color Emoji"
else:
    EMOJI_FONT = "Noto Color Emoji"

HELP_TEXT = (
    "If you are in immediate danger, please contact your local emergency "
    "number right away.\n\n"
    "India: Tele-MANAS 14416 (24x7 mental health support).\n\n"
    "You can also reach out to someone you trust. You do not have to go "
    "through a hard moment alone."
)


class MoodStack:
    def __init__(self, items=None):
        self._items = list(items) if items else []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            return None
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def clear(self):
        self._items.clear()

    def to_list(self):
        return list(self._items)


def clean_entry(e):
    try:
        mood = int(e.get("mood", 0))
    except Exception:
        return None
    if mood not in MOODS:
        return None
    return {
        "mood": mood,
        "note": str(e.get("note", "")),
        "time": str(e.get("time", "")),
    }


class MoodTrackingPage(ctk.CTk):
    def __init__(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        super().__init__()
        self.title("Mood Tracking")
        self.geometry("1280x830")
        self.minsize(1050, 720)
        self.configure(fg_color=BG)

        self.entries = {}
        self.stack = MoodStack()
        self.selected_mood = None
        self.chart_points = []
        self.mood_buttons = {}
        self.history_popup = None
        self.settings_popup = None

        self.load_data()
        self.build_ui()
        self.restore_today()
        self.refresh_all()

        self.bind("<Control-s>", lambda e: self.save_data())

    def load_data(self):
        if not DATA_FILE.exists():
            return
        try:
            raw = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            for key, e in raw.get("entries", {}).items():
                datetime.strptime(key, "%Y-%m-%d")
                cleaned = clean_entry(e)
                if cleaned:
                    self.entries[key] = cleaned
        except Exception:
            self.entries = {}

        items = []
        try:
            for item in json.loads(DATA_FILE.read_text(encoding="utf-8")).get("stack", []):
                datetime.strptime(item["date"], "%Y-%m-%d")
                cleaned = clean_entry(item)
                if not cleaned:
                    continue
                cleaned["date"] = item["date"]
                prev = item.get("previous")
                cleaned["previous"] = clean_entry(prev) if isinstance(prev, dict) else None
                items.append(cleaned)
        except Exception:
            items = []

        if not items:
            for key in sorted(self.entries):
                e = dict(self.entries[key])
                e["date"] = key
                e["previous"] = None
                items.append(e)
        self.stack = MoodStack(items)

    def save_data(self):
        try:
            DATA_FILE.write_text(
                json.dumps(
                    {"entries": self.entries, "stack": self.stack.to_list()}, indent=2
                ),
                encoding="utf-8",
            )
        except Exception as e:
            messagebox.showerror("Save Error", str(e), parent=self)

    def current_streak(self):
        d = date.today()
        if d.isoformat() not in self.entries:
            d -= timedelta(days=1)
        n = 0
        while d.isoformat() in self.entries:
            n += 1
            d -= timedelta(days=1)
        return n

    def build_ui(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_left_navbar()

        self.main = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.main.grid(row=0, column=1, sticky="nsew")
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_columnconfigure(1, weight=0)
        self.main.grid_columnconfigure(2, weight=0)
        self.main.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            self.main, text="HOW IS YOUR MOOD?",
            font=("Arial", 26), text_color=DARK,
        ).grid(row=0, column=0, columnspan=2, pady=(8, 0))

        self.build_mood_card()
        self.build_streak()
        self.build_icon_rail()
        self.build_bottom()

    def create_left_navbar(self):
        self.left_nav_expanded = True
        self.left_nav_width = 260
        self.left_nav_collapsed_width = 65

        self.left_navbar = ctk.CTkFrame(
            self, width=self.left_nav_width, fg_color=GRAY, corner_radius=0
        )
        self.left_navbar.grid(row=0, column=0, sticky="ns")
        self.left_navbar.grid_propagate(False)

        top = ctk.CTkFrame(self.left_navbar, height=100, fg_color="transparent")
        top.pack(fill="x", padx=5, pady=(10, 20))
        top.pack_propagate(False)

        self.left_logo = ctk.CTkLabel(
            top, text="Logo", width=160, height=70, fg_color=SIDEBAR,
            text_color=WHITE, font=("Arial", 13), corner_radius=0,
        )
        self.left_logo.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.left_toggle = ctk.CTkButton(
            top, text="<", width=45, height=70, fg_color=SIDEBAR,
            hover_color="#333333", text_color=WHITE, font=("Arial", 24),
            corner_radius=0, command=self.toggle_left_navbar,
        )
        self.left_toggle.pack(side="right")

        menu = ctk.CTkFrame(self.left_navbar, fg_color="transparent")
        menu.pack(fill="both", expand=True, padx=3)

        self.left_nav_buttons = []
        items = [
            ("Mental health survey", self.open_mental_health_survey),
            ("AI ChatBot", self.open_ai_chatbot),
            ("Appointment Booking", self.open_appointment_booking),
            ("Journaling", self.open_journaling),
            ("Mood Tracking", self.open_mood_tracking),
            ("Goal Tracking", self.open_goal_tracking),
            ("News/ Blogs", self.open_news_blogs),
            ("Resources", self.open_resources),
        ]
        for text, command in items:
            ctk.CTkFrame(menu, height=10, fg_color=GRAY, corner_radius=0).pack(fill="x")
            active = text == "Mood Tracking"
            button = ctk.CTkButton(
                menu, text=text, height=48,
                fg_color="#4a4a4a" if active else SIDEBAR,
                hover_color="#333333",
                text_color=WHITE if active else "#D0D0D0",
                font=("Arial", 14), corner_radius=0, anchor="center",
                command=command,
            )
            button.pack(fill="x")
            self.left_nav_buttons.append((button, text))

    def toggle_left_navbar(self):
        if self.left_nav_expanded:
            self.left_navbar.configure(width=self.left_nav_collapsed_width)
            self.left_logo.pack_forget()
            self.left_toggle.configure(text=">")
            for button, _ in self.left_nav_buttons:
                button.configure(text="")
        else:
            self.left_navbar.configure(width=self.left_nav_width)
            self.left_logo.pack(side="left", fill="both", expand=True, padx=(0, 10))
            self.left_toggle.configure(text="<")
            for button, text in self.left_nav_buttons:
                button.configure(text=text)
        self.left_nav_expanded = not self.left_nav_expanded

    def open_mental_health_survey(self): print("Mental Health Survey selected")
    def open_ai_chatbot(self): print("AI ChatBot selected")
    def open_appointment_booking(self): print("Appointment Booking selected")
    def open_journaling(self): print("Journaling selected")
    def open_mood_tracking(self): print("Mood Tracking selected")
    def open_goal_tracking(self): print("Goal Tracking selected")
    def open_news_blogs(self): print("News / Blogs selected")
    def open_resources(self): print("Resources selected")

    def build_mood_card(self):
        card = ctk.CTkFrame(self.main, fg_color=PANEL, corner_radius=0)
        card.grid(row=1, column=0, padx=(16, 6), pady=8, sticky="nsew")

        self.face_canvas = tk.Canvas(
            card, width=100, height=100, bg=PANEL, highlightthickness=0
        )
        self.face_canvas.pack(pady=(10, 0))

        self.feeling_label = ctk.CTkLabel(
            card, text="I am feeling ____", font=("Arial", 24), text_color=DARK
        )
        self.feeling_label.pack(pady=(0, 6))

        panel = ctk.CTkFrame(card, fg_color=DARK, corner_radius=0)
        panel.pack(fill="x", padx=12)

        row = ctk.CTkFrame(panel, fg_color="transparent")
        row.pack(fill="x", padx=8, pady=(10, 4))
        row.grid_columnconfigure(tuple(range(5)), weight=1)

        for i, value in enumerate(MOODS):
            cv = tk.Canvas(
                row, width=72, height=40, bg=BTN_IDLE,
                highlightthickness=0, cursor="hand2",
            )
            cv.grid(row=0, column=i, padx=6)
            cv.bind("<Button-1>", lambda e, v=value: self.select_mood(v))
            self.mood_buttons[value] = cv

        note_row = ctk.CTkFrame(panel, fg_color="transparent")
        note_row.pack(fill="x", padx=14, pady=(0, 10))
        note_row.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            note_row, text="Short Note:", text_color=WHITE, font=("Arial", 11)
        ).grid(row=0, column=0, padx=(0, 8))

        self.note_entry = ctk.CTkEntry(
            note_row, height=28, corner_radius=2, border_width=0,
            fg_color="#2b2b2b", text_color=WHITE,
            placeholder_text="What's on your mind? (optional)",
            placeholder_text_color="#999999",
        )
        self.note_entry.grid(row=0, column=1, sticky="ew")
        self.note_entry.bind("<Return>", lambda e: self.submit_mood())

        self.continue_button = ctk.CTkButton(
            card, text="Continue →", width=210, height=32, corner_radius=16,
            fg_color=BLACK, hover_color=GRAY, text_color=WHITE,
            font=("Arial", 12), command=self.submit_mood,
        )
        self.continue_button.pack(pady=(10, 2))

        stack_row = ctk.CTkFrame(card, fg_color="transparent")
        stack_row.pack(pady=(4, 0))
        self.undo_button = ctk.CTkButton(
            stack_row, text="Undo Last (Pop)", width=100, height=28, corner_radius=14,
            fg_color=DARK, hover_color=GRAY, text_color=WHITE,
            font=("Arial", 11), command=self.undo_last,
        )
        self.undo_button.pack(side="left", padx=4)
        self.peek_button = ctk.CTkButton(
            stack_row, text="Peek Latest", width=100, height=28, corner_radius=14,
            fg_color=DARK, hover_color=GRAY, text_color=WHITE,
            font=("Arial", 11), command=self.peek_latest,
        )
        self.peek_button.pack(side="left", padx=4)
        self.stack_label = ctk.CTkLabel(
            card, text="", font=("Arial", 10), text_color=GRAY
        )
        self.stack_label.pack(pady=(4, 0))

        self.status_label = ctk.CTkLabel(
            card, text="", font=("Arial", 10), text_color=GRAY
        )
        self.status_label.pack(pady=(0, 6))

    def build_streak(self):
        streak = ctk.CTkFrame(self.main, fg_color=PANEL, width=110, corner_radius=0)
        streak.grid(row=1, column=1, padx=6, pady=8, sticky="nsew")
        streak.grid_propagate(False)
        streak.pack_propagate(False)

        ctk.CTkLabel(
            streak, text="Streak", font=("Arial", 11), text_color=DARK
        ).pack(pady=(10, 0))
        ctk.CTkLabel(
            streak, text="Day", font=("Arial", 20), text_color=DARK
        ).pack()
        self.streak_label = ctk.CTkLabel(
            streak, text="0", font=("Arial", 22), text_color=DARK
        )
        self.streak_label.pack()

        flame = tk.Canvas(streak, width=44, height=48, bg=PANEL, highlightthickness=0)
        flame.pack(pady=(4, 0))
        flame.create_polygon(
            22, 3, 34, 20, 37, 33, 29, 45, 15, 45, 7, 33, 10, 20, 17, 27,
            smooth=True, fill=DARK, outline=DARK,
        )
        flame.create_oval(16, 30, 28, 44, fill=PANEL, outline=PANEL)

    def build_icon_rail(self):
        rail = ctk.CTkFrame(self.main, fg_color="transparent")
        rail.grid(row=0, column=2, rowspan=2, padx=(6, 16), pady=(8, 0), sticky="n")

        icons = [
            ("V", self.open_history),
            ("⚙", self.open_settings),
            ("⌂", self.go_today),
            ("☼", self.show_help),
        ]
        for text, command in icons:
            ctk.CTkButton(
                rail, text=text, width=46, height=46, corner_radius=23,
                fg_color=PANEL, hover_color="#c8c8c8", text_color=DARK,
                font=("Arial", 18), command=command,
            ).pack(pady=5)

    def build_bottom(self):
        bottom = ctk.CTkFrame(self.main, fg_color="transparent")
        bottom.grid(row=2, column=0, columnspan=3, padx=16, pady=(0, 14), sticky="nsew")
        bottom.grid_columnconfigure(0, weight=3, uniform="charts")
        bottom.grid_columnconfigure(1, weight=2, uniform="charts")
        bottom.grid_rowconfigure(0, weight=1)

        trend = ctk.CTkFrame(bottom, fg_color=PANEL, corner_radius=0)
        trend.grid(row=0, column=0, padx=(0, 6), sticky="nsew")
        ctk.CTkLabel(
            trend, text="MOOD TREND (LAST 14 DAYS)",
            font=("Arial", 10, "bold"), text_color=DARK,
        ).pack(anchor="nw", padx=12, pady=(9, 0))
        self.trend_caption = ctk.CTkLabel(
            trend, text="", font=("Arial", 9), text_color=GRAY, anchor="w"
        )
        self.trend_caption.pack(anchor="nw", padx=12)
        self.trend_canvas = tk.Canvas(trend, bg=PANEL, highlightthickness=0)
        self.trend_canvas.pack(fill="both", expand=True, padx=8, pady=(2, 8))
        self.trend_canvas.bind("<Configure>", lambda e: self.draw_trend())
        self.trend_canvas.bind("<Motion>", self.on_trend_motion)
        self.trend_canvas.bind("<Leave>", lambda e: self.reset_caption())

        donut = ctk.CTkFrame(bottom, fg_color=PANEL, corner_radius=0)
        donut.grid(row=0, column=1, padx=(6, 0), sticky="nsew")
        ctk.CTkLabel(
            donut, text="MOOD BREAKDOWN (LAST 30 DAYS)",
            font=("Arial", 10, "bold"), text_color=DARK,
        ).pack(anchor="nw", padx=12, pady=(9, 0))
        self.donut_canvas = tk.Canvas(donut, bg=PANEL, highlightthickness=0)
        self.donut_canvas.pack(fill="both", expand=True, padx=8, pady=8)
        self.donut_canvas.bind("<Configure>", lambda e: self.draw_donut())

    def select_mood(self, mood):
        self.selected_mood = mood
        for value,cv in self.mood_buttons.items():
            cv.delete("all")
            cv.configure(bg=WHITE if value == mood else BTN_IDLE)
            cv.create_text(36, 20, text=MOODS[value]["emoji"], font=(EMOJI_FONT, -26))
        self.feeling_label.configure(
            text=f"I am feeling {MOODS[mood]['name']}" if mood else "I am feeling ____"
        )
        self.face_canvas.delete("all")
        self.face_canvas.create_text(
            50, 50, text=MOODS[mood or 4]["emoji"], font=(EMOJI_FONT, -78)
        )

    def restore_today(self):
        entry = self.entries.get(date.today().isoformat())
        self.select_mood(entry["mood"] if entry else None)
        self.note_entry.delete(0, "end")
        if entry and entry["note"]:
            self.note_entry.insert(0, entry["note"])

    def submit_mood(self):
        if self.selected_mood is None:
            messagebox.showwarning(
                "Pick a mood", "Please choose how you are feeling first.", parent=self
            )
            return

        today = date.today().isoformat()
        previous = self.entries.get(today)
        new_entry = {
            "mood": self.selected_mood,
            "note": self.note_entry.get().strip()[:140],
            "time": datetime.now().strftime("%H:%M"),
        }
        self.entries[today] = new_entry
        record = dict(new_entry)
        record["date"] = today
        record["previous"] = dict(previous) if previous else None
        self.stack.push(record)
        self.save_data()
        self.refresh_all()

        self.status_label.configure(
            text=f"Saved: {MOODS[self.selected_mood]['name']} · streak Day {self.current_streak()}"
        )
        self.after(4000, lambda: self.status_label.configure(text=""))

    def undo_last(self):
        if self.stack.is_empty():
            messagebox.showinfo("Nothing to undo", "The mood stack is empty.", parent=self)
            return
        top = self.stack.pop()
        if top["previous"]:
            self.entries[top["date"]] = dict(top["previous"])
        else:
            self.entries.pop(top["date"], None)
        self.save_data()
        self.restore_today()
        self.refresh_all()
        self.status_label.configure(text=f"Undid entry for {top['date']}")
        self.after(4000, lambda: self.status_label.configure(text=""))

    def peek_latest(self):
        top = self.stack.peek()
        if top is None:
            messagebox.showinfo("Stack empty", "No mood has been logged yet.", parent=self)
            return
        d = datetime.strptime(top["date"], "%Y-%m-%d").strftime("%a, %d %b %Y")
        text = f"{d} at {top['time']}\nMood: {MOODS[top['mood']]['name']}"
        if top["note"]:
            text += f"\nNote: {top['note']}"
        text += f"\n\nStack size: {self.stack.size()}"
        messagebox.showinfo("Latest entry (top of stack)", text, parent=self)

    def go_today(self):
        self.restore_today()
        self.refresh_all()

    def show_help(self):
        messagebox.showinfo("Need support?", HELP_TEXT, parent=self)

    def open_history(self):
        if self.history_popup is not None and self.history_popup.winfo_exists():
            self.history_popup.lift()
            return

        win = ctk.CTkToplevel(self)
        self.history_popup = win
        win.title("Mood History")
        win.geometry("460x520")
        win.configure(fg_color=PANEL)
        win.transient(self)

        ctk.CTkLabel(
            win, text="Mood History", font=("Arial", 17, "bold"), text_color=DARK
        ).pack(anchor="w", padx=18, pady=12)

        scroll = ctk.CTkScrollableFrame(win, fg_color=PANEL)
        scroll.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        scroll.grid_columnconfigure(0, weight=1)

        keys = sorted(self.entries, reverse=True)[:90]
        if not keys:
            ctk.CTkLabel(
                scroll, text="No mood entries yet.", text_color=GRAY
            ).grid(row=0, column=0, pady=20)
            return

        for r, key in enumerate(keys):
            e = self.entries[key]
            d = datetime.strptime(key, "%Y-%m-%d").strftime("%a, %d %b %Y")
            row = ctk.CTkFrame(scroll, fg_color=DARK, corner_radius=0)
            row.grid(row=r, column=0, padx=4, pady=2, sticky="ew")
            row.grid_columnconfigure(1, weight=1)

            face = tk.Canvas(row, width=34, height=34, bg=DARK, highlightthickness=0)
            face.grid(row=0, column=0, rowspan=2, padx=8, pady=6)
            face.create_text(17, 17, text=MOODS[e["mood"]]["emoji"], font=(EMOJI_FONT, -24))

            ctk.CTkLabel(
                row, text=f"{d} · {MOODS[e['mood']]['name']}",
                text_color=WHITE, font=("Arial", 11, "bold"), anchor="w",
            ).grid(row=0, column=1, sticky="ew")
            ctk.CTkLabel(
                row, text=e["note"] or "—", text_color="#D0D0D0",
                font=("Arial", 10), anchor="w", wraplength=330, justify="left",
            ).grid(row=1, column=1, sticky="ew", pady=(0, 6))

    def open_settings(self):
        if self.settings_popup is not None and self.settings_popup.winfo_exists():
            self.settings_popup.lift()
            return

        win = ctk.CTkToplevel(self)
        self.settings_popup = win
        win.title("Settings")
        win.geometry("320x230")
        win.resizable(False, False)
        win.configure(fg_color=PANEL)
        win.transient(self)

        ctk.CTkLabel(
            win, text="Settings", font=("Arial", 17, "bold"), text_color=DARK
        ).pack(anchor="w", padx=18, pady=12)

        ctk.CTkButton(
            win, text="EXPORT HISTORY (CSV)", height=38, corner_radius=2,
            fg_color=DARK, hover_color=GRAY, text_color=WHITE,
            command=self.export_csv,
        ).pack(fill="x", padx=18, pady=4)
        ctk.CTkButton(
            win, text="CLEAR ALL HISTORY", height=38, corner_radius=2,
            fg_color=GRAY, hover_color=WHITE, text_color=BLACK,
            command=self.clear_history,
        ).pack(fill="x", padx=18, pady=4)
        ctk.CTkButton(
            win, text="CLOSE", height=38, corner_radius=2,
            fg_color=GRAY, hover_color=WHITE, text_color=BLACK,
            command=win.destroy,
        ).pack(fill="x", padx=18, pady=4)

    def export_csv(self):
        try:
            with open(EXPORT_FILE, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["date", "time", "mood_score", "mood", "note"])
                for key in sorted(self.entries):
                    e = self.entries[key]
                    w.writerow([key, e["time"], e["mood"], MOODS[e["mood"]]["name"], e["note"]])
            messagebox.showinfo("Exported", f"Saved to:\n{EXPORT_FILE}", parent=self.settings_popup)
        except Exception as e:
            messagebox.showerror("Export Error", str(e), parent=self.settings_popup)

    def clear_history(self):
        if not self.entries:
            messagebox.showinfo("Nothing to clear", "History is already empty.",
                                parent=self.settings_popup)
            return
        if messagebox.askyesno(
            "Clear history", "Delete all mood entries? This cannot be undone.",
            parent=self.settings_popup,
        ):
            self.entries = {}
            self.stack.clear()
            self.save_data()
            self.restore_today()
            self.refresh_all()

    def reset_caption(self):
        self.trend_caption.configure(
            text="Scale: 1 = Awful, 5 = Great. Hover a point for details."
        )

    def draw_trend(self):
        c = self.trend_canvas
        c.delete("all")
        self.chart_points = []

        w = max(c.winfo_width(), 300)
        h = max(c.winfo_height(), 110)
        left, right, top, bottom = 28, 14, 10, 22
        cw, ch = w - left - right, max(20, h - top - bottom)

        def X(i): return left + cw * i / 13
        def Y(m): return top + ch - (m - 1) / 4 * ch

        for m in range(1, 6):
            c.create_line(left, Y(m), w - right, Y(m), fill=GRID if m in (1, 5) else "#c4c4c4")
            c.create_text(left - 10, Y(m), text=str(m), fill=GRAY, font=("Arial", 8))

        days = [date.today() - timedelta(days=13 - i) for i in range(14)]
        pts = []
        for i, d in enumerate(days):
            if (13 - i) % 2 == 0:
                c.create_text(X(i), h - 9, text=str(d.day), fill=DARK, font=("Arial", 8))
            e = self.entries.get(d.isoformat())
            if e:
                x, y = X(i), Y(e["mood"])
                pts.append((x, y))
                self.chart_points.append((x, y, d, e))

        if not pts:
            c.create_text(w / 2, h / 2, text="No entries yet. Log your first mood above.",
                          fill=GRAY, font=("Arial", 10))
            return

        if len(pts) > 1:
            c.create_line(*[v for p in pts for v in p], fill=DARK, width=3,
                          joinstyle="round", capstyle="round")
        for x, y in pts:
            c.create_oval(x - 5, y - 5, x + 5, y + 5, fill=DARK, outline=WHITE, width=2)

    def on_trend_motion(self, event):
        best, best_d = None, 18
        for x, y, d, e in self.chart_points:
            dist = hypot(event.x - x, event.y - y)
            if dist < best_d:
                best, best_d = (d, e), dist
        if best is None:
            self.reset_caption()
            return
        d, e = best
        text = f"{d.strftime('%d %b')} · {MOODS[e['mood']]['name']}"
        if e["note"]:
            note = e["note"] if len(e["note"]) <= 70 else e["note"][:67] + "..."
            text += f" — {note}"
        self.trend_caption.configure(text=text)

    def draw_donut(self):
        c = self.donut_canvas
        c.delete("all")

        w = max(c.winfo_width(), 240)
        h = max(c.winfo_height(), 110)

        cutoff = date.today() - timedelta(days=29)
        counts = {m: 0 for m in MOODS}
        for key, e in self.entries.items():
            if datetime.strptime(key, "%Y-%m-%d").date() >= cutoff:
                counts[e["mood"]] += 1
        total = sum(counts.values())

        size = max(60, min(h - 16, w * 0.45, 170))
        ring = size * 0.17
        x0, y0 = 14 + ring / 2, (h - size) / 2 + ring / 2
        x1, y1 = 14 + size - ring / 2, (h + size) / 2 - ring / 2
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2

        if total == 0:
            c.create_oval(x0, y0, x1, y1, outline="#c4c4c4", width=ring)
            c.create_text(cx, cy, text="No data", fill=GRAY, font=("Arial", 10))
        else:
            angle = 90
            for m in MOODS:
                if counts[m] == 0:
                    continue
                extent = -359.9 if counts[m] == total else -360 * counts[m] / total
                c.create_arc(x0, y0, x1, y1, start=angle, extent=extent,
                             style="arc", outline=MOODS[m]["color"], width=ring)
                angle += extent
            avg = sum(m * n for m, n in counts.items()) / total
            c.create_text(cx, cy - 6, text=f"{avg:.1f}", fill=DARK, font=("Arial", 16, "bold"))
            c.create_text(cx, cy + 12, text="avg mood", fill=GRAY, font=("Arial", 8))

        lx = 14 + size + 22
        step = min(24, (h - 12) / 5)
        ly = h / 2 - step * 2
        for m in reversed(MOODS):
            pct = counts[m] / total * 100 if total else 0
            c.create_rectangle(lx, ly - 6, lx + 12, ly + 6,
                               fill=MOODS[m]["color"], outline=DARK)
            c.create_text(lx + 20, ly, anchor="w", fill=DARK, font=("Arial", 10),
                          text=f"{MOODS[m]['name']}  {counts[m]} ({pct:.0f}%)")
            ly += step

    def refresh_all(self):
        self.streak_label.configure(text=str(self.current_streak()))
        logged = date.today().isoformat() in self.entries
        self.continue_button.configure(text="Update →" if logged else "Continue →")
        top = self.stack.peek()
        top_text = (
            f"{top['date']} {MOODS[top['mood']]['name']}" if top else "empty"
        )
        self.stack_label.configure(text=f"Stack size: {self.stack.size()}  |  Top: {top_text}")
        self.undo_button.configure(state="disabled" if self.stack.is_empty() else "normal")
        self.peek_button.configure(state="disabled" if self.stack.is_empty() else "normal")
        self.reset_caption()
        self.draw_trend()
        self.draw_donut()


if __name__ == "__main__":
    app = MoodTrackingPage()
    app.mainloop()
