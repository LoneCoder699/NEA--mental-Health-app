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
        if d.isoformat() not in self.entries:
            d -= timedelta(days = 1)
        n = 0
        while d.isoformat() in self.entries:
            n+=1
            d-=timedelta(days = 1)
        return n


    def build_ui(self):
        self.grid_columnconfigure(0,weight=0)
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(0,weight=1)
        self.build_navbar()
        self.main = ctk.CTkFrame(self,fg_color = BG)
        self.main.grid(row = 0, column = 1, sticky = 'nsew')
        self.main.grid_columnconfigure(0,weight=1)
        self.main.grid_columnconfigure(1,weight=0)
        self.main.grid_columnconfigure(2,weight=0)
        self.main.grid_rowconfigure(0,weight=1)
        self.mood_label = ctk.CTkLabel(self.main,text = 'HOW IS YOUR MOOD?', font = ("Arial", 25), text_color = DARK)
        self.mood_label.grid(row = 0, column = 0, columnspan = 2, pady = (8,0))
        self.build_mood_card()
        self.build_streak()
        self.create_sidebar()
        self.build_bottom()


    def build_navbar(self):

        self.create_left_navbar()

    def create_left_navbar(self):

        self.left_nav_expanded = True

        self.left_nav_width = 260

        self.left_nav_collapsed_width = 65

        self.left_navbar = ctk.CTkFrame(
            self,
            width=self.left_nav_width,
            fg_color=GRAY,
            corner_radius=0,
        )

        self.left_navbar.grid(
            row=0,
            column=0,
            sticky="ns"
        )

        self.left_navbar.grid_propagate(
            False
        )

        self.left_nav_top = ctk.CTkFrame(
            self.left_navbar,
            height=100,
            fg_color="transparent",
        )

        self.left_nav_top.pack(
            fill="x",
            padx=5,
            pady=(10, 20)
        )

        self.left_nav_top.pack_propagate(
            False
        )

        self.left_logo = ctk.CTkLabel(
            self.left_nav_top,
            text="Logo",
            width=160,
            height=70,
            fg_color=SIDEBAR,
            text_color=WHITE,
            font=("Arial", 13),
            corner_radius=0,
        )

        self.left_logo.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        self.left_toggle = ctk.CTkButton(
            self.left_nav_top,
            text="<",
            width=45,
            height=70,
            fg_color=SIDEBAR,
            hover_color="#333333",
            text_color=WHITE,
            font=("Arial", 24),
            corner_radius=0,
            command=self.toggle_left_navbar,
        )

        self.left_toggle.pack(
            side="right"
        )

        self.left_menu_frame = ctk.CTkFrame(
            self.left_navbar,
            fg_color="transparent"
        )

        self.left_menu_frame.pack(
            fill="both",
            expand=True,
            padx=3
        )

        self.left_nav_buttons = []

        menu_items = [

            (
                "Mental health survey",
                self.open_mental_health_survey
            ),

            (
                "AI ChatBot",
                self.open_ai_chatbot
            ),

            (
                "Appointment Booking",
                self.open_appointment_booking
            ),

            (
                "Journaling",
                self.open_journaling
            ),

            (
                "Mood Tracking",
                self.open_mood_tracking
            ),

            (
                "Goal Tracking",
                self.open_goal_tracking
            ),

            (
                "News/ Blogs",
                self.open_news_blogs
            ),

            (
                "Resources",
                self.open_resources
            ),
        ]

        for text, command in menu_items:

            separator = ctk.CTkFrame(
                self.left_menu_frame,
                height=10,
                fg_color=GRAY,
                corner_radius=0,
            )

            separator.pack(
                fill="x"
            )

            button = ctk.CTkButton(
                self.left_menu_frame,
                text=text,
                height=48,
                fg_color=SIDEBAR,
                hover_color="#333333",
                text_color="#D0D0D0",
                font=("Arial", 14),
                corner_radius=0,
                anchor="center",
                command=command,
            )

            button.pack(
                fill="x"
            )

            self.left_nav_buttons.append(
                (button, text)
            )

    def go_home(self):
        self.close_dropdowns()
        print("Navigating to Home Page")

    def open_profile(self):
        self.close_dropdowns()
        print("Navigating to Profile Page")
    
    def logout(self):
        self.close_dropdowns()
        print("Logging out...")

    def toggle_left_navbar(self):

        if self.left_nav_expanded:

            self.left_navbar.configure(
                width=self.left_nav_collapsed_width
            )

            self.left_logo.pack_forget()

            self.left_toggle.configure(
                text=">"
            )

            for button, text in self.left_nav_buttons:

                button.configure(
                    text=""
                )

            self.left_nav_expanded = False

        else:

            self.left_navbar.configure(
                width=self.left_nav_width
            )

            self.left_logo.pack(
                side="left",
                fill="both",
                expand=True,
                padx=(0, 10)
            )

            self.left_toggle.configure(
                text="<"
            )

            for button, text in self.left_nav_buttons:

                button.configure(
                    text=text
                )

            self.left_nav_expanded = True

    def open_mental_health_survey(self):
        print("Mental Health Survey selected")

    def open_ai_chatbot(self):
        print("AI ChatBot selected")

    def open_appointment_booking(self):
        print("Appointment Booking selected")

    def open_journaling(self):
        print("Journaling selected")

    def open_mood_tracking(self):
        print("Mood Tracking selected")

    def open_goal_tracking(self):
        print("Goal Tracking selected")

    def open_news_blogs(self):
        print("News / Blogs selected")

    def open_resources(self):
        print("Resources selected")

    def build_mood_card(self):
        card = ctk.CTkFrame(self.main, fg_color = PANEL)
        card.grid(row = 1, column = 0, padx = (16,6), pady = 8, sticky = 'nsew')
        self.face_canvas = tk.Canvas(card,wdith = 100, height = 100, bg = PANEL)
        self.face_canvas.pack(pady = (10,0))
        self.feeling_label = ctk.CTkLabel(card,text="I am feeling ___", font = ("Arial",24), text_color = DARK)
        self.feeling_label.pack(pady = (0,5))
        self.panel = ctk.CTkFrame(card, fg_color = DARK)
        self.panel.pack(fill = 'x', padx = 12)
        self.row = ctk.CTkFrame(self.panel,fg_color = 'transparent')
        self.row.pack(fill = 'x',padx = 12, pady = (10,4))
        self.row.grid_columnconfigure(tuple(range(5)),weight = 1)
        for i,value in enumerate(MOODS):
            iv = tk.Canvas(self.row,width = 70, height = 40,bg = GRAY)
            iv.grid(row = 0, column = 1, padx = 5)
            iv.bind('<Button-1>',lambda e, v = value: self.select_mood(v))
            self.mood_buttons[value] = iv
        note_row = ctk.CTkFrame(self.panel, fg_color = 'transparent')
        note_row.pack(fill = 'x', padx = 14, pady = (0,10))
        note_row.grid_columnconfigure(1,weight = 1)
        self.note_label = ctk.CTkLabel(note_row, text = 'Short Note:', text_color = WHITE, font = ("Arial", 12))
        self.note_label.grid(row = 0, column = 0, padx = (0,8))
        self.note_entry = ctk.CTkEntry(note_row , height = 30, corner_radius = 2, fg_color = BLACK, text_color = WHITE, placeholder_text = "What's on your mind? (optional)", placeholder_text_color= GRAY)
        self.note_entry.grid(row = 0, column = 1)
        self.note_entry.bind('<Return>', lambda e: self.submit_mood())
        self.continue_button = ctk.CTkButton(card, text = 'Continue →', width = 200, height = 30, corner_radius = 15, fg_color = BLACK, hover_color = GRAY, text_color = WHITE, font = ("Arial", 12), command = self.submit_mood)
        self.continue_button.pack(pady =(10,2))
        self.status_label = ctk.CTkLabel(card, text = '', font = ("Arial", 10), text_color = GRAY)
        self.status_label.pack(pady = (0,6))


    def build_streak(self):
        streak_frame = ctk.CTkFrame(self.main, fg_color = PANEL, width = 100)
        streak_frame.grid(row =1, column = 1, padx = 6, pady = 8, sticky = 'nsew')
        streak_frame.grid_propagate(False)
        streak_frame.pack_propagate(False)
        streak_label = ctk.CTkLabel(streak_frame, text = 'Streak', font = ("Arial", 12), text_color = DARK)
        streak_label.pack(pady = (10,0))
        days_label = ctk.CTkLabel(streak_frame, text = 'Day', font = ("Arial", 20), text_color = DARK)
        days_label.pack()
        no_label = ctk.CTkLabel(streak_frame, text = '0', font = ("Arial", 22), text_color = DARK)
        no_label.pack()
        flame = tk.Canvas(streak_frame, width = 45, height = 48, bg = PANEL)
        flame.pack(pady = (4,0))
        flame.create_polygon(22,3,34,20,37,33,29,45,15,45,7,33,10,20,17,27,smooth = True, fill = DARK, outline = DARK)
        flame.create_oval(16,30,28,44,fill = PANEL, outline = PANEL)


    def create_sidebar(self):
        self.sidebar_open = True
        self.sidebar = ctk.CTkFrame(
            self,
            width=90,
            fg_color=SIDEBAR,
            corner_radius=0
        )
        self.sidebar.place(
            relx=1,
            rely=0,
            anchor="ne"
        )

        self.sidebar.pack_propagate(False)

        self.sidebar_toggle = ctk.CTkButton(
            self.sidebar,
            text=">",
            width=55,
            height=40,
            fg_color="transparent",
            hover_color="#333333",
            text_color=WHITE,
            font=("Arial", 22),
            corner_radius=0,
            command=self.toggle_sidebar
        )

        self.sidebar_toggle.pack(
            pady=(15, 20)
        )
    
        logo = ctk.CTkLabel(
            self.sidebar,
            text="C",
            font=("Arial", 32, "bold"),
            text_color=WHITE
        )

        logo.pack(
            pady=(0, 35)
        )

        home_button = ctk.CTkButton(
            self.sidebar,
            text="⌂",
            width=55,
            height=50,
            fg_color="transparent",
            hover_color="#333333",
            text_color=WHITE,
            font=("Arial", 28),
            command=self.go_home
        )

        home_button.pack(
            pady=10
        )

        profile_button = ctk.CTkButton(
            self.sidebar,
            text="◉",
            width=55,
            height=50,
            fg_color="transparent",
            hover_color="#333333",
            text_color=WHITE,
            font=("Arial", 24),
            command=self.open_profile
        )

        profile_button.pack(
            pady=10
        )

        spacer = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        spacer.pack(
            expand=True,
            fill="both"
        )

        self.after(
            100,
            self.set_sidebar_height
        )

    def set_sidebar_height(self):

        height = self.winfo_height()

        if height > 1:

            self.sidebar.configure(
                height=height
            )

    def toggle_sidebar(self):

        if self.sidebar_open:

            self.animate_sidebar_close()

        else:

            self.animate_sidebar_open()

    def animate_sidebar_open(self, height=0):

        max_height = self.winfo_height()

        if max_height <= 1:

            self.after(
                50,
                lambda: self.animate_sidebar_open(height)
            )

            return

        if height < max_height:

            height += 25

            if height > max_height:
                height = max_height

            self.sidebar.configure(
                height=height,
                width=90
            )

            self.after(
                10,
                lambda: self.animate_sidebar_open(height)
            )

        else:

            self.sidebar_open = True

            self.sidebar_toggle.configure(
                text=">"
            )

    def animate_sidebar_close(self, height=None):

        max_height = self.winfo_height()

        if max_height <= 1:
            return

        if height is None:
            height = max_height

        if height > 0:

            height -= 25

            if height < 0:
                height = 0

            self.sidebar.configure(
                height=height,
                width=90
            )

            self.after(
                10,
                lambda: self.animate_sidebar_close(height)
            )

        else:

            self.sidebar.configure(
                width=90,
                height=1
            )

            self.sidebar_open = False

            self.sidebar_toggle.configure(
                text="<"
            )    


    def build_bottom(self):
        bottom = ctk.CTkFrame(self.main, fg_color = 'transparent')
        bottom.grid(row=2,column = 0, padx = 16, pady = (0,14), columnspan = 3, sticky = 'nsew')
        bottom.grid_columnconfigure(0, weight = 2)
        bottom.grid_columnconfigure(1, weight = 2)
        bottom.grid_rowconfigure(0, weight = 1)
        chart = ctk.CTkFrame(bottom, fg_color = PANEL)
        chart.grid(row = 0, column = 0, padx = (0,6), sticky = 'nsew')
        trend_label = ctk.CTkLabel(chart, text = "MOOD TREND (LAST 2 WEEKS)", font = ("Arial", 12, 'bold'), text_color = DARK)
        trend_label.pack(anchor = 'nw', padx = 10, pady = (8,0))
        self.caption = ctk.CTkLabel(chart, text = '', font = ("Arial", 10))
        self.caption.pack(anchor = 'nw', padx = 12)
        self.chart_canvas = tk.Canvas(chart, bg = PANEL)
        self.chart_canvas.pack()