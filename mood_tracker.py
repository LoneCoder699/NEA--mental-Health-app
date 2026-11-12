import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, date, timedelta
import json
from pathlib import Path
from collections import deque
from tkcalendar import DateEntry
import sys
import csv

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

if sys.platform.startswith("win"):
    EMOJI_FONT = "Segoe UI Emoji"

elif sys.platform == "darwin":
    EMOJI_FONT = "Apple Color Emoji"
else:
    EMOJI_FONT = "Noto Color Emoji"

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
        self.chart_canvas.pack(fill = 'both', expand = True, padx = 8, pady = (2,8))
        self.chart_canvas.bind('<Configure>', lambda e: self.draw_chart())
        self.chart_canvas.bind('<Motion>', self.hover_chart)
        self.chart_canvas.bind('<Leave>', lambda e: self.reset_caption())
        donut = ctk.CTkFrame(bottom, fg_color = PANEL)
        donut.grid(row = 0, column = 1, padx = (6,0), sticky = 'nsew')
        donut_label = ctk.CTkLabel(donut, text = 'MOOD BREAKDOWN (Last 30 days)', font= ('Arial', 10, 'bold'), text_color = DARK)
        donut_label.pack(anchow = 'nw', padx = 12, pady = (9,0))
        self.donut_canvas = tk.Canvas(donut, bg= PANEL)
        self.donut_canvas.pack(expand = True, fill = 'both', padx = 8, pady = 8)
        self.donut_canvas.bind('<Configure>', lambda e: self.draw_donut())


    def select_mood(self, mood):
        self.selected_mood = mood
        for value,cv in self.mood_buttons.items():
            cv.delete('all')
            cv.configure(bg = WHITE if value == mood else GRAY)
            cv.create_text(36,20, text = MOODS[value]['emoji'], font = (EMOJI_FONT,-25))
            self.feeling_label.configure(text = f'I am feeling {MOODS[mood]['name']}' else 'I am feeling _____')
            self.face_canvas.delete('all')
            self.face_canvas.create_text(50,50, text = MOODS[mood or 3]['emoji'], font = (EMOJI_FONT,-75))


    def restore_today(self):
        entry = self.entries.get(date.today().isoformat())
        self.select_mood(entry['mood'] if entry else None)
        self.note_entry.delete(0,'n')
        if entry and entry['note']:
            self.note_entry.insert(0,entry['note'])


    def submit_mood(self):
        if self.selected_mood is None:
            messagebox.showwarning('pick a mood', 'please choose the mood according to how you are feeling first', parent = self)

        self.entries[date.today().isoformat()] = {'mood':self.selected_mood,'note':self.note_entry.get().strip(), 'time':datetime.now().strftime('%H:%M')}
        self.save_data()
        self.refresh_all()
        self.status_label.configure(text = f"saved:{MOODS[self.selected_mood]['name']}. Streak Day {self.current_streak()}")
        self.after(4000,lambda:self.status_label.configure(text = ''))


    def open_history(self):
        if self.history_popup is not None and self.history_popup.winfo_exists():
            self.history_popup.lift()
            return
        win = ctk.CTkToplevel(self)
        self.histroy_popup = win
        win.title('mood history')
        win.geometry('460x520')
        win.configure(fg_color = PANEL)
        win.transient(self)
        history_label = ctk.CTkLabel(win, text = 'mood history', font = {'Arial', 16, 'bold'})
        history_label.pack(anchor = 'w', padx = 20, pady = 12)
        scroll_frame = ctk.CTkScrollableFrame(win, bg = 'white')
        scroll_frame.pack(fill = 'both', expand = True, padx = 12, pady = (0,12))
        scroll_frame.grid_columnconfigure(0, weight = 1)
        id = sorted(self.entries,reverse = True)
        if not id:
            no_mood_label = ctk.CTkLabel(scroll_frame, text = 'No Mood Entries Yet', text_color = GRAY)
            no_mood_label.grid(row = 0, column = 0, pady = 20)
            return

        for r,key in enumerate(id):
            e = self.entries[key]
            d = datetime.strptime(key, "%Y-%m-%d").strftime('%a,%d %b %Y')
            row = ctk.CTkFrame(scroll_frame, fg_color = DARK)
            row.grid(row = r, padx = 4, pady = 2, sticky = 'ew')
            row.grid_columnconfigure(1, weight = 1)
            face = tk.Canvas(row, width = 30, height = 30, bg = DARK)
            face.grid(row = 0, column = 0, rowspan = 2, padx = 8, pady = 6)
            face.create_text(17,17,text = MOODS[e['mood']]['emoji'], font = (EMOJI_FONT,-25))
            mood_one_label = ctk.CTkLabel(row, text = f"{d}.{MOODS[e['mood']]['name']}", text_color = WHITE, font = ("Arial", 12, 'bold'), anchor = 'w')
            mood_one_label.grid(row = 0, column = 1, sticky = 'ew')
            note_one_label = ctk.CTkLabel(row,text = e['note'] or '___', text_color = GRAY, font = ("Arial", 11), anchor = 'w', wraplength = 350,justify = 'left')
            note_one_label.grid(row =1, column = 1, sticky = 'ew', pady = (0,6))


    def open_settings(self):
        if self.settings_popup is not None and self.settings_popup.winfo_exists():
            self.settings_popup.lift()
            return
        win = ctk.CTkToplevel(self)
        self.settings_popup = win
        win.title('Settings')
        win.geometry('320x230')
        win.resizeable(False, False)
        win.configure(fg_color = PANEL)
        win.transient(self)
        mood_settings_label = ctk.CTkLabel(win,text = 'Mood settings', font = ('Arial', 16, 'bold'), text_color = DARK)
        mood_settings_label.pack(anchor = 'west', padx = 18, pady = 12, text_color = DARK)
        export_button = ctk.CTkButton(win,text = 'Export History', height = 40, corner_radius = 2, fg_color = DARK, text_color = WHITE, hover_color = GRAY, command = self.export)
        export_button.pack(fill = 'x', padx = 18, pady = 4)
        clearall_button = ctk.CTkButton(win,text = 'Clear All History', height = 40, corner_radius = 2, fg_color = DARK, text_color = WHITE, hover_color = GRAY, command = self.clearall)
        clearall_button.pack(fill = 'x', padx = 18, pady = 4) 
        close_button = ctk.CTkButton(win,text = 'Close History', height = 40, corner_radius = 2, fg_color = DARK, text_color = WHITE, hover_color = GRAY, command = self.close)
        close_button.pack(fill = 'x', padx = 18, pady = 4)
    

    def export(self):
        try:
            with open(EXPORT_FILE,"w",encoding = 'utf8') as f:
                w = csv.writer(f)
                w.writerow(['date','time','mood_score','mood','note'])
                for key in sorted(self.entries):
                    e = self.entries[key]
                    w.writerow([key,e['time'],e['mood'],MOODS[e['mood']]['name'],e['note']])
            messagebox.showinfo('exported',f'Saved to- \n{EXPORT_FILE}',parent = self.settings_popup)

        except Exception as e:
            messagebox.showerror('Export Error', str(e), parent = self.settings_popup)


    def clear_all(self):
        if not self.entries:
            messagebox.showinfo('No entries', 'History is already empty', parent = self.settings_popup)
            return
        if messagebox.askyesno('clear history', 'Delete all mood entries? This cannot be undone', parent = self.settings_popup)
        self.entries = {}
        self.save_data()
        self.restore_today()
        self.refresh_all()


    def reset_caption(self):
        self.trend_caption.configure(text = 'Scale: 1 = Awful, 5 = Great. Hover a point for details')


    def draw_chart(self):
        c = self.chart_canvas
        c.delete('all')
        self.chart_points = []
        w = max(c.winfo_width(),300)
        h = max(c.winfo_height(), 110)
        left, right, top, bottom = 28,14,10,22
        cw,ch = w-left-right, max(20,h-top-bottom)

        def X(i):
            return left+cw*i/13
        
        def Y(j):
            return top+ch-(j-1)/4*ch
        
        for j in range(1,6):
            c.create_line(left,Y(j),w-right,Y(j),fill = GRID if m in (1,5) else "#c4c4c4")
            c.create_text(left-10,Y(j), text = str(j), fill = GRAY, font = ("Arial", 8))
        
        days = [date.today()-timedelta(days = 13-i) for i in range(14)]
        pts = []